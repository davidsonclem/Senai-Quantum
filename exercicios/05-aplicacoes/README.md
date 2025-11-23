# Exercícios - Aplicações de Computação Quântica

## Objetivos
- Explorar aplicações práticas da computação quântica
- Entender limitações atuais (era NISQ)
- Conhecer casos de uso reais

## Exercícios

### Exercício 1: Criptografia Quântica (QKD)
**Problema:** Explique o protocolo BB84 de distribuição quântica de chaves.

**Resposta:**
**BB84 (Bennett-Brassard 1984):** Primeiro protocolo de QKD.

**Princípio:** Usa propriedades quânticas para detectar espionagem.

**Etapas:**
1. Alice prepara qubits aleatórios em bases aleatórias (+/× basis)
2. Alice envia qubits para Bob através de canal quântico
3. Bob mede em bases aleatórias
4. Bob e Alice comparam bases (via canal clássico)
5. Descartam bits onde usaram bases diferentes
6. Verificam amostra para detectar espionagem
7. Restante vira chave compartilhada secreta

**Segurança:** Princípio da não-clonagem garante que espião seja detectado.

**Estados usados:**
- Base + (rectilinear): |0⟩, |1⟩
- Base × (diagonal): |+⟩, |−⟩

### Exercício 2: Simulação Quântica
**Problema:** Por que computadores quânticos são naturais para simular sistemas quânticos?

**Resposta:**
**Problema Clássico:** Simular n partículas quânticas requer 2ⁿ números complexos.
- 50 qubits = 10¹⁵ números (petabytes de memória!)
- Crescimento exponencial impossibilita simulação clássica

**Solução Quântica:** n qubits simulam n qubits naturalmente!

**Aplicações:**
1. **Química Quântica**
   - Estrutura molecular
   - Reações químicas
   - Design de medicamentos

2. **Física de Materiais**
   - Supercondutores
   - Materiais quânticos
   - Propriedades magnéticas

3. **Física de Partículas**
   - Cromodinâmica quântica (QCD)
   - Teoria de campos

**Algoritmos:** VQE, QPE, Trotterização

### Exercício 3: Otimização Quântica
**Problema:** Liste 3 problemas de otimização que podem se beneficiar de QAOA ou quantum annealing.

**Resposta:**
1. **Problema do Caixeiro Viajante (TSP)**
   - Encontrar rota mais curta visitando todas cidades
   - Aplicação: logística, roteamento

2. **Portfolio Optimization**
   - Maximizar retorno minimizando risco
   - Aplicação: finanças, investimentos

3. **Protein Folding**
   - Encontrar configuração 3D de energia mínima
   - Aplicação: biologia, drug discovery

**Outros exemplos:**
- Scheduling e alocação de recursos
- MaxCut e particionamento de grafos
- Coloração de grafos
- Satisfiability (SAT)

### Exercício 4: Machine Learning Quântico
**Problema:** O que são Quantum Neural Networks (QNN) e como diferem de redes neurais clássicas?

**Resposta:**
**QNN:** Redes neurais implementadas em circuitos quânticos parametrizados.

**Diferenças:**
1. **Representação:**
   - Clássico: Números reais
   - Quântico: Amplitudes complexas em superposição

2. **Operações:**
   - Clássico: Multiplicação de matrizes, ativações
   - Quântico: Portas quânticas parametrizadas

3. **Espaço de Estados:**
   - Clássico: Linear
   - Quântico: Exponencial (Hilbert space)

**Vantagens potenciais:**
- Espaço de features exponencial
- Emaranhamento como recurso
- Paralelismo quântico

**Desafios atuais:**
- Barren plateaus (gradientes vanishing)
- Ruído em hardware NISQ
- Carregamento de dados clássicos

**Arquiteturas:**
- Quantum Variational Classifier
- Quantum Convolutional Neural Networks
- Quantum Boltzmann Machines

### Exercício 5: Correção de Erros Quânticos
**Problema:** Por que correção de erros é crucial para computação quântica e como funciona?

**Resposta:**
**Problema:** Qubits são frágeis!
- Decoerência (perda de informação quântica)
- Ruído nas portas
- Erros de medição

**Solução:** Quantum Error Correction (QEC)

**Desafio único:** Não podemos simplesmente copiar qubits (teorema da não-clonagem)!

**Códigos de Correção:**

1. **Bit-flip code (3 qubits):**
   - Protege contra X errors
   - |0⟩ → |000⟩, |1⟩ → |111⟩

2. **Phase-flip code:**
   - Protege contra Z errors
   - Similar, mas na base |+⟩/|−⟩

3. **Shor Code (9 qubits):**
   - Protege contra X e Z errors
   - Combina bit-flip e phase-flip

4. **Surface Codes:**
   - Mais promissor para implementação
   - Qubits em grade 2D
   - Alta tolerância a erros
   - Overhead: ~1000 qubits físicos → 1 qubit lógico

**Requisito:** Taxa de erro < threshold (~1% para surface codes)

### Exercício 6: Era NISQ
**Problema:** O que caracteriza a era NISQ e quais suas limitações?

**Resposta:**
**NISQ:** Noisy Intermediate-Scale Quantum

**Características:**
- 50-1000 qubits
- Sem correção de erros completa
- Circuitos rasos (< 100 portas)
- Ruído significativo

**Limitações:**
- Não pode executar algoritmos de Shor para números úteis
- Decoerência limita profundidade de circuito
- Precisão limitada

**Estratégias para era NISQ:**
1. **Algoritmos híbridos** (VQE, QAOA)
2. **Mitigação de erros** (não correção completa)
3. **Problemas específicos** onde quantum tem vantagem mesmo com ruído
4. **Validação experimental** de conceitos

**Futuro:** Fault-tolerant quantum computing (milhões de qubits)

### Exercício 7: Supremacia/Vantagem Quântica
**Problema:** Explique a diferença entre supremacia quântica e vantagem quântica prática.

**Resposta:**
**Supremacia Quântica:**
- Computador quântico resolve problema que clássico não consegue (em tempo razoável)
- Problema pode ser artificial/sem utilidade prática
- **Exemplo:** Google (2019) - random circuit sampling em 200s vs 10,000 anos

**Vantagem Quântica Prática:**
- Computador quântico resolve problema ÚTIL melhor que clássico
- Critérios:
  - Problema relevante
  - Speedup significativo
  - Resultado verificável
  
**Status atual (2024):**
- Supremacia: ✓ Demonstrada (debatida)
- Vantagem prática: ✗ Ainda não alcançada definitivamente

**Candidatos para vantagem prática:**
- Simulação quântica de moléculas
- Otimização específica de domínio
- Machine learning em certos datasets

## Recursos Adicionais
- IBM Quantum - Use Cases
- Qiskit Applications
- Papers recentes em arXiv quant-ph
- Quantum Computing Report
