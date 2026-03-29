# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# solvers.py — Versão Otimizada para Google Colab (AerSampler + MPS)
# =============================================================================

import time
import numpy as np
from qiskit_aer.primitives import Sampler as AerSampler  # Otimizado para RAM
from qiskit.quantum_info import SparsePauliOp
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_algorithms import QAOA, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA

from config import QAOA_REPS, QAOA_MAXITER

_converter = QuadraticProgramToQubo()

def _to_qubo(qp):
    """Converte QuadraticProgram para QUBO."""
    return _converter.convert(qp)

def create_xy_mixer(n_qubits):
    """
    Cria um Mixer XY (Parity-Preserving).
    Implementa a soma de operadores (XX + YY) entre qubits vizinhos lineares.
    """
    ops = []
    for i in range(n_qubits - 1):
        # Termo XX
        x_list = ["I"] * n_qubits
        x_list[i] = "X"
        x_list[i+1] = "X"
        ops.append(("".join(x_list[::-1]), 0.5))
        
        # Termo YY
        y_list = ["I"] * n_qubits
        y_list[i] = "Y"
        y_list[i+1] = "Y"
        ops.append(("".join(y_list[::-1]), 0.5))
        
    return SparsePauliOp.from_list(ops)

def solve_classical(qp):
    """Resolve o problema via NumPyMinimumEigensolver (exato)."""
    qubo   = _to_qubo(qp)
    solver = MinimumEigenOptimizer(NumPyMinimumEigensolver())
    t0     = time.time()
    result = solver.solve(qubo)
    return result, time.time() - t0

def solve_qaoa(qp, reps: int = QAOA_REPS, maxiter: int = QAOA_MAXITER):
    qubo = _to_qubo(qp)
    
    # Usando o Sampler padrão do Aer para maior estabilidade no Colab
    from qiskit_aer.primitives import Sampler as AerSampler
    sampler = AerSampler() 
    
    optimizer = COBYLA(maxiter=maxiter)
    
    # TESTE DE ESTABILIDADE: Comente o Mixer XY e use o padrão (None)
    # mixer_op = create_xy_mixer(n_qubits)
    
    qaoa = QAOA(sampler=sampler, 
                optimizer=optimizer, 
                reps=reps, 
                mixer=None) # Mixer padrão X
    
    solver = MinimumEigenOptimizer(qaoa)
    t0 = time.time()
    result = solver.solve(qubo)
    return result, time.time() - t0