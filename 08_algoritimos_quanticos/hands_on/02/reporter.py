# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# reporter.py — Salvamento automático de plots e geração de relatório PDF
# =============================================================================

import os
import datetime
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image,
    Table, TableStyle, HRFlowable, PageBreak,
)

REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "relatorio_tsp")

_resultados = []
_plot_paths  = {}


def _garantir_pasta():
    os.makedirs(REPORT_DIR, exist_ok=True)


def salvar_plot(fig: plt.Figure, chave: str, tipo: str) -> str:
    """Salva a Figure retornada pela função de visualização em disco.

    Recebe o objeto Figure diretamente — não depende de plt.gcf(),
    garantindo que o conteúdo correto seja salvo independente do backend.

    Args:
        fig:   Figure retornada por plot_graph / plot_route / plot_qaoa_probabilities.
        chave: Chave da instância ("3c", "4c", "5c", "6c").
        tipo:  Identificador do plot ("grafo", "classico", "qaoa", "prob").

    Returns:
        Caminho completo do arquivo salvo.
    """
    _garantir_pasta()
    nome = f"{chave}_{tipo}.png"
    path = os.path.join(REPORT_DIR, nome)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)  # libera memória imediatamente
    _plot_paths[f"{chave}_{tipo}"] = path
    print(f"  📷 Plot salvo: {nome}")
    return path


def registrar_resultado(
    chave:         str,
    label:         str,
    n:             int,
    route_classic: list,
    t_classic:     float,
    route_qaoa:    list,
    t_qaoa:        float,
):
    """Registra os resultados de uma instância para uso no relatório final."""
    def _route_str(r):
        return " → ".join(map(str, r + [r[0]])) if r else "Inválida"

    def _routes_equiv(r1, r2):
        if not r1 or not r2:
            return False
        e1 = set(zip(r1, r1[1:] + [r1[0]]))
        e2 = set(zip(r2, r2[1:] + [r2[0]]))
        return e1 == e2 or e1 == {(b, a) for a, b in e2}

    _resultados.append({
        "chave":          chave,
        "label":          label,
        "n":              n,
        "route_classic":  _route_str(route_classic),
        "t_classic":      t_classic,
        "route_qaoa":     _route_str(route_qaoa),
        "t_qaoa":         t_qaoa,
        "equivalente":    _routes_equiv(route_classic, route_qaoa),
        "qubits_vertice": n * n,
        "qubits_aresta":  n * (n - 1) // 2,
    })


