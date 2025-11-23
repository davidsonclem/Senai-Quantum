# Exercícios - Fundamentos de Computação Quântica

## Objetivos
- Compreender os conceitos básicos de computação quântica
- Familiarizar-se com a notação matemática
- Entender qubits, superposição e emaranhamento

## Exercícios

### Exercício 1: Notação de Dirac
**Problema:** Escreva os seguintes estados quânticos na notação de Dirac (bra-ket):
1. Um qubit no estado |0⟩
2. Um qubit no estado |1⟩
3. Um qubit em superposição igual (|0⟩ + |1⟩)/√2

**Resposta:**
1. |0⟩ = [1, 0]ᵀ
2. |1⟩ = [0, 1]ᵀ
3. |+⟩ = (|0⟩ + |1⟩)/√2 = [1/√2, 1/√2]ᵀ

### Exercício 2: Probabilidades
**Problema:** Dado um qubit no estado |ψ⟩ = (3|0⟩ + 4|1⟩)/5:
1. Este estado está normalizado?
2. Qual a probabilidade de medir |0⟩?
3. Qual a probabilidade de medir |1⟩?

**Resposta:**
1. Sim, pois |3/5|² + |4/5|² = 9/25 + 16/25 = 1
2. P(|0⟩) = |3/5|² = 9/25 = 0.36 = 36%
3. P(|1⟩) = |4/5|² = 16/25 = 0.64 = 64%

### Exercício 3: Superposição
**Problema:** Explique o conceito de superposição quântica e dê um exemplo prático.

**Resposta:**
Superposição é a capacidade de um qubit estar simultaneamente em múltiplos estados. Diferente de um bit clássico (0 ou 1), um qubit pode estar em uma combinação linear de |0⟩ e |1⟩.

Exemplo: O estado |+⟩ = (|0⟩ + |1⟩)/√2 representa um qubit com 50% de probabilidade de ser medido como 0 ou 1.

### Exercício 4: Sistemas de 2 Qubits
**Problema:** Quantos estados de base existem em um sistema de 2 qubits? Liste-os.

**Resposta:**
Existem 4 estados de base (2² = 4):
- |00⟩
- |01⟩
- |10⟩
- |11⟩

### Exercício 5: Emaranhamento
**Problema:** O que é um estado emaranhado? Dê um exemplo de um estado de Bell.

**Resposta:**
Um estado emaranhado é aquele que não pode ser escrito como produto tensorial de estados individuais. Os qubits estão correlacionados de forma não-clássica.

Exemplo de estado de Bell (EPR pair):
|Φ⁺⟩ = (|00⟩ + |11⟩)/√2

Este estado não pode ser escrito como |ψ₁⟩ ⊗ |ψ₂⟩ para nenhum par de estados de qubit único.

## Recursos Adicionais
- Nielsen & Chuang - "Quantum Computation and Quantum Information"
- IBM Quantum Learning
- Qiskit Textbook
