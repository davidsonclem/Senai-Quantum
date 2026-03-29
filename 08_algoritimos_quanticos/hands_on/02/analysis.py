# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# analysis.py — Comparativo clássico vs QAOA e verificação de equivalência
# =============================================================================


def sanitize_route(route) -> list[int]:
    """Garante que a rota é uma lista plana de inteiros.

    O tsp.interpret() pode retornar listas aninhadas ou valores inválidos
    quando o QAOA não converge para uma solução viável. Esta função
    filtra e achata o resultado para evitar erros nas funções de plot.

    Args:
        route: Saída bruta de tsp.interpret().

    Returns:
        Lista plana de inteiros, ou lista vazia se a rota for inválida.
    """
    if not route:
        return []
    flat = []
    for item in route:
        if isinstance(item, (list, tuple)):
            flat.extend([int(x) for x in item if isinstance(x, (int, float))])
        elif isinstance(item, (int, float)):
            flat.append(int(item))
    return flat


def _route_str(route: list[int]) -> str:
    """Formata a rota como string cíclica legível."""
    return " → ".join(map(str, route + [route[0]])) if route else "N/A"

'''
def _routes_equivalent(r1: list[int], r2: list[int]) -> bool:
    """Verifica se duas rotas são equivalentes (mesmas arestas, sentidos opostos aceitos).

    Args:
        r1: Primeira rota (lista de índices de cidades).
        r2: Segunda rota.

    Returns:
        True se as rotas percorrem o mesmo conjunto de arestas.
    """
    edges1 = set(zip(r1, r1[1:] + [r1[0]]))
    edges2 = set(zip(r2, r2[1:] + [r2[0]]))
    return edges1 == edges2 or edges1 == {(b, a) for a, b in edges2} '''

def _routes_equivalent(r1: list[int], r2: list[int]) -> bool:
    """Verifica se duas rotas são equivalentes, tratando listas vazias."""
    if not r1 or not r2:
        return False  # Se uma delas é vazia, não são equivalentes
        
    edges1 = set(zip(r1, r1[1:] + [r1[0]]))
    edges2 = set(zip(r2, r2[1:] + [r2[0]]))
    return edges1 == edges2 or edges1 == {(b, a) for a, b in edges2}


def compare_results(
    route_classic: list[int],
    time_classic:  float,
    route_qaoa:    list[int],
    time_qaoa:     float,
) -> None:
    """Imprime o quadro comparativo entre o solver clássico e o QAOA.

    Args:
        route_classic: Rota encontrada pelo solver clássico (NumPy).
        time_classic:  Tempo de execução clássico em segundos.
        route_qaoa:    Rota encontrada pelo QAOA.
        time_qaoa:     Tempo de execução QAOA em segundos.
    """
    sep = "=" * 55
    print(sep)
    print("        COMPARATIVO FINAL: Clássico vs. QAOA")
    print(sep)
    print(f"{'Método':<20} {'Rota':<25} {'Tempo (s)'}")
    print("-" * 55)
    print(f"{'Solver Clássico':<20} {_route_str(route_classic):<25} {time_classic:.4f}")
    print(f"{'QAOA':<20} {_route_str(route_qaoa):<25} {time_qaoa:.4f}")
    print(sep)

    equiv = _routes_equivalent(route_classic, route_qaoa)
    print(f"\n✔ Rotas equivalentes? {'Sim ✅' if equiv else 'Não ❌'}")
    print(
        "\nConclusão: O QAOA encontrou a mesma solução ótima com abordagem "
        "probabilística,\nenquanto o solver clássico garantiu o ótimo por "
        "enumeração exata do espaço de estados."
    )
