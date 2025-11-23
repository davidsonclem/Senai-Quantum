# Exercícios - Circuitos Quânticos

## Objetivos
- Desenhar e analisar circuitos quânticos
- Entender a ordem de operações
- Calcular resultados de medições

## Exercícios

### Exercício 1: Circuito Simples
**Problema:** Desenhe um circuito que:
1. Inicializa um qubit em |0⟩
2. Aplica uma porta H
3. Mede o qubit

Qual a probabilidade de cada resultado?

**Resposta:**
```
     ┌───┐┌─┐
q_0: ┤ H ├┤M├
     └───┘└╥┘
c: 1/══════╩═
           0
```
Estado após H: |+⟩ = (|0⟩ + |1⟩)/√2
P(0) = 50%, P(1) = 50%

### Exercício 2: Estado de Bell
**Problema:** Construa um circuito que cria o estado |Φ⁺⟩ = (|00⟩ + |11⟩)/√2

**Resposta:**
```
     ┌───┐     
q_0: ┤ H ├──■──
     └───┘┌─┴─┐
q_1: ─────┤ X ├
          └───┘
```
1. H no q_0: (|0⟩ + |1⟩)/√2 ⊗ |0⟩
2. CNOT: (|00⟩ + |11⟩)/√2

### Exercício 3: Circuito com 3 Qubits
**Problema:** Crie um circuito que aplica H em todos os 3 qubits. Quantos estados possíveis existem após a medição?

**Resposta:**
```
     ┌───┐
q_0: ┤ H ├
     ├───┤
q_1: ┤ H ├
     ├───┤
q_2: ┤ H ├
     └───┘
```
Estado final: |+⟩⊗³ = (1/2√2)(|000⟩ + |001⟩ + |010⟩ + |011⟩ + |100⟩ + |101⟩ + |110⟩ + |111⟩)
8 estados possíveis, cada um com probabilidade 1/8 = 12.5%

### Exercício 4: Teleporte Quântico (Conceitual)
**Problema:** Descreva os passos principais do protocolo de teleporte quântico.

**Resposta:**
1. Criar par EPR entre Alice e Bob: (|00⟩ + |11⟩)/√2
2. Alice tem o qubit a ser teleportado: α|0⟩ + β|1⟩
3. Alice aplica CNOT entre seu qubit e sua metade do par EPR
4. Alice aplica H no qubit original
5. Alice mede seus 2 qubits (4 resultados possíveis)
6. Alice envia 2 bits clássicos para Bob
7. Bob aplica correções baseadas nos bits recebidos
8. Bob agora tem o estado α|0⟩ + β|1⟩

### Exercício 5: Medição Parcial
**Problema:** Dado o estado emaranhado (|00⟩ + |11⟩)/√2, se medirmos apenas o primeiro qubit e obtivermos 0, qual o estado do segundo qubit?

**Resposta:**
Estado inicial: (|00⟩ + |11⟩)/√2

Medindo q_0 = 0:
- A probabilidade é |⟨0|√2⟩|² para o termo |00⟩ = 1/2
- Após medir 0, o estado colapsa para |00⟩
- Portanto, q_1 está definitivamente em |0⟩

Se tivéssemos medido q_0 = 1, q_1 estaria em |1⟩.

### Exercício 6: Reversibilidade
**Problema:** Todo circuito quântico (sem medição) é reversível. Construa o circuito inverso de:
```
q_0: ──H──■──T──
          │
q_1: ─────X─────
```

**Resposta:**
Circuito inverso (ordem reversa, portas inversas):
```
q_0: ──T†──■───H──
           │
q_1: ──────X──────
```
Nota: T† = T³, X e H são suas próprias inversas.

### Exercício 7: Circuito GHZ
**Problema:** Crie um circuito que gera o estado GHZ em 3 qubits: (|000⟩ + |111⟩)/√2

**Resposta:**
```
     ┌───┐          
q_0: ┤ H ├──■────■──
     └───┘┌─┴─┐  │  
q_1: ─────┤ X ├──┼──
          └───┘┌─┴─┐
q_2: ──────────┤ X ├
               └───┘
```

## Recursos Adicionais
- Qiskit Circuit Library
- Quantum Circuit Simulator
- Quantum Algorithm Zoo
