"""
Exemplo 4: Algoritmo de Grover
Busca em banco de dados não ordenado com speedup quadrático.
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
import numpy as np
import os
import tempfile

def grover_oracle(qc, target):
    """
    Oráculo que marca o estado alvo.
    Para 2 qubits, target pode ser '00', '01', '10', ou '11'.
    """
    # Implementar oráculo baseado no estado alvo
    if target == '00':
        qc.cz(0, 1)
        qc.x([0, 1])
        qc.cz(0, 1)
        qc.x([0, 1])
    elif target == '01':
        qc.x(0)
        qc.cz(0, 1)
        qc.x(0)
    elif target == '10':
        qc.x(1)
        qc.cz(0, 1)
        qc.x(1)
    elif target == '11':
        qc.cz(0, 1)

def grover_diffusion(qc, n_qubits):
    """
    Operador de difusão de Grover.
    """
    # Aplicar H
    qc.h(range(n_qubits))
    # Aplicar X
    qc.x(range(n_qubits))
    # Multi-controlled Z
    qc.h(n_qubits-1)
    qc.mcx(list(range(n_qubits-1)), n_qubits-1)
    qc.h(n_qubits-1)
    # Aplicar X novamente
    qc.x(range(n_qubits))
    # Aplicar H
    qc.h(range(n_qubits))

def grover_algorithm(n_qubits, target, iterations):
    """
    Implementa o algoritmo de Grover.
    """
    qc = QuantumCircuit(n_qubits, n_qubits)
    
    # Inicializar em superposição uniforme
    qc.h(range(n_qubits))
    
    # Aplicar iterações de Grover
    for _ in range(iterations):
        qc.barrier()
        # Oráculo
        grover_oracle(qc, target)
        qc.barrier()
        # Difusão
        grover_diffusion(qc, n_qubits)
    
    qc.barrier()
    # Medir
    qc.measure(range(n_qubits), range(n_qubits))
    
    return qc

# Parâmetros
n_qubits = 2
target = '11'  # Estado que queremos encontrar
N = 2**n_qubits  # Número de elementos
optimal_iterations = int(np.pi/4 * np.sqrt(N))  # ≈ 1 para N=4

print("=== ALGORITMO DE GROVER ===\n")
print(f"Número de qubits: {n_qubits}")
print(f"Tamanho do espaço de busca: {N}")
print(f"Estado alvo: |{target}⟩")
print(f"Iterações ótimas: {optimal_iterations}")

# Criar e executar circuito
qc = grover_algorithm(n_qubits, target, optimal_iterations)

print("\nCircuito:")
print(qc)

# Simular
simulator = Aer.get_backend('qasm_simulator')
job = simulator.run(qc, shots=1000)
result = job.result()
counts = result.get_counts(qc)

print("\nResultados (1000 shots):")
for state in sorted(counts.keys()):
    prob = counts[state] / 1000 * 100
    marker = " ← ALVO" if state == target else ""
    print(f"|{state}⟩: {counts[state]:4d} vezes ({prob:5.2f}%){marker}")

# Plotar
plot_histogram(counts)
plt.title(f'Algoritmo de Grover - Buscando |{target}⟩')
output_path = os.path.join(tempfile.gettempdir(), 'exemplo_04_histogram.png')
plt.savefig(output_path)
print(f"\nHistograma salvo em {output_path}")

# Explicação
print("\n=== EXPLICAÇÃO ===")
print("Algoritmo de Grover encontra elemento marcado em O(√N) queries.")
print(f"\nPara N={N} elementos:")
print(f"- Busca clássica: ~{N//2} tentativas em média, {N} no pior caso")
print(f"- Busca quântica: ~{optimal_iterations} iteração(ões)!")
print("\nO algoritmo:")
print("1. Inicia em superposição uniforme (todas as possibilidades)")
print("2. Oráculo inverte fase do estado alvo")
print("3. Difusão amplifica amplitude do estado marcado")
print("4. Após ~π/4√N iterações, probabilidade de medir alvo ≈ 100%")
print("\nSpeedup quadrático:")
print("- 4 elementos: 1 iteração vs 2 em média (clássico)")
print("- 1000000 elementos: ~785 iterações vs 500000 em média (clássico)")
