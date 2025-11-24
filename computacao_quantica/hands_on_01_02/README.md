# Hands-On: Circuitos Quânticos e Visualização de Estados

![Status](https://img.shields.io/badge/Status-Concluído-green)
![Course](https://img.shields.io/badge/Curso-Especialização_Computação_Quântica-blue)
![Institution](https://img.shields.io/badge/Instituição-SENAI_CIMATEC-red)
![Framework](https://img.shields.io/badge/Framework-Qiskit-purple)

Este repositório contém os artefatos, códigos e análises desenvolvidos durante as atividades práticas **Hands-on 1 e 2** da disciplina de **Fundamentos da Computação Quântica**.

---

## 🏫 Contexto Acadêmico

- **Instituição:** Universidade SENAI CIMATEC
- **Curso:** Especialização em Computação Quântica
- **Disciplina:** Fundamentos da Computação Quântica
- **Professor:** Dr. Otto Menegasso Pires
- **Data da Entrega:** 24/11/2025

---

## 👥 Equipe de Desenvolvimento

| Membro | Função |
|:---|:---|
| **Davidson Clem** | Desenvolvimento, Documentação, Análise e Testes|
| **João Filipe Muchanga** | Desenvolvimento e Análise |
| **José Hidalgo Suárez** | Desenvolvimento e Testes |
| **Wild Freitas da Silva Santos** | Desenvolvimento e Revisão |

---

## 🎯 Objetivos da Atividade

O objetivo principal deste projeto é consolidar o entendimento sobre a manipulação de qubits e a visualização de seus estados na Esfera de Bloch. As atividades focam em:

1. **Circuitos de 2 Qubits:** Criação e execução de circuitos quânticos compostos.
2. **Matrizes de Pauli:** Aplicação prática de portas X, Y, Z em circuitos reais.
3. **Sistemas Compostos:** Implementação de portas de emaranhamento (CNOT) interagindo com portas de superposição (Hadamard).
4. **Análise Teórica:** Justificativa matemática da evolução do vetor de estado |ψ⟩.
5. **Visualização:** Demonstração passo a passo da evolução vetorial na Esfera de Bloch.

---

## ⚙️ Preparação do Ambiente e Stack Tecnológico

Para executar as simulações, utilizamos o **Qiskit** como framework principal.

### Instalação

Se você estiver rodando localmente ou no Google Colab, execute a célula de instalação:

```python
%pip install qiskit qiskit_aer pylatexenc cartopy matplotlib
```

### Bibliotecas Utilizadas

| Biblioteca / Classe | Função no Projeto |
|:---|:---|
| `QuantumCircuit` | Classe fundamental para construção lógica dos circuitos e alocação de registros quânticos/clássicos |
| `Statevector` | Utilizada para extração do vetor de estado exato |
| `plot_bloch_multivector` | Ferramenta de visualização 3D para plotar o vetor de estado na Esfera de Bloch |
| `AerSimulator` | Backend de simulação local utilizado para validar a lógica dos circuitos antes da execução |

---

## ⚛️ Experimento A: Rotações em 1 Qubit

Neste circuito, manipulamos um único qubit (q₀) partindo do estado fundamental |0⟩. O objetivo é visualizar como diferentes portas afetam a fase e a amplitude do vetor, percorrendo a Esfera de Bloch.

### Snippet do Código

```python
qc = QuantumCircuit(1)
qc.h(0)             # Passo 2: Cria superposição
qc.s(0)             # Passo 3: Rotação de fase (Z)
qc.y(0)             # Passo 4: Rotação Pauli-Y
qc.rx(np.pi / 4, 0) # Passo 5: Rotação arbitrária em X
qc.ry(np.pi/2, 0)   # Passo 6: Rotação arbitrária em Y
```

### 📝 Evolução do Estado (Passo a Passo)

A tabela abaixo descreve a trajetória do qubit na Esfera de Bloch durante a execução:

| Passo | Porta | Ação na Esfera de Bloch | Estado Resultante (Teórico) |
|:---:|:---:|:---|:---|
| 1 | Inicial | Vetor aponta verticalmente para o Polo Norte (+Z) | \|0⟩ |
| 2 | H (Hadamard) | Vetor desce 90° até o Equador (+X). Cria superposição | \|+⟩ = (\|0⟩ + \|1⟩)/√2 |
| 3 | S (Fase) | Rotação de 90° ao longo do equador (eixo Z). Vetor vai para +Y | (1/√2)(\|0⟩ + i\|1⟩) |
| 4 | Y (Pauli-Y) | Rotação de 180° em Y. (Fase global, visualmente estático) | Visualmente inalterado |
| 5 | Rx(π/4) | Rotação de 45° em X. O vetor sai do plano equatorial | Estado Misto |
| 6 | Ry(π/2) | Rotação final de 180°. Espelhamento na esfera | Estado Final |

---

## 🔗 Experimento B: Entrelaçamento (2 Qubits)

Neste experimento, exploramos um sistema composto. A sequência de portas cria correlações quânticas e manipula estados de Bell (Emaranhamento).

### Snippet do Código

```python
qc = QuantumCircuit(2)
qc.x(0)         # q0 vira |1⟩
qc.h(0)         # q0 entra em superposição |-⟩
qc.cx(0, 1)     # CNOT: q0 controla q1 -> GERA EMARANHAMENTO
qc.h(0)         # Desfaz superposição em q0 (Interferência)
qc.ry(np.pi, 1) # Rotação final em q1
```

### 🔍 Análise Detalhada da Evolução

#### Após Porta X (q₀)
O sistema sai de |00⟩ para |10⟩.  
**Visualização:** q₀ aponta para o Sul.

#### Após Porta H (q₀)
Cria-se superposição no controle. O estado é |-⟩ ⊗ |0⟩.  
**Visualização:** q₀ aponta para o eixo -X (equador).

#### Após CNOT (q₀ → q₁)
**Momento do Emaranhamento.** O estado do segundo qubit torna-se dependente do primeiro.

Não é mais possível descrever o sistema como dois vetores independentes puros na Esfera de Bloch padrão; a informação reside na correlação entre eles.

#### Etapas Finais (H e Ry)
Aplicação de novas rotações para manipular a base de medição, demonstrando a reversibilidade.

---

## 📂 Estrutura do Repositório

Organização dos arquivos neste projeto:

```
├── notebooks/          # Códigos fonte (Jupyter Notebooks)
│   ├── HandsOn_01.ipynb
│   └── HandsOn_02.ipynb
├── images/             # Capturas das Esferas de Bloch e Circuitos
├── README.md           # Esta documentação
└── requirements.txt    # Dependências (qiskit, matplotlib, etc.)
```

---

## 🚀 Como Executar

Para reproduzir os experimentos deste repositório em sua máquina:

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/nome-do-repo.git
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute os Notebooks:**
Abra os arquivos `.ipynb` localizados na pasta `notebooks/` utilizando Jupyter Lab, VS Code ou Google Colab.

---

## 📊 Resultados Esperados

As simulações validam os princípios fundamentais da mecânica quântica computacional:

- **Superposição:** Confirmada visualmente quando o vetor toca a linha do equador da esfera.
- **Fase Relativa:** Confirmada pelas rotações ao redor do eixo Z (mudança de cor/fase na esfera).
- **Entrelaçamento:** Confirmado matematicamente e pela visualização do Statevector do sistema composto.

---

## 📝 Licença

Este projeto foi desenvolvido para fins acadêmicos na Universidade SENAI CIMATEC.

---

## 📧 Contato

**Davidson Clem**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Davidson_Clem-blue?logo=linkedin)](https://www.linkedin.com/in/davidson-clem/)

