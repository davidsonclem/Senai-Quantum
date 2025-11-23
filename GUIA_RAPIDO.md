# Guia Rápido - Computação Quântica

## 🎯 Por Onde Começar?

Se você é novo em computação quântica, siga este roteiro de aprendizado:

### Passo 1: Fundamentos Teóricos (1-2 semanas)
📁 Comece com: `exercicios/01-fundamentos/`

**O que aprender:**
- O que é um qubit?
- Superposição e emaranhamento
- Notação de Dirac (bra-ket)
- Probabilidades em medições quânticas

**Recursos:**
- Leia o README em `exercicios/01-fundamentos/`
- Assista: "Quantum Computing for Computer Scientists" (YouTube)
- Consulte: `recursos/referencias.md`

### Passo 2: Portas Quânticas (1 semana)
📁 Continue com: `exercicios/02-portas-quanticas/`

**O que aprender:**
- Portas de Pauli (X, Y, Z)
- Porta Hadamard (H)
- Porta CNOT
- Portas de fase (S, T)

**Prática:**
- Execute: `exemplos/qiskit/exemplo_01_basico.py`
- Modifique os exemplos e observe o comportamento

### Passo 3: Circuitos Quânticos (1 semana)
📁 Avance para: `exercicios/03-circuitos-quanticos/`

**O que aprender:**
- Como construir circuitos
- Ordem de operações
- Medição de qubits
- Estados de Bell

**Prática:**
- Execute: `exemplos/qiskit/exemplo_02_estado_bell.py`
- Crie seus próprios circuitos

### Passo 4: Algoritmos Quânticos (2-3 semanas)
📁 Estude: `exercicios/04-algoritmos/`

**O que aprender:**
- Algoritmo de Deutsch-Jozsa
- Algoritmo de Grover
- Transformada de Fourier Quântica
- VQE e QAOA

**Prática:**
- Execute: `exemplos/qiskit/exemplo_03_deutsch_jozsa.py`
- Execute: `exemplos/qiskit/exemplo_04_grover.py`
- Implemente variações dos algoritmos

### Passo 5: Aplicações (Ongoing)
📁 Explore: `exercicios/05-aplicacoes/`

**O que aprender:**
- Criptografia quântica
- Simulação quântica
- Otimização
- Machine Learning quântico

## 🛠️ Configuração do Ambiente

### Linux/Mac
```bash
# Instalar Python (se necessário)
sudo apt install python3 python3-pip  # Ubuntu/Debian
brew install python3                   # macOS

# Clonar repositório
git clone https://github.com/davidsonclem/Senai-Quantum.git
cd Senai-Quantum

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Windows
```powershell
# Instalar Python de python.org (se necessário)

