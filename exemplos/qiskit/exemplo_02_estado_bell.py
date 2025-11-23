"""
Exemplo 2: Estado de Bell (Emaranhamento)
Demonstra criação de um par EPR emaranhado.
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# Criar circuito com 2 qubits e 2 bits clássicos
qc = QuantumCircuit(2, 2)

# Criar estado de Bell |Φ⁺⟩ = (|00⟩ + |11⟩)/√2
# Passo 1: Aplicar Hadamard no qubit 0
qc.h(0)

# Passo 2: Aplicar CNOT com controle no qubit 0 e alvo no qubit 1
qc.cx(0, 1)

# Adicionar barreira para visualização
qc.barrier()

# Medir ambos os qubits
qc.measure([0, 1], [0, 1])

# Desenhar o circuito
print("Circuito para Estado de Bell:")
print(qc)

# Simular
simulator = Aer.get_backend('qasm_simulator')
job = simulator.run(qc, shots=1000)
result = job.result()
counts = result.get_counts(qc)

print("\nResultados da medição (1000 shots):")
print(counts)

# Plotar
plot_histogram(counts)
plt.title('Estado de Bell - Qubits Emaranhados')
plt.savefig('/tmp/exemplo_02_histogram.png')
print("\nHistograma salvo em /tmp/exemplo_02_histogram.png")

# Explicação
print("\n=== EXPLICAÇÃO ===")
print("Estado de Bell: |Φ⁺⟩ = (|00⟩ + |11⟩)/√2")
print("Os qubits estão emaranhados!")
print("Características:")
print("- Se medirmos '00', ambos qubits são 0")
print("- Se medirmos '11', ambos qubits são 1")
print("- Nunca medimos '01' ou '10'")
print("- Os qubits estão perfeitamente correlacionados")
print("- Resultado esperado: ~50% '00' e ~50% '11'")

# Verificar correlação
print("\n=== VERIFICAÇÃO DA CORRELAÇÃO ===")
total = sum(counts.values())
prob_00 = counts.get('00', 0) / total * 100
prob_11 = counts.get('11', 0) / total * 100
prob_01 = counts.get('01', 0) / total * 100
prob_10 = counts.get('10', 0) / total * 100

print(f"P(00) = {prob_00:.2f}%")
print(f"P(11) = {prob_11:.2f}%")
print(f"P(01) = {prob_01:.2f}%")
print(f"P(10) = {prob_10:.2f}%")
