# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# tsp_graph.py — Modelagem do grafo e construção do QUBO por aresta
# =============================================================================
#
# Comparação de complexidade de qubits:
#
#   Modelagem por vértice (node-based) — padrão Qiskit Tsp:
#     qubits = N²   →  4 cidades = 16, 6 cidades = 36  (estoura RAM)
#
#   Modelagem por aresta (edge-based) — implementada aqui:
#     qubits = N(N-1)/2  →  4 cidades = 6, 6 cidades = 15  (viável)
#
# Na modelagem por aresta cada variável binária x_{ij} representa
# "a aresta entre a cidade i e a cidade j está na rota?" (1) ou não (0).
#
# O Hamiltoniano é composto por:
#   H_custo    = soma dos pesos das arestas ativas
#   H_grau     = penaliza nós com grau != 2 (cada cidade deve ter exatamente
#                2 arestas: uma de chegada e uma de saída)
#   H_subtour  = penaliza sub-rotas (ciclos que não visitam todas as cidades)
#
# Referência: Hadfield et al. (2019) — "From the Quantum Approximate
# Optimization Algorithm to a Quantum Alternating Operator Ansatz"
# =============================================================================

import numpy as np
import itertools
import networkx as nx
from qiskit_optimization.problems import QuadraticProgram


def create_graph(w: list[list[int]]) -> nx.Graph:
    """Transforma a matriz de adjacência em um Grafo NetworkX.

    Args:
        w: Matriz de adjacência N×N com os custos entre cidades.

    Returns:
        Grafo não-dirigido com os pesos nas arestas.
    """
    G = nx.Graph()
    n = len(w)
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(i + 1, n):
            G.add_edge(i, j, weight=w[i][j])
    return G


def _edge_index(i: int, j: int, n: int) -> int:
    """Retorna o índice linear da aresta (i, j) com i < j.

    As arestas são enumeradas percorrendo o triângulo superior da matriz:
    (0,1)=0, (0,2)=1, ..., (0,n-1)=n-2, (1,2)=n-1, ...

    Args:
        i: Índice do primeiro vértice (deve ser < j).
        j: Índice do segundo vértice.
        n: Número total de cidades.

    Returns:
        Índice inteiro da variável x_{ij} no vetor de decisão.
    """
    if i > j:
        i, j = j, i
    return i * n - i * (i + 1) // 2 + (j - i - 1)


def build_qubo(w: list[list[int]], penalty: float = None):
    """Constrói o QUBO do TSP usando modelagem baseada em arestas (edge-based).

    Cada variável binária x_{ij} representa a presença da aresta (i,j)
    na rota. A formulação usa N(N-1)/2 qubits em vez de N² — redução
    crítica para rodar instâncias de 5 e 6 cidades em 16 GB RAM.

    Hamiltoniano completo:
        H = H_custo + penalty * (H_grau + H_subtour)

    H_custo:   minimiza a soma dos pesos das arestas ativas.
    H_grau:    garante grau exatamente 2 para cada cidade
               (restrição: sum_{j≠i} x_{ij} = 2 para todo i).
    H_subtour: penaliza sub-rotas via restrição de Miller-Tucker-Zemlin
               simplificada para grafos pequenos (N <= 6).

    Args:
        w:       Matriz de adjacência N×N.
        penalty: Peso das restrições. Se None, usa 2 * max(w) automaticamente.

    Returns:
        Tuple (qp, edge_list) onde:
          qp        — QuadraticProgram pronto para conversão QUBO.
          edge_list — lista de tuplas (i, j) na ordem das variáveis.
    """
    n       = len(w)
    w_arr   = np.array(w, dtype=float)
    penalty = penalty if penalty is not None else 2.0 * w_arr[w_arr < 1e8].max()

    # Lista ordenada de arestas (triângulo superior)
    edges     = [(i, j) for i in range(n) for j in range(i + 1, n)]
    num_edges = len(edges)  # = N(N-1)/2

    qp = QuadraticProgram(name="TSP_edge")

    # Variáveis binárias: x_i_j = 1 se aresta (i,j) está na rota
    for i, j in edges:
        qp.binary_var(name=f"x_{i}_{j}")

    # -------------------------------------------------------------------------
    # H_custo: minimiza custo total das arestas ativas
    # -------------------------------------------------------------------------
    linear_cost = {f"x_{i}_{j}": w_arr[i][j] for i, j in edges}
    qp.minimize(linear=linear_cost)

    # -------------------------------------------------------------------------
    # H_grau: cada cidade deve ter exatamente 2 arestas (chegada + saída)
    # Restrição: sum_{j≠i} x_{ij} = 2  para todo i em {0, ..., n-1}
    # -------------------------------------------------------------------------
    for i in range(n):
        neighbors = {}
        for j in range(n):
            if i == j:
                continue
            a, b = (i, j) if i < j else (j, i)
            neighbors[f"x_{a}_{b}"] = 1
        qp.linear_constraint(
            linear=neighbors,
            sense="==",
            rhs=2,
            name=f"grau_{i}",
        )

    # -------------------------------------------------------------------------
    # H_subtour: para N <= 6 usa eliminação explícita de sub-rotas
    # Garante que não existam ciclos parciais de tamanho k < N.
    # Para cada subconjunto S de tamanho 2 <= k <= N//2, o número de
    # arestas dentro de S deve ser <= |S| - 1.
    # -------------------------------------------------------------------------
    cidades = list(range(n))
    for k in range(2, n // 2 + 1):
        for subset in itertools.combinations(cidades, k):
            subset_edges = {
                f"x_{i}_{j}": 1
                for i, j in itertools.combinations(subset, 2)
            }
            if subset_edges:
                qp.linear_constraint(
                    linear=subset_edges,
                    sense="<=",
                    rhs=len(subset) - 1,
                    name=f"subtour_{'_'.join(map(str, subset))}",
                )

    return qp, edges


def interpret_edge_solution(x: np.ndarray, edges: list, n: int) -> list[int]:
    """Converte o vetor de solução edge-based em uma rota ordenada de cidades.

    Reconstrói o ciclo hamiltoniano a partir das arestas ativas (x_{ij} = 1),
    começando sempre pela cidade 0.

    Args:
        x:     Vetor binário de solução (uma entrada por aresta).
        edges: Lista de tuplas (i, j) na mesma ordem das variáveis.
        n:     Número de cidades.

    Returns:
        Lista ordenada de cidades representando a rota, ou lista vazia
        se a solução não formar um ciclo hamiltoniano válido.
    """
    # Monta lista de adjacência com as arestas ativas
    adj = {i: [] for i in range(n)}
    for idx, (i, j) in enumerate(edges):
        if round(x[idx]) == 1:
            adj[i].append(j)
            adj[j].append(i)

    # Verifica se todo nó tem grau 2 (condição necessária para ciclo hamiltoniano)
    if any(len(v) != 2 for v in adj.values()):
        return []

    # Percorre o ciclo a partir da cidade 0
    route   = [0]
    prev    = -1
    current = 0
    for _ in range(n - 1):
        nexts = [v for v in adj[current] if v != prev]
        if not nexts:
            return []
        prev, current = current, nexts[0]
        route.append(current)

    return route if len(route) == n else []
