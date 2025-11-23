# Exercícios - Portas Quânticas

## Objetivos
- Compreender as principais portas quânticas
- Calcular o efeito de portas em estados quânticos
- Entender a reversibilidade das operações quânticas

## Exercícios

### Exercício 1: Porta Pauli-X
**Problema:** Aplique a porta X (NOT quântica) nos seguintes estados:
1. X|0⟩ = ?
2. X|1⟩ = ?
3. X|+⟩ = ?

**Resposta:**
Matriz X = [[0, 1], [1, 0]]
1. X|0⟩ = |1⟩
2. X|1⟩ = |0⟩
3. X|+⟩ = X(|0⟩ + |1⟩)/√2 = (|1⟩ + |0⟩)/√2 = |+⟩

### Exercício 2: Porta Hadamard
**Problema:** A porta Hadamard cria superposição. Calcule:
1. H|0⟩ = ?
2. H|1⟩ = ?
3. H(H|0⟩) = ?

**Resposta:**
Matriz H = (1/√2)[[1, 1], [1, -1]]
1. H|0⟩ = |+⟩ = (|0⟩ + |1⟩)/√2
2. H|1⟩ = |−⟩ = (|0⟩ − |1⟩)/√2
3. H(H|0⟩) = H|+⟩ = |0⟩ (a porta H é sua própria inversa)

### Exercício 3: Porta Pauli-Z
**Problema:** Aplique a porta Z nos estados:
1. Z|0⟩ = ?
2. Z|1⟩ = ?
3. Z|+⟩ = ?

**Resposta:**
Matriz Z = [[1, 0], [0, -1]]
1. Z|0⟩ = |0⟩
2. Z|1⟩ = −|1⟩
3. Z|+⟩ = Z(|0⟩ + |1⟩)/√2 = (|0⟩ − |1⟩)/√2 = |−⟩

### Exercício 4: Porta CNOT
**Problema:** A porta CNOT é uma porta de 2 qubits. Calcule:
1. CNOT|00⟩ = ?
2. CNOT|01⟩ = ?
3. CNOT|10⟩ = ?
4. CNOT|11⟩ = ?

**Resposta:**
CNOT inverte o segundo qubit (target) se o primeiro (control) for |1⟩:
1. CNOT|00⟩ = |00⟩
2. CNOT|01⟩ = |01⟩
3. CNOT|10⟩ = |11⟩
4. CNOT|11⟩ = |10⟩

### Exercício 5: Portas de Fase
**Problema:** Explique a diferença entre as portas S e T.

**Resposta:**
- Porta S (fase de π/2): S = [[1, 0], [0, i]]
  - S|0⟩ = |0⟩
  - S|1⟩ = i|1⟩

- Porta T (fase de π/4): T = [[1, 0], [0, e^(iπ/4)]]
  - T|0⟩ = |0⟩
  - T|1⟩ = e^(iπ/4)|1⟩

A porta S adiciona fase de 90°, enquanto T adiciona fase de 45°.

### Exercício 6: Composição de Portas
**Problema:** Mostre que S = T²

**Resposta:**
T² = T·T
e^(iπ/4) · e^(iπ/4) = e^(iπ/2) = i
Portanto, T²|1⟩ = i|1⟩ = S|1⟩ ✓

### Exercício 7: Criando Emaranhamento
**Problema:** Descreva como criar um estado de Bell usando H e CNOT.

**Resposta:**
Sequência: H ⊗ I → CNOT
1. Estado inicial: |00⟩
2. Após H no primeiro qubit: (|0⟩ + |1⟩)/√2 ⊗ |0⟩ = (|00⟩ + |10⟩)/√2
3. Após CNOT: (|00⟩ + |11⟩)/√2 = |Φ⁺⟩ (estado de Bell)

## Recursos Adicionais
- Tabela de portas quânticas comuns
- Qiskit documentation - Quantum Gates
