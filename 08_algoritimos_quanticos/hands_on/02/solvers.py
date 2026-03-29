# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# solvers.py — Solvers clássico (NumPy) e quântico (QAOA)
# =============================================================================
#
# Compatibilidade: Python 3.14 + qiskit >= 1.0 + qiskit-algorithms >= 0.3
#
# O AerSampler (V1) não é compatível com qiskit-algorithms >= 0.3 que espera
# a interface V2. A solução é usar StatevectorSampler (V2 nativo) com o
# wrapper de compatibilidade StatevectorSamplerV1 quando necessário.
#
# Com a modelagem edge-based o número de qubits é pequeno o suficiente para
# o StatevectorSampler rodar bem mesmo em 16 GB RAM:
#   n=3 →  3 qubits  n=4 →  6 qubits  n=5 → 10 qubits  n=6 → 15 qubits
# =============================================================================

import time
from qiskit.primitives import StatevectorSampler
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_algorithms import QAOA, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA

from config import QAOA_REPS, QAOA_MAXITER

_converter = QuadraticProgramToQubo()


def _to_qubo(qp):
    """Converte QuadraticProgram para QUBO."""
    return _converter.convert(qp)


def solve_classical(qp):
    """Resolve o problema via NumPyMinimumEigensolver (solver exato clássico).

    Args:
        qp: QuadraticProgram gerado por build_qubo().

    Returns:
        Tuple (resultado, tempo_segundos).
    """
    qubo   = _to_qubo(qp)
    solver = MinimumEigenOptimizer(NumPyMinimumEigensolver())
    t0     = time.time()
    result = solver.solve(qubo)
    return result, time.time() - t0


def solve_qaoa(qp, reps: int = QAOA_REPS, maxiter: int = QAOA_MAXITER):
    """Resolve o problema usando QAOA com StatevectorSampler (V2).

    Seguro para Python 3.14 + qiskit >= 1.0. Com a modelagem edge-based
    o número de qubits é reduzido o suficiente para rodar em 16 GB RAM.

    Args:
        qp:      QuadraticProgram gerado por build_qubo().
        reps:    Número de camadas QAOA.
        maxiter: Iterações do otimizador COBYLA.

    Returns:
        Tuple (resultado, tempo_segundos).
    """
    qubo      = _to_qubo(qp)
    sampler   = StatevectorSampler()
    optimizer = COBYLA(maxiter=maxiter)
    qaoa      = QAOA(sampler=sampler, optimizer=optimizer, reps=reps)
    solver    = MinimumEigenOptimizer(qaoa)

    t0     = time.time()
    result = solver.solve(qubo)
    return result, time.time() - t0
