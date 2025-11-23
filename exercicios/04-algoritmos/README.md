# Exercícios - Algoritmos Quânticos

## Objetivos
- Compreender algoritmos quânticos clássicos
- Analisar a complexidade e vantagem quântica
- Implementar algoritmos básicos

## Exercícios

### Exercício 1: Algoritmo de Deutsch-Jozsa
**Problema:** Explique o problema que o algoritmo de Deutsch-Jozsa resolve e por que ele demonstra vantagem quântica.

**Resposta:**
**Problema:** Determinar se uma função booleana f: {0,1}ⁿ → {0,1} é constante (sempre 0 ou sempre 1) ou balanceada (metade 0, metade 1).

**Solução Clássica:** Requer até 2ⁿ⁻¹ + 1 avaliações no pior caso.

**Solução Quântica:** Apenas 1 avaliação!

**Circuito (n=1):**
```
     ┌───┐┌─────┐┌───┐┌─┐
q_0: ┤ H ├┤     ├┤ H ├┤M├
     ├───┤│ Uf  │└───┘└╥┘
q_1: ┤ X ├┤     ├──────╫─
     └───┘└─────┘      ║
c: 1/═══════════════════╩═
```

Se medir |0⟩ → função constante
Se medir |1⟩ → função balanceada

### Exercício 2: Algoritmo de Grover
**Problema:** O algoritmo de Grover busca em um banco de dados não ordenado. Qual a complexidade?

**Resposta:**
**Problema:** Encontrar um elemento marcado em uma lista de N elementos não ordenados.

**Complexidade Clássica:** O(N) - busca linear
**Complexidade Quântica:** O(√N) - speedup quadrático!

**Componentes principais:**
1. Inicialização em superposição uniforme (H⊗ⁿ)
2. Oráculo: marca o estado alvo com fase negativa
3. Difusão: amplifica amplitude do estado marcado
4. Repetir √N vezes
5. Medir

**Número de iterações:** ≈ (π/4)√N

### Exercício 3: Transformada de Fourier Quântica (QFT)
**Problema:** Explique a importância da QFT e sua complexidade.

**Resposta:**
**QFT:** Análogo quântico da Transformada de Fourier Discreta (DFT).

**Aplicação:** |x⟩ → (1/√N) Σⱼ e^(2πixj/N) |j⟩

**Complexidade:**
- DFT Clássica: O(N log N) com FFT
- QFT: O(log² N) - exponencialmente mais rápida!

**Uso:** Componente essencial do algoritmo de Shor e estimativa de fase.

**Circuito (3 qubits):**
```
q_0: ─H─S─T─────────────×─
        │  │             │
q_1: ───■──┼──H─S────────×─
           │    │        │
q_2: ──────■────■──H─────×─
```

### Exercício 4: Algoritmo de Shor (Conceitual)
**Problema:** Descreva o problema que o algoritmo de Shor resolve e sua importância.

**Resposta:**
**Problema:** Fatorar números inteiros grandes N em seus fatores primos.

**Importância:** Quebra criptografia RSA (baseada na dificuldade de fatoração)!

**Complexidade:**
- Clássico: Sub-exponencial, mas muito lento para números grandes
- Quântico: O(log³ N) - exponencialmente mais rápido

**Etapas principais:**
1. Escolher a < N aleatório, coprimo com N
2. Usar QPE (Quantum Phase Estimation) para encontrar período r de aˣ mod N
3. Se r é par e aʳ/² ≠ -1 (mod N), calcular:
   - p = gcd(aʳ/² - 1, N)
   - q = gcd(aʳ/² + 1, N)
4. Verificar se p e q são fatores não-triviais de N

**Componente quântico:** Estimativa de fase usando QFT

### Exercício 5: Variational Quantum Eigensolver (VQE)
**Problema:** O que é VQE e para que serve?

**Resposta:**
**VQE:** Algoritmo híbrido quântico-clássico para encontrar o autovalor mínimo (energia fundamental) de um Hamiltoniano.

**Aplicações:**
- Química quântica (estrutura molecular)
- Ciência dos materiais
- Otimização

**Como funciona:**
1. Preparar estado quântico parametrizado |ψ(θ)⟩
2. Medir energia ⟨ψ(θ)|H|ψ(θ)⟩ no computador quântico
3. Otimizar θ classicamente para minimizar energia
4. Iterar até convergência

**Vantagem:** Adequado para computadores quânticos NISQ (Noisy Intermediate-Scale Quantum)

### Exercício 6: QAOA (Quantum Approximate Optimization Algorithm)
**Problema:** Explique QAOA e um problema que ele pode resolver.

**Resposta:**
**QAOA:** Algoritmo para problemas de otimização combinatória.

**Exemplo - MaxCut:**
Dado um grafo, particionar vértices em 2 grupos maximizando arestas entre grupos.

**Estrutura:**
1. Estado inicial: superposição uniforme
2. Aplicar p camadas de:
   - Hamiltoniano de problema (fase)
   - Hamiltoniano de mistura (superposição)
3. Medir e avaliar custo
4. Otimizar parâmetros classicamente

**Circuito (simplificado):**
```
Para cada camada p:
- Aplicar e^(-iγH_C) (problema)
- Aplicar e^(-iβH_M) (mistura)
```

### Exercício 7: Amplitude Amplification
**Problema:** Como a amplificação de amplitude generaliza o algoritmo de Grover?

**Resposta:**
**Amplificação de Amplitude:** Técnica genérica para amplificar a probabilidade de estados "bons" em superposição.

**Grover é caso especial:** quando há apenas um estado bom.

**Generalização:**
- Funciona com múltiplos estados bons
- Pode ser aplicada a saídas de outros algoritmos quânticos
- Speedup de O(1/√a) onde a é fração de estados bons

**Operadores:**
1. A: Prepara superposição (inclui estados bons)
2. S₀: Reflexão sobre |0⟩
3. Sψ: Reflexão sobre |ψ⟩
4. Q = -ASₐA⁻¹S₀ (operador de Grover)

## Recursos Adicionais
- Qiskit Textbook - Quantum Algorithms
- Quantum Algorithm Zoo (quantumalgorithmzoo.org)
- Nielsen & Chuang - Capítulos sobre algoritmos
