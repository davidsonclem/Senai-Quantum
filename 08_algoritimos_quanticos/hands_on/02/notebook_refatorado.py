# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Curso de Especialização em Computação Quântica
# Hands-On 02: Implementação do QAOA para o Problema do Caixeiro Viajante
# Disciplina: Algoritmos Quânticos | Turma: 98895
# Professor: Dr. Gustavo Arruda
# Alunos: Davidson Corrêa Clem, João Filipe Muchanga, José Hidalgo Suárez
# Data: 15/03/2026
# =============================================================================


# ----------------------------------------------------------------------------
# CÉLULA 1 — Instalação de dependências
# Execute apenas uma vez. Comente nas execuções seguintes.
# ----------------------------------------------------------------------------
import subprocess, sys

subprocess.check_call([
    sys.executable, "-m", "pip", "install", "-q",
    "qiskit", "qiskit-aer", "qiskit-optimization",
    "qiskit-algorithms", "docplex", "networkx",
    "matplotlib", "reportlab",
])
print("✔ Dependências instaladas.")


# ----------------------------------------------------------------------------
# CÉLULA 2 — Imports globais
# ----------------------------------------------------------------------------
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

print("✔ Imports prontos.")


# ----------------------------------------------------------------------------
# CÉLULA 3 — Loop principal
# ----------------------------------------------------------------------------
from config        import INSTANCES
from tsp_graph     import build_qubo, interpret_edge_solution
from solvers       import solve_classical, solve_qaoa
from visualization import plot_graph, plot_route, plot_qaoa_probabilities
from analysis      import compare_results, sanitize_route
from reporter      import salvar_plot, registrar_resultado, gerar_relatorio
from progress      import ProgressBar, progresso_etapas

progresso_etapas(INSTANCES)

total     = len(INSTANCES)
inicio_geral = __import__("time").time()

for idx, (chave, instancia) in enumerate(INSTANCES.items()):
    # Descomente para pular instâncias pesadas durante testes:
    # if chave in ("5c", "6c"): continue

    w     = instancia["matrix"]
    label = instancia["label"]
    n     = len(w)

    print(f"\n{'='*55}")
    print(f"  [{idx+1}/{total}]  INSTÂNCIA: {label} ({chave})")
    print(f"{'='*55}")

    # --- Grafo ---
    bar = ProgressBar(f"Gerando grafo — {label}", total, idx)
    bar.iniciar()
    fig_grafo = plot_graph(w, title_suffix=label)
    salvar_plot(fig_grafo, chave, "grafo")
    bar.parar()

    # --- QUBO ---
    bar = ProgressBar(f"Construindo QUBO — {label}", total, idx)
    bar.iniciar()
    qp, edges = build_qubo(w)
    bar.parar()

    # --- Solver clássico ---
    bar = ProgressBar(f"Solver clássico — {label}", total, idx)
    bar.iniciar()
    result_classic, t_classic = solve_classical(qp)
    bar.parar()

    route_classic = sanitize_route(
        interpret_edge_solution(result_classic.x, edges, n)
    )
    print(f"  Rota: {route_classic}  |  Tempo: {t_classic:.4f} s")

    if route_classic:
        fig_c = plot_route(w, route_classic, title=f"Rota Clássica — {label}")
        salvar_plot(fig_c, chave, "classico")

    # --- QAOA ---
    bar = ProgressBar(f"QAOA — {label}", total, idx)
    bar.iniciar()
    try:
        result_qaoa, t_qaoa = solve_qaoa(qp)
        bar.parar(sucesso=True)
    except Exception as e:
        bar.parar(sucesso=False)
        print(f"  ✗  Erro no QAOA: {e}")
        continue

    route_qaoa = sanitize_route(
        interpret_edge_solution(result_qaoa.x, edges, n)
    )
    print(f"  Rota: {route_qaoa}  |  Tempo: {t_qaoa:.4f} s")

    if route_qaoa:
        fig_q = plot_route(w, route_qaoa, title=f"Rota QAOA — {label}")
        salvar_plot(fig_q, chave, "qaoa")
    else:
        print("  ⚠️  Rota inválida — tente aumentar QAOA_MAXITER em config.py.")

    # --- Probabilidades ---
    bar = ProgressBar(f"Histograma — {label}", total, idx)
    bar.iniciar()
    fig_p = plot_qaoa_probabilities(result_qaoa)
    salvar_plot(fig_p, chave, "prob")
    bar.parar()

    # --- Comparativo e registro ---
    compare_results(route_classic, t_classic, route_qaoa, t_qaoa)
    registrar_resultado(chave, label, n,
                        route_classic, t_classic,
                        route_qaoa,    t_qaoa)

tempo_total = __import__("time").time() - inicio_geral
print(f"\n{'='*55}")
print(f"  Todas as instâncias concluídas em "
      f"{int(tempo_total//60):02d}:{int(tempo_total%60):02d}")
print(f"{'='*55}")


# ----------------------------------------------------------------------------
# CÉLULA 4 — Relatório PDF
# ----------------------------------------------------------------------------
print("\nGerando relatório PDF...")
caminho_pdf = gerar_relatorio()
print(f"📄 Relatório disponível em: {caminho_pdf}")
