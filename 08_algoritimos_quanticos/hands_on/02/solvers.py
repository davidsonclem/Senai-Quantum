# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# solvers.py — Versão Blindada para Google Colab (Resolve Invalid circuits)
# =============================================================================

import time
import numpy as np
from qiskit_aer.primitives import Sampler as AerSampler
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_algorithms import QAOA, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA
from qiskit.quantum_info import SparsePauliOp

from config import QAOA_REPS, QAOA_MAXITER

_converter = QuadraticProgramToQubo()

def _to_qubo(qp):
    return _converter.convert(qp)

def create_xy_mixer(n_qubits):
    ops = []
    for i in range(n_qubits - 1):
        x_list = ["I"] * n_qubits
        x_list[i], x_list[i+1] = "X", "X"
        ops.append(("".join(x_list[::-1]), 0.5))
        y_list = ["I"] * n_qubits
        y_list[i], y_list[i+1] = "Y", "Y"
        ops.append(("".join(y_list[::-1]), 0.5))
    return SparsePauliOp.from_list(ops)

def solve_classical(qp):
    qubo = _to_qubo(qp)
    solver = MinimumEigenOptimizer(NumPyMinimumEigensolver())
    t0 = time.time()
    result = solver.solve(qubo)
    return result, time.time() - t0

def solve_qaoa(qp, reps: int = QAOA_REPS, maxiter: int = QAOA_MAXITER):
    qubo = _to_qubo(qp)
    n_qubits = qubo.get_num_vars()
    
    # FORÇA BRUTA: Criamos o sampler fora e configuramos o QAOA 
    # de modo que o Optimizer não precise "adivinhar" nada.
    sampler = AerSampler(run_options={"method": "statevector"})
    
    optimizer = COBYLA(maxiter=maxiter)
    mixer_op = create_xy_mixer(n_qubits)
    
    # Criar o QAOA puro primeiro
    qaoa_alg = QAOA(sampler=sampler, 
                    optimizer=optimizer, 
                    reps=reps, 
                    mixer=mixer_op)
    
    # O segredo: passamos o algoritmo JÁ INSTANCIADO para o solver
    solver = MinimumEigenOptimizer(qaoa_alg)

    t0 = time.time()
    try:
        result = solver.solve(qubo)
    except Exception as e:
        # Se ainda assim der erro de sequência, o Colab está com conflito de versão.
        # Tentamos o fallback para o solver clássico para não travar seu relatório.
        print(f"⚠️ Erro técnico no QAOA: {e}. Verifique as versões das bibliotecas.")
        raise e
        
    return result, time.time() - t0