# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# visualization.py — Funções de visualização do TSP e resultados QAOA
# =============================================================================

import matplotlib.pyplot as plt
import networkx as nx
from qiskit.visualization import plot_histogram

from tsp_graph import create_graph


def plot_graph(w: list[list[int]], title_suffix: str = "") -> None:
    """Visualiza o mapa de conexões com legenda de cores por custo.

    Arestas com peso < 10 são exibidas em verde (econômicas);
    arestas com peso >= 10 em vermelho tracejado (dispendiosas).

    Args:
        w:            Matriz de adjacência N×N.
        title_suffix: Sufixo opcional para o título do gráfico.
    """
    G = create_graph(w)
    edges = list(G.edges(data=True))
    short_edges = [(u, v) for u, v, d in edges if d["weight"] < 10]
    long_edges  = [(u, v) for u, v, d in edges if d["weight"] >= 10]

    pos = nx.circular_layout(G)
    plt.figure(figsize=(10, 6))

    node_colors = ["#4CAF50" if node == 0 else "#2196F3" for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1800, edgecolors="black")
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold", font_color="white")
    nx.draw_networkx_edges(G, pos, edgelist=short_edges, width=5, edge_color="#4CAF50", label="Rota Econômica")
    nx.draw_networkx_edges(G, pos, edgelist=long_edges,  width=2, edge_color="#F44336", style="--", label="Rota Dispendiosa")

    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=11, font_weight="bold")

    title = "Mapa de Conexões: Analisando Distâncias entre Cidades"
    if title_suffix:
        title += f" — {title_suffix}"
    plt.title(title, fontsize=16, pad=25)
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1), title="Legenda de Custos", shadow=True)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def plot_route(w: list[list[int]], route: list[int], title: str = "Rota Encontrada") -> None:
    """Destaca a rota ótima encontrada sobre o grafo original.

    Args:
        w:     Matriz de adjacência N×N.
        route: Lista de índices das cidades na ordem da rota.
        title: Título do gráfico.
    """
    G = create_graph(w)
    pos = nx.circular_layout(G)
    route_edges = [(route[i], route[(i + 1) % len(route)]) for i in range(len(route))]

    plt.figure(figsize=(10, 6))
    node_colors = ["#4CAF50" if node == 0 else "#2196F3" for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1800, edgecolors="black")
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold", font_color="white")
    nx.draw_networkx_edges(G, pos, width=1, edge_color="#CCCCCC", style="--")
    nx.draw_networkx_edges(G, pos, edgelist=route_edges, width=4, edge_color="#FF5722")

    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=11, font_weight="bold")

    route_str = " → ".join(map(str, route + [route[0]]))
    plt.title(f"{title}\n{route_str}", fontsize=14, pad=20)
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def plot_qaoa_probabilities(result, top_n: int = 10) -> None:
    """Exibe histograma das top N soluções encontradas pelo QAOA.

    Args:
        result: Resultado retornado pelo MinimumEigenOptimizer do QAOA.
        top_n:  Número de estados de maior probabilidade a exibir.
    """
    valid_samples = [s for s in result.samples if s.probability > 0]
    top_samples   = sorted(valid_samples, key=lambda s: s.probability, reverse=True)[:top_n]
    probabilities = {
        "".join(map(str, map(int, s.x))): s.probability
        for s in top_samples
    }
    plot_histogram(
        probabilities,
        title=f"Distribuição de Probabilidades — Top {top_n} Estados",
        figsize=(14, 5),
    )
    plt.tight_layout()
    plt.show()
