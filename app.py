import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Scanner Arbitragem PRO", layout="wide")

st.title("📊 Scanner de Arbitragem Esportiva PRO")

# =========================
# CONFIGURAÇÃO
# =========================

ARBITRAGEM_MINIMA = 1.5  # %

# =========================
# BASE SIMULADA (TEMPORÁRIA)
# depois vamos conectar APIs reais
# =========================

dados = [
    {
        "esporte": "⚽ Futebol",
        "liga": "Premier League",
        "jogo": "Liverpool vs Arsenal",
        "horario": "16:00",
        "live": True,
        "odds": [
            ("Betano", "Liverpool", 2.12, "oficial"),
            ("Bet365", "Empate", 3.40, "oficial"),
            ("Pinnacle", "Arsenal", 3.80, "oficial"),
            ("Futelrede", "Liverpool", 2.25, "indireto"),
        ]
    },

    {
        "esporte": "🎮 E‑sports",
        "liga": "CS2 Major",
        "jogo": "FURIA vs NAVI",
        "horario": "14:30",
        "live": False,
        "odds": [
            ("Betano", "FURIA", 2.20, "oficial"),
            ("Pinnacle", "NAVI", 2.05, "oficial"),
            ("Superbet-net", "FURIA", 2.32, "indireto"),
        ]
    },

    {
        "esporte": "🏀 Basquete",
        "liga": "NBA",
        "jogo": "Lakers vs Celtics",
        "horario": "21:00",
        "live": False,
        "odds": [
            ("Bet365", "Lakers", 2.30, "oficial"),
            ("Betano", "Celtics", 1.95, "oficial"),
            ("Esportenet", "Lakers", 2.40, "indireto"),
        ]
    }
]


# =========================
# FUNÇÃO ARBITRAGEM
# =========================

def calcular_arbitragem(odds):

    melhores_odds = {}

    for casa, resultado, odd, tipo in odds:

        if resultado not in melhores_odds:
            melhores_odds[resultado] = (casa, odd)

        else:
            if odd > melhores_odds[resultado][1]:
                melhores_odds[resultado] = (casa, odd)

    soma = sum(1 / odd for casa, odd in melhores_odds.values())

    if soma < 1:

        lucro = (1 - soma) * 100

        return True, lucro, melhores_odds

    return False, 0, melhores_odds


# =========================
# EXIBIÇÃO
# =========================

for evento in dados:

    arbitragem, lucro, melhores = calcular_arbitragem(evento["odds"])

    if arbitragem and lucro >= ARBITRAGEM_MINIMA:

        status_live = "🔴 AO VIVO" if evento["live"] else "🟢 PRÉ‑JOGO"

        st.subheader(f"{status_live} — {evento['esporte']}")

        st.write(f"🏆 {evento['liga']}")
        st.write(f"⚔️ {evento['jogo']}")
        st.write(f"🕐 {evento['horario']}")

        st.write("### Casas utilizadas na arbitragem:")

        for resultado, (casa, odd) in melhores.items():

            st.write(f"{casa} → {resultado} @ {odd}")

        st.success(f"📈 Arbitragem detectada: {round(lucro,2)}%")

        investimento = st.number_input(
            f"Valor aposta ({evento['jogo']})",
            min_value=10.0,
            value=100.0,
            key=evento["jogo"]
        )

        lucro_estimado = investimento * (lucro / 100)

        st.info(f"💰 Lucro estimado: R$ {round(lucro_estimado,2)}")

        st.caption(f"⏱️ Atualizado: {datetime.now().strftime('%H:%M:%S')}")

        st.divider()