# Clonar repositório
git clone https://github.com/davidsonclem/Senai-Quantum.git
cd Senai-Quantum

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
```

## ▶️ Executando os Exemplos

### Teste Rápido
```bash
# Ativar ambiente virtual (se ainda não ativou)
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Executar primeiro exemplo
python exemplos/qiskit/exemplo_01_basico.py
```

### Executar Todos os Exemplos
```bash
cd exemplos/qiskit
python exemplo_01_basico.py
python exemplo_02_estado_bell.py
python exemplo_03_deutsch_jozsa.py
python exemplo_04_grover.py
```

## 📝 Exercícios Sugeridos

### Semana 1-2: Fundamentos
- [ ] Ler e resolver todos exercícios em `01-fundamentos/`
- [ ] Calcular probabilidades de medição manualmente
- [ ] Compreender notação de Dirac

### Semana 3: Portas
- [ ] Ler `02-portas-quanticas/`
- [ ] Executar `exemplo_01_basico.py`
- [ ] Modificar exemplo para usar diferentes portas

### Semana 4: Circuitos
- [ ] Ler `03-circuitos-quanticos/`
- [ ] Executar `exemplo_02_estado_bell.py`
- [ ] Criar estado de Bell diferente (|Φ⁻⟩, |Ψ⁺⟩, |Ψ⁻⟩)

### Semana 5-7: Algoritmos
- [ ] Ler `04-algoritmos/`
- [ ] Executar `exemplo_03_deutsch_jozsa.py`
- [ ] Executar `exemplo_04_grover.py`
- [ ] Implementar Deutsch-Jozsa para n=3 qubits

### Semana 8+: Aplicações
- [ ] Ler `05-aplicacoes/`
- [ ] Pesquisar aplicação de interesse
- [ ] Implementar projeto pequeno

## 💡 Dicas de Estudo

### Para Iniciantes
1. **Não pule os fundamentos** - Álgebra linear é essencial
2. **Faça os cálculos manualmente** - Antes de usar o computador
3. **Desenhe os circuitos** - Visualização ajuda muito
4. **Use o simulador** - Teste suas intuições

### Para Programadores
1. **Comece com Qiskit** - É o mais popular e bem documentado
2. **Leia o código dos exemplos** - Entenda cada linha
3. **Modifique os exemplos** - Aprendizado ativo
4. **Use Jupyter Notebooks** - Ótimo para experimentação

### Para Matemáticos
1. **Foque na álgebra linear** - Espaços de Hilbert, unitários
2. **Estude os papers originais** - Links em `recursos/referencias.md`
3. **Prove teoremas** - No-cloning, teleportation
4. **Implemente algoritmos do zero** - Sem frameworks

## 🎓 Próximos Passos

Após completar este repositório:

1. **Execute em Hardware Real**
   - Crie conta na IBM Quantum Experience
   - Execute seus circuitos em computadores quânticos reais
   - Observe o efeito do ruído

2. **Projetos Avançados**
   - Implementar algoritmo de Shor
   - Experimentar com VQE para química
   - Tentar QAOA em problemas de otimização

3. **Contribua para Open Source**
   - Qiskit (github.com/Qiskit/qiskit)
   - Cirq (github.com/quantumlib/Cirq)
   - PennyLane (github.com/PennyLaneAI/pennylane)

4. **Continue Aprendendo**
   - Curse online (Coursera, edX)
   - Participe de hackathons
   - Junte-se à comunidade

## 🆘 Precisa de Ajuda?

### Recursos da Comunidade
- **Stack Exchange**: quantum.stackexchange.com
- **Qiskit Slack**: qiskit.org/slack
- **Reddit**: r/QuantumComputing
- **Discord**: Vários servidores de QC

### Documentação
- **Qiskit**: qiskit.org/documentation
- **IBM Quantum**: quantum-computing.ibm.com/learn
- **Qiskit Textbook**: qiskit.org/textbook

### Dúvidas Comuns

**P: Preciso de um PhD em física?**
R: Não! Conhecimento básico de álgebra linear é suficiente.

**P: Quanto tempo leva para aprender?**
R: Conceitos básicos: 2-3 meses. Proficiência: 6-12 meses.

**P: Preciso de um computador quântico?**
R: Não! Simuladores funcionam bem para aprendizado.

**P: Vale a pena aprender agora?**
R: Sim! O campo está crescendo rapidamente.

## 📊 Checklist de Progresso

Marque conforme avança:

### Fundamentos
- [ ] Entendo o que é um qubit
- [ ] Sei calcular probabilidades de medição
- [ ] Compreendo superposição
- [ ] Compreendo emaranhamento

### Prática
- [ ] Executei todos os exemplos
- [ ] Criei meu primeiro circuito
- [ ] Modifiquei exemplos existentes
- [ ] Implementei algoritmo do zero

### Avançado
- [ ] Executei em hardware real
- [ ] Implementei VQE ou QAOA
- [ ] Contribuí para projeto open source
- [ ] Criei projeto pessoal

---

**Boa sorte em sua jornada na computação quântica! 🚀🔬**

*Lembre-se: Computação quântica é difícil para todo mundo no início. Seja paciente e persistente!*
