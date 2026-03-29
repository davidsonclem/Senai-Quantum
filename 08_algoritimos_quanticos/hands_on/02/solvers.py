# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# solvers.py — Versão Blindada para Google Colab (Resolve Invalid circuits)
# =============================================================================

import time
import numpy as np
from qiskit_aer.primitives import Sampler as AerSampler
from qiskit.quantum_info import SparsePauliOp
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_algorithms import QAOA, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA

from config import QAOA_REPS, QAOA_MAXITER

_converter = QuadraticProgramToQubo()

def _to_qubo(qp):
    return _converter.convert(qp)

def create_xy_mixer(n_qubits):
    """Cria um Mixer XY (Parity-Preserving) para manter o peso de Hamming."""
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
    qubo   = _to_qubo(qp)
    solver = MinimumEigenOptimizer(NumPyMinimumEigensolver())
    t0     = time.time()
    result = solver.solve(qubo)
    return result, time.time() - t0

def solve_qaoa(qp, reps: int = QAOA_REPS, maxiter: int = QAOA_MAXITER):
    """
    Versão corrigida: Usa AerSampler diretamente no QAOA para evitar
    erros de validação de sequência de circuitos no Colab.
    """
    qubo      = _to_qubo(qp)
    n_qubits  = qubo.get_num_vars() 
    
    # 1. Definimos o Sampler do Aer com configurações de segurança
    sampler = AerSampler(run_options={"method": "statevector", "shots": 1024})
    
    # 2. Otimizador com limite de iterações para o Colab não travar
    optimizer = COBYLA(maxiter=maxiter)
    
    # 3. Mixer XY (importante para o TSP edge-based)
    mixer_op = create_xy_mixer(n_qubits)
    
    # 4. Instanciamos o QAOA passando o sampler OTIMIZADO
    qaoa = QAOA(sampler=sampler, 
                optimizer=optimizer, 
                reps=reps, 
                mixer=mixer_op)
    
    # 5. O wrapper de otimização agora receberá o QAOA já configurado
    solver = MinimumEigenOptimizer(qaoa)

    t0     = time.time()
    result = solver.solve(qubo)
    return result, time.time() - t0