def gerar_relatorio(caminho: str = None) -> str:
    """Gera o relatório PDF consolidado com todos os resultados e plots."""
    _garantir_pasta()

    if caminho is None:
        ts      = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        caminho = os.path.join(REPORT_DIR, f"relatorio_tsp_{ts}.pdf")

    doc    = SimpleDocTemplate(caminho, pagesize=A4,
                               leftMargin=2*cm, rightMargin=2*cm,
                               topMargin=2*cm,  bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    story  = []

    titulo_estilo = ParagraphStyle(
        "Titulo", parent=styles["Title"],
        fontSize=16, spaceAfter=6, textColor=colors.HexColor("#1A237E"),
    )
    subtitulo_estilo = ParagraphStyle(
        "Subtitulo", parent=styles["Heading2"],
        fontSize=12, spaceBefore=14, spaceAfter=4,
        textColor=colors.HexColor("#283593"),
    )
    secao_estilo = ParagraphStyle(
        "Secao", parent=styles["Heading3"],
        fontSize=10, spaceBefore=10, spaceAfter=2,
        textColor=colors.HexColor("#37474F"),
    )
    corpo_estilo = ParagraphStyle(
        "Corpo", parent=styles["Normal"],
        fontSize=9, leading=14, spaceAfter=4,
    )

    # Capa
    story.append(Spacer(1, 1.5*cm))
    story.append(Paragraph("UNIVERSIDADE SENAI CIMATEC", styles["Normal"]))
    story.append(Paragraph("Curso de Especialização em Computação Quântica", styles["Normal"]))
    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor("#1A237E")))
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph("Relatório — Hands-On 02", titulo_estilo))
    story.append(Paragraph(
        "Implementação do QAOA para o Problema do Caixeiro Viajante",
        subtitulo_estilo,
    ))
    story.append(Spacer(1, 0.3*cm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#90A4AE")))
    story.append(Spacer(1, 0.5*cm))

    for label, value in [
        ("Disciplina:",  "Algoritmos Quânticos"),
        ("Turma:",       "98895"),
        ("Professor:",   "Dr. Gustavo Arruda"),
        ("Alunos:",      "Davidson Corrêa Clem, João Filipe Muchanga, José Hidalgo Suárez"),
        ("Data:",        datetime.datetime.now().strftime("%d/%m/%Y %H:%M")),
        ("Modelagem:",   "Edge-based — N(N-1)/2 qubits"),
        ("Sampler:",     "StatevectorSampler (Qiskit V2)"),
    ]:
        story.append(Paragraph(f"<b>{label}</b>  {value}", corpo_estilo))

    story.append(PageBreak())

    # Tabela resumo
    story.append(Paragraph("1. Resumo Comparativo — Todas as Instâncias", subtitulo_estilo))
    story.append(Spacer(1, 0.2*cm))

    cabecalho = ["Instância", "N", "Qubits\nvértice", "Qubits\naresta",
                 "Rota clássica", "T clás.(s)", "Rota QAOA", "T QAOA(s)", "Equiv.?"]
    dados = [cabecalho] + [[
        r["chave"], str(r["n"]), str(r["qubits_vertice"]), str(r["qubits_aresta"]),
        r["route_classic"], f"{r['t_classic']:.2f}",
        r["route_qaoa"],    f"{r['t_qaoa']:.2f}",
        "Sim ✓" if r["equivalente"] else "Não ✗",
    ] for r in _resultados]

    tabela = Table(dados, repeatRows=1)
    tabela.setStyle(TableStyle([
        ("BACKGROUND",     (0, 0), (-1, 0),  colors.HexColor("#1A237E")),
        ("TEXTCOLOR",      (0, 0), (-1, 0),  colors.white),
        ("FONTSIZE",       (0, 0), (-1, -1), 8),
        ("ALIGN",          (0, 0), (-1, -1), "CENTER"),
        ("VALIGN",         (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.HexColor("#F5F5F5"), colors.white]),
        ("GRID",           (0, 0), (-1, -1), 0.4, colors.HexColor("#BDBDBD")),
        ("TOPPADDING",     (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING",  (0, 0), (-1, -1), 4),
    ]))
    story.append(tabela)

    # Seção por instância
    for r in _resultados:
        story.append(PageBreak())
        story.append(Paragraph(f"2. Instância: {r['label']} ({r['chave']})", subtitulo_estilo))
        story.append(Paragraph(
            f"Qubits — vértice: <b>{r['qubits_vertice']}</b>  |  "
            f"aresta: <b>{r['qubits_aresta']}</b>  "
            f"(redução de {r['qubits_vertice'] - r['qubits_aresta']} qubits)",
            corpo_estilo,
        ))
        story.append(Spacer(1, 0.2*cm))

        tipos = [
            ("grafo",    "Mapa de conexões"),
            ("classico", "Rota — Solver clássico"),
            ("qaoa",     "Rota — QAOA"),
            ("prob",     "Distribuição de probabilidades QAOA"),
        ]
        for i in range(0, len(tipos), 2):
            linha = []
            for tipo, descricao in tipos[i:i+2]:
                path = _plot_paths.get(f"{r['chave']}_{tipo}")
                if path and os.path.exists(path):
                    linha.append([Image(path, width=8.5*cm, height=5.5*cm),
                                  Paragraph(descricao, corpo_estilo)])
                else:
                    linha.append([Paragraph(f"[{descricao} indisponível]", corpo_estilo),
                                  Paragraph("", corpo_estilo)])
            if len(linha) == 2:
                tbl = Table([[linha[0][0], linha[1][0]],
                             [linha[0][1], linha[1][1]]],
                            colWidths=[8.7*cm, 8.7*cm])
            else:
                tbl = Table([[linha[0][0]], [linha[0][1]]], colWidths=[8.7*cm])
            tbl.setStyle(TableStyle([
                ("ALIGN",  (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]))
            story.append(tbl)
            story.append(Spacer(1, 0.3*cm))

        story.append(Paragraph("Resultados", secao_estilo))
        story.append(Paragraph(
            f"Rota clássica: <b>{r['route_classic']}</b> (tempo: {r['t_classic']:.4f} s)",
            corpo_estilo))
        story.append(Paragraph(
            f"Rota QAOA: <b>{r['route_qaoa']}</b> (tempo: {r['t_qaoa']:.4f} s)",
            corpo_estilo))
        equiv = ("Sim — o QAOA encontrou a mesma solução ótima."
                 if r["equivalente"] else
                 "Não — o QAOA não convergiu para a solução ótima nesta execução.")
        story.append(Paragraph(f"Rotas equivalentes: <b>{equiv}</b>", corpo_estilo))

    # Conclusão
    story.append(PageBreak())
    story.append(Paragraph("3. Conclusão", subtitulo_estilo))
    story.append(Paragraph(
        "A modelagem baseada em arestas (edge-based) reduziu significativamente "
        "o número de qubits necessários para representar o TSP, viabilizando "
        "a execução de instâncias com 5 e 6 cidades em ambientes com memória "
        "limitada (16 GB RAM). O QAOA demonstrou capacidade de encontrar "
        "soluções próximas ao ótimo com abordagem probabilística, enquanto o "
        "solver clássico garantiu o ótimo por enumeração exata do espaço de estados.",
        corpo_estilo,
    ))

    doc.build(story)
    print(f"\n✔ Relatório gerado: {caminho}")
    return caminho
