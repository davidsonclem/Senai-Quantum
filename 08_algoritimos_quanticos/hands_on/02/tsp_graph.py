# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# tsp_graph.py — Modelagem do grafo e conversão para QUBO
# =============================================================================

import numpy as np
import networkx as nx
from qiskit_optimization.applications import Tsp
from qiskit_optimization.converters import QuadraticProgramToQubo


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


def build_qubo(w: list[list[int]]):
    """Converte a matriz de adjacência em um problema QUBO via Qiskit.

    Encapsula a sequência: matriz → Tsp → QuadraticProgram → QUBO.
    Retorna também o objeto Tsp para posterior interpretação da solução.

    Args:
        w: Matriz de adjacência N×N.

    Returns:
        Tuple (tsp, qubo) prontos para uso nos solvers.
    """
    tsp_problem = Tsp(np.array(w))
    qp          = tsp_problem.to_quadratic_program()
    converter   = QuadraticProgramToQubo()
    qubo        = converter.convert(qp)
    return tsp_problem, qubo
