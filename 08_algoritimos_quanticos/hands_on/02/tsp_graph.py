# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# tsp_graph.py — Modelagem otimizada com Poda de Arestas (Pruning)
# =============================================================================

import numpy as np
import itertools
import networkx as nx
from qiskit_optimization.problems import QuadraticProgram

def create_graph(w: list[list[int]]) -> nx.Graph:
    """Transforma a matriz de adjacência em um Grafo NetworkX."""
    G = nx.Graph()
    n = len(w)
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(i + 1, n):
            # Apenas adiciona ao grafo visual se não for uma 'parede' (custo 50)
            if w[i][j] < 50:
                G.add_edge(i, j, weight=w[i][j])
    return G

def build_qubo(w: list[list[int]], penalty: float = None):
    """
    Constrói o QUBO com Poda de Arestas para reduzir o número de qubits.
    Arestas com custo >= 50 são ignoradas na criação de variáveis binárias.
    """
    n = len(w)
    w_arr = np.array(w, dtype=float)
    
    # Define penalidade: se não informada, usa o dobro do maior custo válido
    valid_costs = w_arr[w_arr < 50]
    max_val = valid_costs.max() if valid_costs.size > 0 else 10
    penalty = penalty if penalty is not None else 2.5 * max_val

    qp = QuadraticProgram(name="TSP_edge_optimized")
    
    # 1. Identificar arestas viáveis (Poda/Pruning)
    # Apenas criamos qubits para caminhos que fazem sentido econômico
    active_edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if w[i][j] < 50:
                var_name = f"x_{i}_{j}"
                qp.binary_var(name=var_name)
                active_edges.append((i, j))

    # 2. H_custo: Minimizar pesos das arestas ativas
    linear_objective = {f"x_{i}_{j}": w[i][j] for i, j in active_edges}
    qp.minimize(linear=linear_objective)

    # 3. H_grau: Cada cidade deve ter grau 2
    # sum_{j ligado a i} x_{ij} = 2
    for i in range(n):
        # Filtra apenas as variáveis que envolvem a cidade 'i'
        incident_vars = {
            f"x_{a}_{b}": 1 
            for a, b in active_edges if a == i or b == i
        }
        
        # Só adiciona restrição se a cidade tiver ao menos 2 arestas possíveis
        if len(incident_vars) >= 2:
            qp.linear_constraint(
                linear=incident_vars,
                sense="==",
                rhs=2,
                name=f"grau_{i}"
            )

    # 4. H_subtour: Eliminação de ciclos menores (apenas para arestas ativas)
    cidades = list(range(n))
    for k in range(2, n // 2 + 1):
        for subset in itertools.combinations(cidades, k):
            # Arestas internas ao subconjunto que existem no modelo
            subset_edges = {
                f"x_{a}_{b}": 1
                for a, b in itertools.combinations(subset, 2)
                if (a, b) in active_edges or (b, a) in active_edges
            }
            
            if len(subset_edges) >= k: # Só restringe se houver risco de ciclo
                qp.linear_constraint(
                    linear=subset_edges,
                    sense="<=",
                    rhs=len(subset) - 1,
                    name=f"sub_cluster_{'_'.join(map(str, subset))}"
                )

    return qp, active_edges

def interpret_edge_solution(x: np.ndarray, edges: list, n: int) -> list[int]:
    """Reconstrói a rota a partir das arestas ativas."""
    adj = {i: [] for i in range(n)}
    for idx, (i, j) in enumerate(edges):
        if round(x[idx]) == 1:
            adj[i].append(j)
            adj[j].append(i)

    if any(len(v) != 2 for v in adj.values()):
        return []

    route = [0]
    prev = -1
    curr = 0
    try:
        for _ in range(n - 1):
            nxt = [v for v in adj[curr] if v != prev][0]
            prev, curr = curr, nxt
            route.append(curr)
    except IndexError:
        return []

    return route if len(route) == n else []