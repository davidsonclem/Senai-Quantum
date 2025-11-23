"""
Exemplo 3: Algoritmo de Deutsch-Jozsa
Demonstra vantagem quântica: determina se função é constante ou balanceada com 1 query.
"""

from qiskit import QuantumCircuit
from qiskit_aer import Aer

def deutsch_jozsa_circuit(oracle_type='constant_0'):
    """
    Cria circuito Deutsch-Jozsa para n=2 qubits.
    
    oracle_type:
    - 'constant_0': f(x) = 0 para todo x
    - 'constant_1': f(x) = 1 para todo x
    - 'balanced': f(x) é balanceada
    """
    # 2 qubits de entrada + 1 qubit auxiliar
    qc = QuantumCircuit(3, 2)
    
    # Inicializar qubit auxiliar em |1⟩
    qc.x(2)
    
    # Aplicar Hadamard em todos os qubits
    qc.h([0, 1, 2])
    
    qc.barrier()
    
    # Oráculo (implementar função)
    if oracle_type == 'constant_0':
        # f(x) = 0: não fazer nada
        pass
    elif oracle_type == 'constant_1':
        # f(x) = 1: aplicar Z no auxiliar
        qc.z(2)
    elif oracle_type == 'balanced':
        # Exemplo: f(x) = x₀ ⊕ x₁
        qc.cx(0, 2)
        qc.cx(1, 2)
    
    qc.barrier()
    
    # Aplicar Hadamard nos qubits de entrada
    qc.h([0, 1])
    
    # Medir qubits de entrada
    qc.measure([0, 1], [0, 1])
    
    return qc

# Testar diferentes tipos de função
print("=== ALGORITMO DE DEUTSCH-JOZSA ===\n")

for oracle_type in ['constant_0', 'constant_1', 'balanced']:
    print(f"\nTestando com oráculo: {oracle_type}")
    print("-" * 50)
    
    qc = deutsch_jozsa_circuit(oracle_type)
    
    # Simular
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)
    
    print(f"Resultados: {counts}")
    
    # Interpretar resultado
    if '00' in counts and counts['00'] > 900:
        print("✓ Função é CONSTANTE")
    else:
        print("✓ Função é BALANCEADA")

# Mostrar um dos circuitos
print("\n=== CIRCUITO (oráculo balanceado) ===")
qc = deutsch_jozsa_circuit('balanced')
print(qc)

# Explicação
print("\n=== EXPLICAÇÃO ===")
print("Algoritmo de Deutsch-Jozsa resolve o problema com apenas 1 query!")
print("Classicamente, seria necessário até 2^(n-1) + 1 queries no pior caso.")
print("\nInterpretação:")
print("- Medir |00⟩ → função é CONSTANTE")
print("- Qualquer outro resultado → função é BALANCEADA")
print("\nVantagem quântica:")
print("- n=2: 1 query (quântico) vs até 3 queries (clássico)")
print("- n=10: 1 query (quântico) vs até 513 queries (clássico)")
print("- n=100: 1 query (quântico) vs até 2^99 + 1 queries (clássico)!!")
