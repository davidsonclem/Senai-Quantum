"""
Exemplo 1: Circuito Quântico Básico
Demonstra criação de um circuito simples com porta Hadamard e medição.
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Criar um circuito quântico com 1 qubit e 1 bit clássico
qc = QuantumCircuit(1, 1)

# Adicionar porta Hadamard (cria superposição)
qc.h(0)

# Medir o qubit
qc.measure(0, 0)

# Desenhar o circuito
print("Circuito Quântico:")
print(qc)

# Simular o circuito
simulator = Aer.get_backend('qasm_simulator')
job = simulator.run(qc, shots=1000)
result = job.result()

# Obter contagens
counts = result.get_counts(qc)
print("\nResultados da medição (1000 shots):")
print(counts)

# Plotar histograma
plot_histogram(counts)
plt.title('Distribuição de Medições - Superposição')
plt.savefig('/tmp/exemplo_01_histogram.png')
print("\nHistograma salvo em /tmp/exemplo_01_histogram.png")

# Explicação
print("\n=== EXPLICAÇÃO ===")
print("Inicialmente o qubit está em |0⟩")
print("Após a porta Hadamard: |+⟩ = (|0⟩ + |1⟩)/√2")
print("Ao medir, colapsamos para |0⟩ ou |1⟩ com 50% de probabilidade cada")
print(f"Resultado esperado: ~500 medições de '0' e ~500 de '1'")
