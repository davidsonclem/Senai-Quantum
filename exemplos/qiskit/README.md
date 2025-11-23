# Exemplos Práticos com Qiskit

Esta pasta contém exemplos práticos de programação quântica usando o framework Qiskit da IBM.

## 📋 Pré-requisitos

```bash
pip install qiskit qiskit-aer matplotlib numpy
```

## 📚 Exemplos Disponíveis

### 1. `exemplo_01_basico.py`
**Conceitos:** Circuito básico, superposição, medição
- Cria um circuito simples com 1 qubit
- Aplica porta Hadamard para criar superposição
- Demonstra distribuição probabilística das medições

**Como executar:**
```bash
python exemplo_01_basico.py
```

### 2. `exemplo_02_estado_bell.py`
**Conceitos:** Emaranhamento, estado de Bell, correlação quântica
- Cria par EPR emaranhado
- Demonstra correlação perfeita entre qubits
- Mostra que nunca medimos estados não correlacionados

**Como executar:**
```bash
python exemplo_02_estado_bell.py
```

### 3. `exemplo_03_deutsch_jozsa.py`
**Conceitos:** Vantagem quântica, oráculo, interferência
- Implementa algoritmo de Deutsch-Jozsa
- Determina se função é constante ou balanceada com 1 query
- Demonstra speedup exponencial vs abordagem clássica

**Como executar:**
```bash
python exemplo_03_deutsch_jozsa.py
```

### 4. `exemplo_04_grover.py`
**Conceitos:** Busca quântica, amplificação de amplitude
- Implementa algoritmo de Grover para busca
- Demonstra speedup quadrático O(√N)
- Encontra elemento marcado em banco não ordenado

**Como executar:**
```bash
python exemplo_04_grover.py
```

## 🎯 Objetivos de Aprendizado

Após estudar estes exemplos, você será capaz de:
1. Criar e manipular circuitos quânticos básicos
2. Entender superposição e emaranhamento na prática
3. Implementar algoritmos quânticos clássicos
4. Visualizar e interpretar resultados de simulações
5. Compreender a vantagem quântica em aplicações específicas

## 📊 Saídas

Os exemplos geram:
- Representação textual dos circuitos
- Contagens de medições
- Histogramas (salvos em `/tmp/`)
- Explicações detalhadas dos resultados

## 🔍 Próximos Passos

Após dominar estes exemplos, você pode:
1. Modificar os parâmetros e observar o comportamento
2. Criar seus próprios circuitos e algoritmos
3. Explorar algoritmos mais avançados (QFT, VQE, QAOA)
4. Executar em computadores quânticos reais via IBM Quantum
5. Estudar mitigação de erros e técnicas NISQ

## 📖 Recursos Adicionais

- [Qiskit Documentation](https://qiskit.org/documentation/)
- [Qiskit Textbook](https://qiskit.org/learn)
- [IBM Quantum Experience](https://quantum-computing.ibm.com/)
- [Qiskit Tutorials](https://github.com/Qiskit/qiskit-tutorials)

## ⚠️ Notas Importantes

- Os exemplos usam simuladores locais (sem ruído)
- Resultados em hardware real podem diferir devido ao ruído
- Para executar em hardware real, é necessário criar conta IBM Quantum
- Os histogramas são salvos no diretório `/tmp/`

## 🤝 Contribuindo

Sinta-se livre para:
- Adicionar novos exemplos
- Melhorar a documentação
- Reportar problemas ou bugs
- Sugerir melhorias

---

**Bons estudos em Computação Quântica! 🚀**
