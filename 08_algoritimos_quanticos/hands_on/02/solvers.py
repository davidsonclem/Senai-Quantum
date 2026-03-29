# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# solvers.py — Versão Final Ajustada para Google Colab (Qiskit 1.x/2.0)
# =============================================================================

import time
import numpy as np
from qiskit_aer.primitives import Sampler as AerSampler  # Primitiva otimizada
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
    Ajuda a manter o peso de Hamming (número de arestas ligadas).
    """
    ops = []
    # Conectividade linear para o mixer (i -> i+1)
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
    """
    Resolve o TSP usando QAOA com Mixer XY e AerSampler.
    Ajustado para evitar erros de 'Invalid circuits' e estouro de memória.
    """
    qubo      = _to_qubo(qp)
    n_qubits  = qubo.get_num_vars() 
    
    # 1. Usar AerSampler com backend explícito (Statevector)
    # O método 'statevector' é o mais estável para até 15 qubits no Colab
    sampler = AerSampler(run_options={"method": "statevector", "shots": 1024})
    
    # 2. Configurar o otimizador clássico
    optimizer = COBYLA(maxiter=maxiter)
    
    # 3. Criar o Mixer XY customizado
    mixer_op = create_xy_mixer(n_qubits)
    
    # 4. Configurar o QAOA com o Sampler do Aer
    qaoa = QAOA(sampler=sampler, 
                optimizer=optimizer, 
                reps=reps, 
                mixer=mixer_op)
    
    # 5. Resolver via Optimization Wrapper
    solver = MinimumEigenOptimizer(qaoa)

    t0     = time.time()
    result = solver.solve(qubo)
    return result, time.time() - t0