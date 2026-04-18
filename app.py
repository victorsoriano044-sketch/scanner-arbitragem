import streamlit as st
import time

st.set_page_config(layout="wide")
st.title("Scanner PRO Arbitragem Completa Multi‑Mercado")

# ===============================
# CONFIG USUÁRIO
# ===============================

stake_total = st.number_input(
    "Valor total da aposta",
    10,
    10000,
    100
)

alerta_minimo = st.slider(
    "Alerta mínimo (%)",
    0.5,
    10.0,
    1.5
)


# ===============================
# BASE SIMULADA MULTI-MERCADO
# (estrutura pronta para APIs reais)
# ===============================

def coletar_odds():

    return {

        "Barcelona vs Real Madrid": {

            "1x2": {

                "Betano": {"home": 2.15},

                "Pinnacle": {"away": 2.10}

            },

            "OverUnder2.5": {

                "Superbet": {"over": 2.08},

                "Betano": {"under": 2.05}

            },

            "Handicap+1": {

                "Pinnacle": {"home": 2.04},

                "Superbet": {"away": 2.06}

            },

            "Kickoff": {

                "Betano": "20:00",

                "Pinnacle": "19:45"

            }

        }

    }


# ===============================
# DETECTOR SUREBET
# ===============================

dados = coletar_odds()

surebet_detectada = False


for jogo in dados:

    mercados = dados[jogo]


    # ===============================
    # 1x2
    # ===============================

    if "1x2" in mercados:

        casas = mercados["1x2"]

        if len(casas) >= 2:

            odds = []

            for casa in casas:

                odds.append(list(casas[casa].values())[0])

            soma = sum(1/x for x in odds)

            if soma < 1:

                surebet_detectada = True

                lucro_percentual = (1 - soma) * 100


                if lucro_percentual >= alerta_minimo:

                    st.warning("🚨 ALERTA 1x2 🚨")


                st.success(f"{jogo} → arbitragem 1x2 ({round(lucro_percentual,2)}%)")


    # ===============================
    # OVER/UNDER
    # ===============================

    if "OverUnder2.5" in mercados:

        casas = mercados["OverUnder2.5"]

        if len(casas) >= 2:

            odds = []

            for casa in casas:

                odds.append(list(casas[casa].values())[0])

            soma = sum(1/x for x in odds)

            if soma < 1:

                surebet_detectada = True

                lucro_percentual = (1 - soma) * 100


                if lucro_percentual >= alerta_minimo:

                    st.warning("🚨 ALERTA OVER/UNDER 🚨")


                st.success(f"{jogo} → arbitragem gols ({round(lucro_percentual,2)}%)")


    # ===============================
    # HANDICAP
    # ===============================

    if "Handicap+1" in mercados:

        casas = mercados["Handicap+1"]

        if len(casas) >= 2:

            odds = []

            for casa in casas:

                odds.append(list(casas[casa].values())[0])

            soma = sum(1/x for x in odds)

            if soma < 1:

                surebet_detectada = True

                lucro_percentual = (1 - soma) * 100


                if lucro_percentual >= alerta_minimo:

                    st.warning("🚨 ALERTA HANDICAP 🚨")


                st.success(f"{jogo} → arbitragem handicap ({round(lucro_percentual,2)}%)")


    # ===============================
    # DIVERGÊNCIA DE HORÁRIO
    # ===============================

    if "Kickoff" in mercados:

        horarios = list(mercados["Kickoff"].values())

        if len(set(horarios)) > 1:

            st.warning(f"⚠ Divergência de horário → {jogo}")

            for casa in mercados["Kickoff"]:

                st.write(casa, "→", mercados["Kickoff"][casa])

            st.markdown("---")


# ===============================
# STATUS
# ===============================

if not surebet_detectada:

    st.info("Scanner ativo ✔ aguardando oportunidades multi‑mercado")


time.sleep(30)

st.rerun()