# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# config.py — Configuração centralizada
# =============================================================================

# -----------------------------------------------------------------------------
# Hiperparâmetros do QAOA
# -----------------------------------------------------------------------------
QAOA_REPS    = 1     # Camadas QAOA (mínimo para 4 cidades no Colab)
QAOA_MAXITER = 50    # Iterações COBYLA (reduzido para economizar RAM)
QAOA_SHOTS   = 1024  # Amostras por execução

# -----------------------------------------------------------------------------
# Instâncias do TSP — matrizes de adjacência do exercício
# Penalidade 50 representa arestas inexistentes / muito caras
# -----------------------------------------------------------------------------
INSTANCES = {
    "3c": {
        "label": "3 cidades",
        "matrix": [
            [0,  10, 15],
            [10,  0, 20],
            [15, 20,  0],
        ],
    },
    "4c": {
        "label": "4 cidades",
        "matrix": [
            [ 0,  1, 50, 50],
            [ 1,  0,  2, 50],
            [50,  2,  0,  3],
            [50, 50,  3,  0],
        ],
    },
    "5c": {
        "label": "5 cidades",
        "matrix": [
            [0, 2, 9, 10,  7],
            [2, 0, 6,  4,  3],
            [9, 6, 0,  8,  5],
            [10, 4, 8,  0,  6],
            [7, 3, 5,  6,  0],
        ],
    },
    "6c": {
        "label": "6 cidades",
        "matrix": [
            [0, 4, 1, 9, 8, 6],
            [4, 0, 3, 5, 2, 7],
            [1, 3, 0, 6, 4, 5],
            [9, 5, 6, 0, 3, 2],
            [8, 2, 4, 3, 0, 4],
            [6, 7, 5, 2, 4, 0],
        ],
    },
}

# Instância padrão usada no notebook (enunciado pede 4 cidades)
DEFAULT_INSTANCE = "3c"

# =============================================================================
# SUGESTÕES PARA ACELERAR A EXECUÇÃO (apenas sugestões — não alteram o código)
# =============================================================================
#
# 1. SHOTS ADAPTATIVO
#    Comece com QAOA_SHOTS = 256 para testes rápidos;
#    aumente para 1024 ou 4096 somente na execução final.
#
# 2. CACHE DE QUBO
#    A conversão TSP → QUBO é determinística para uma mesma matriz.
#    Salvar o resultado em disco (joblib.dump) evita recomputar
#    ao reiniciar o kernel:
#
#      import joblib, pathlib
#      cache = pathlib.Path("qubo_cache.pkl")
#      if cache.exists():
#          qubo = joblib.load(cache)
#      else:
#          qubo = build_qubo(w)
#          joblib.dump(qubo, cache)
#
# 3. PARALELISMO COM JOBLIB (instâncias independentes)
#    Rodar w3, w4, w5 e w6 em paralelo no mesmo kernel:
#
#      from joblib import Parallel, delayed
#      results = Parallel(n_jobs=-1)(
#          delayed(solve_classical)(build_qubo(inst["matrix"]))
#          for inst in INSTANCES.values()
#      )
#
# 4. NUMBA JIT (força bruta clássica pura, sem Qiskit)
#    Se quiser benchmark de força bruta mais rápido para comparação:
#
#      from numba import njit
#      @njit
#      def brute_force_tsp(w): ...
#
# 5. STATEVECTORSIMULATOR vs AerSampler
#    StatevectorSampler (já usado) é a opção mais rápida para n <= 4.
#    Para n >= 5, considere AerSampler com method='matrix_product_state'
#    pois ele usa menos memória que o statevector completo.
# =============================================================================
