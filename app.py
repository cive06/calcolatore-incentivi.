import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Calcolatore Incentivi 5.0", layout="wide")

st.title("🚀 Calcolatore Rientro Investimento")
st.subheader("Simulatore Risparmio Energetico + Incentivi Statali")

# Sidebar per gli Input
with st.sidebar:
    st.header("Dati Investimento")
    investimento = st.number_input("Investimento Totale (€)", value=100000, step=5000)
    risparmio_annuo = st.number_input("Risparmio Bolletta Annuo (€)", value=15000, step=1000)
    aliquota_50 = st.slider("Aliquota Credito 5.0 (%)", 5, 45, 35) / 100
    sabatini = st.checkbox("Includi Nuova Sabatini", value=True)

# Calcoli Logici
credito_totale = investimento * aliquota_50
quota_sabatini = (investimento * 0.07) if sabatini else 0
costo_netto = investimento - credito_totale - quota_sabatini

# Creazione Tabella Flussi
anni = list(range(1, 11))
flussi = []
cumulativo = -investimento

for a in anni:
    inc = (credito_totale / 5) + (quota_sabatini / 5) if a <= 5 else 0
    tot_anno = risparmio_annuo + inc
    cumulativo += tot_anno
    flussi.append(cumulativo)

df = pd.DataFrame({"Anno": anni, "Flusso Cumulativo (€)": flussi})

# Visualizzazione Risultati
col1, col2, col3 = st.columns(3)
col1.metric("Costo Netto Reale", f"€ {costo_netto:,.0f}")
col2.metric("Incentivi Totali", f"€ {credito_totale + quota_sabatini:,.0f}")
col3.metric("Rientro (Payback)", f"{next((i+1 for i, v in enumerate(flussi) if v >= 0), '>10')} Anni")

st.plotly_chart(px.line(df, x="Anno", y="Flusso Cumulativo (€)", title="Recupero dell'Investimento nel Tempo"))
