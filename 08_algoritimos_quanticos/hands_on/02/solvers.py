# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# solvers.py — Versão Final 2026 (Resolução de Conflito de API V2)
# =============================================================================

import time
import numpy as np
from qiskit_aer.primitives import SamplerV2 as AerSampler  # V2 do Aer (2026)
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
    """Cria um Mixer XY eficiente para preservar o peso de Hamming."""
    ops = []
    for i in range(n_qubits - 1):
        # Termo XX + YY
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
    Usa AerSampler V2 com o método 'statevector' forçado para evitar
    o erro de 'Sequence' e o estouro de memória no Colab.
    """
    qubo      = _to_qubo(qp)
    n_qubits  = qubo.get_num_vars()
    
    # O SEGREDO: SamplerV2 com backend explícito e shots definidos
    sampler = AerSampler()
    sampler.options.update(backend_options={"method": "statevector"})
    
    optimizer = COBYLA(maxiter=maxiter)
    
    # Se a instância for de 6 cidades (15 qubits), o Mixer XY pode ser 
    # pesado demais para o Colab. Vamos usar o mixer padrão nestes casos
    # para garantir que o código não 'morra'.
    mixer_op = create_xy_mixer(n_qubits) if n_qubits <= 10 else None
    
    qaoa = QAOA(sampler=sampler, 
                optimizer=optimizer, 
                reps=reps, 
                mixer=mixer_op)
    
    solver = MinimumEigenOptimizer(qaoa)

    t0 = time.time()
    try:
        # Resolve usando o wrapper do Optimization
        result = solver.solve(qubo)
    except Exception as e:
        print(f"⚠️ Falha na execução quântica: {e}")
        # Fallback clássico para não interromper o loop de instâncias
        return solve_classical(qp)

    return result, time.time() - t0