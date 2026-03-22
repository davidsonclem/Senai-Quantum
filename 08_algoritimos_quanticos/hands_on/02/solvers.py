# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# solvers.py — Solvers clássico (NumPy) e quântico (QAOA)
# =============================================================================

import time
from qiskit.primitives import StatevectorSampler
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_algorithms import QAOA, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA

from config import QAOA_REPS, QAOA_MAXITER


def solve_classical(qubo):
    """Resolve o QUBO via NumPyMinimumEigensolver (solver exato clássico).

    Args:
        qubo: Problema QUBO gerado por build_qubo().

    Returns:
        Tuple (resultado, tempo_segundos).
    """
    solver = MinimumEigenOptimizer(NumPyMinimumEigensolver())
    t0     = time.time()
    result = solver.solve(qubo)
    return result, time.time() - t0


def solve_qaoa(qubo, reps: int = QAOA_REPS, maxiter: int = QAOA_MAXITER):
    """Resolve o QUBO usando o algoritmo QAOA variacional.

    Utiliza StatevectorSampler (V2), compatível com qiskit-algorithms >= 0.3.
    O sampler é criado localmente para evitar estado global entre chamadas.

    Args:
        qubo:    Problema QUBO gerado por build_qubo().
        reps:    Número de camadas QAOA (padrão: QAOA_REPS de config.py).
        maxiter: Iterações do otimizador COBYLA (padrão: QAOA_MAXITER).

    Returns:
        Tuple (resultado, tempo_segundos).

    Nota de performance:
        Para n >= 5 cidades, considere substituir StatevectorSampler por
        AerSampler(method='matrix_product_state') — consome menos memória
        pois não mantém o vetor de estado completo (2^n² amplitudes).
    """
    sampler   = StatevectorSampler()
    optimizer = COBYLA(maxiter=maxiter)
    qaoa      = QAOA(sampler=sampler, optimizer=optimizer, reps=reps)
    solver    = MinimumEigenOptimizer(qaoa)

    t0     = time.time()
    result = solver.solve(qubo)
    return result, time.time() - t0
