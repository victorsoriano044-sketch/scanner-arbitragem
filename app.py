import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Scanner Arbitragem PRO", layout="wide")

st.title("📊 Scanner Arbitragem Esportiva PRO")

# =====================
# CONFIGURAÇÕES
# =====================

ARBITRAGEM_MINIMA = st.sidebar.slider(
    "Arbitragem mínima %",
    0.5,
    10.0,
    1.5
)

filtro_live = st.sidebar.selectbox(
    "Filtrar status",
    ["Todos", "Ao vivo", "Pré‑jogo"]
)

filtro_esporte = st.sidebar.selectbox(
    "Filtrar esporte",
    ["Todos", "⚽ Futebol", "🏀 Basquete", "🎮 E‑sports"]
)


# =====================
# BASE SIMULADA
# =====================

dados = [
    {
        "esporte": "⚽ Futebol",
        "liga": "Premier League",
        "jogo": "Liverpool vs Arsenal",
        "data": "18/04/2026",
        "horario": "16:00",
        "live": True,
        "odds": [
            ("Betano", "Liverpool", 2.12),
            ("Bet365", "Empate", 3.40),
            ("Pinnacle", "Arsenal", 3.80),
        ]
    },
    {
        "esporte": "🎮 E‑sports",
        "liga": "CS2 Major",
        "jogo": "FURIA vs NAVI",
        "data": "19/04/2026",
        "horario": "14:30",
        "live": False,
        "odds": [
            ("Betano", "FURIA", 2.20),
            ("Pinnacle", "NAVI", 2.05),
        ]
    }
]


# =====================
# FUNÇÃO ARBITRAGEM
# =====================

def calcular_arbitragem(odds):

    melhores = {}

    for casa, resultado, odd in odds:

        if resultado not in melhores:
            melhores[resultado] = (casa, odd)

        elif odd > melhores[resultado][1]:
            melhores[resultado] = (casa, odd)

    soma = sum(1 / odd for casa, odd in melhores.values())

    if soma < 1:

        lucro = (1 - soma) * 100

        return True, lucro, melhores

    return False, 0, melhores


# =====================
# CONTADOR REGRESSIVO
# =====================

def tempo_restante(data, horario):

    jogo = datetime.strptime(
        data + " " + horario,
        "%d/%m/%Y %H:%M"
    )

    agora = datetime.now()

    if jogo > agora:

        restante = jogo - agora

        horas = restante.seconds // 3600

        minutos = (restante.seconds % 3600) // 60

        return f"⏳ começa em {horas}h {minutos}m"

    return "🔴 já começou"


# =====================
# EXIBIÇÃO
# =====================

for evento in dados:

    arbitragem, lucro, melhores = calcular_arbitragem(evento["odds"])

    if not arbitragem:
        continue

    if lucro < ARBITRAGEM_MINIMA:
        continue

    if filtro_live == "Ao vivo" and not evento["live"]:
        continue

    if filtro_live == "Pré‑jogo" and evento["live"]:
        continue

    if filtro_esporte != "Todos" and evento["esporte"] != filtro_esporte:
        continue

    status = "🔴 AO VIVO" if evento["live"] else "🟢 PRÉ‑JOGO"

    st.subheader(f"{status} — {evento['esporte']}")

    st.write(f"🏆 {evento['liga']}")
    st.write(f"⚔️ {evento['jogo']}")
    st.write(f"📅 {evento['data']}")
    st.write(f"🕐 {evento['horario']}")

    if not evento["live"]:
        st.caption(tempo_restante(evento["data"], evento["horario"]))

    st.write("### Casas arbitragem:")

    for resultado, (casa, odd) in melhores.items():
        st.write(f"{casa} → {resultado} @ {odd}")

    st.success(f"📈 Arbitragem: {round(lucro,2)}%")

    stake_total = st.number_input(
        f"Valor aposta {evento['jogo']}",
        min_value=10.0,
        value=100.0,
        key=evento["jogo"]
    )

    lucro_estimado = stake_total * (lucro / 100)

    st.info(f"💰 Lucro estimado: R$ {round(lucro_estimado,2)}")

    st.caption(
        f"⏱️ Atualizado: {datetime.now().strftime('%H:%M:%S')}"
    )

    st.divider()
