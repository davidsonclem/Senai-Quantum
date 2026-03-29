# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# solvers.py — Solvers clássico (NumPy) e quântico (QAOA)
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
    """Resolve o problema via NumPyMinimumEigensolver (solver exato clássico)."""
    qubo   = _to_qubo(qp)
    solver = MinimumEigenOptimizer(NumPyMinimumEigensolver())
    t0     = time.time()
    result = solver.solve(qubo)
    return result, time.time() - t0

def solve_qaoa(qp, reps: int = QAOA_REPS, maxiter: int = QAOA_MAXITER):
    """Resolve o problema usando QAOA com StatevectorSampler (V2)."""
    qubo      = _to_qubo(qp)
    
    # SEU CÓDIGO ORIGINAL: Limpo e sem conflitos de API
    sampler   = StatevectorSampler()
    optimizer = COBYLA(maxiter=maxiter)
    qaoa      = QAOA(sampler=sampler, optimizer=optimizer, reps=reps)
    solver    = MinimumEigenOptimizer(qaoa)

    t0 = time.time()
    try:
        # Tenta executar. Se faltar RAM (ex: 6 cidades / 15 qubits = 17GB), ele captura
        result = solver.solve(qubo)
        return result, time.time() - t0
    except MemoryError:
        raise RuntimeError("Estouro de Memória: A matriz densa excedeu os 16GB de RAM do Colab.")
    except Exception as e:
        raise RuntimeError(f"Erro na execução quântica: {e}")