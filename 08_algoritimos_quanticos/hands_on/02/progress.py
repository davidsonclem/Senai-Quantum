# =============================================================================
# UNIVERSIDADE SENAI CIMATEC — Hands-On 02: QAOA para TSP
# progress.py — Barra de progresso visual com tempo decorrido
# =============================================================================

import threading
import time
import sys


class ProgressBar:
    """Barra de progresso visual para o terminal do VS Code / Jupyter.

    Exibe:
      [██████████░░░░░░░░░░]  52%  |  etapa: QAOA 4 cidades  |  ⏱ 00:01:23

    Roda em thread separada — não bloqueia a execução do QAOA.
    """

    LARGURA   = 30
    INTERVALO = 0.25  # segundos entre cada refresh

    def __init__(self, etapa: str, total_etapas: int, etapa_atual: int):
        """
        Args:
            etapa:         Descrição da etapa atual (ex: "QAOA 4 cidades").
            total_etapas:  Total de etapas no loop (para % geral).
            etapa_atual:   Índice da etapa atual (0-based).
        """
        self._etapa        = etapa
        self._total        = total_etapas
        self._atual        = etapa_atual
        self._rodando      = False
        self._thread       = None
        self._inicio       = None
        self._sub_progresso = 0.0   # 0.0 → 1.0 dentro da etapa atual

    def _formatar_tempo(self, segundos: float) -> str:
        s = int(segundos)
        h, r = divmod(s, 3600)
        m, s = divmod(r, 60)
        if h:
            return f"{h:02d}:{m:02d}:{s:02d}"
        return f"{m:02d}:{s:02d}"

    def _renderizar(self, progresso_geral: float, elapsed: float) -> str:
        preenchido = int(self.LARGURA * progresso_geral)
        barra      = "█" * preenchido + "░" * (self.LARGURA - preenchido)
        pct        = int(progresso_geral * 100)
        tempo      = self._formatar_tempo(elapsed)
        return (
            f"\r  [{barra}] {pct:3d}%  |  "
            f"{self._etapa}  |  "
            f"⏱ {tempo}  "
        )

    def _pulsar(self):
        """Anima a barra enquanto o progresso interno é desconhecido."""
        pos = 0
        direcao = 1
        while self._rodando:
            elapsed = time.time() - self._inicio

            # Progresso geral: etapas completas + posição pulsante na atual
            base    = self._atual / self._total
            pulso   = (pos / self.LARGURA) / self._total
            geral   = min(base + pulso, (self._atual + 0.99) / self._total)

            preenchido_base  = int(self.LARGURA * base)
            preenchido_extra = max(0, int(self.LARGURA * geral) - preenchido_base)
            vazio            = self.LARGURA - preenchido_base - preenchido_extra

            barra  = "█" * preenchido_base + "▒" * preenchido_extra + "░" * vazio
            tempo  = self._formatar_tempo(elapsed)
            linha  = (
                f"\r  [{barra}]  "
                f"{self._etapa}  |  "
                f"⏱ {tempo}  "
            )
            sys.stdout.write(linha)
            sys.stdout.flush()

            pos += direcao
            if pos >= self.LARGURA or pos <= 0:
                direcao *= -1
            time.sleep(self.INTERVALO)

    def iniciar(self):
        self._rodando = True
        self._inicio  = time.time()
        self._thread  = threading.Thread(target=self._pulsar, daemon=True)
        self._thread.start()

    def parar(self, sucesso: bool = True):
        self._rodando = False
        if self._thread:
            self._thread.join()
        elapsed = time.time() - self._inicio
        tempo   = self._formatar_tempo(elapsed)
        icone   = "✔" if sucesso else "✗"
        # Linha final fixa — sobrescreve a animação
        sys.stdout.write(
            f"\r  {icone}  {self._etapa}  |  ⏱ {tempo}"
            + " " * 20 + "\n"
        )
        sys.stdout.flush()
        return elapsed


def progresso_etapas(instancias: dict):
    """Imprime cabeçalho do progresso geral antes do loop.

    Args:
        instancias: Dicionário INSTANCES do config.py.
    """
    total = len(instancias)
    print(f"\n  Iniciando processamento: {total} instâncias\n")
    for i, (chave, inst) in enumerate(instancias.items(), 1):
        n       = len(inst["matrix"])
        qubits  = n * (n - 1) // 2
        print(f"    {i}/{total}  {inst['label']:12s}  ({qubits} qubits edge-based)")
    print()
