import streamlit as st
import pandas as pd
import os

# Arquivo onde as casas de apostas são armazenadas
CASAS_ARQUIVO = "casas_apostas.csv"
# Arquivo onde as apostas são registradas
APOSTAS_ARQUIVO = "registros_apostas.csv"

# Função para carregar casas de apostas já registradas
def carregar_casas():
    if os.path.exists(CASAS_ARQUIVO):
        return pd.read_csv(CASAS_ARQUIVO)["Casa"].tolist()
    else:
        return []

# Função para registrar uma nova casa de apostas
def registrar_casa_apostas(casa):
    casas = carregar_casas()
    if casa and casa not in casas:
        casas.append(casa)
        df = pd.DataFrame(casas, columns=["Casa"])
        df.to_csv(CASAS_ARQUIVO, index=False)
        st.success(f"A casa '{casa}' foi registrada com sucesso!")
    else:
        st.warning(f"A casa '{casa}' já está registrada ou o nome está vazio.")

# Função para registrar uma aposta
def registrar_aposta(casa, valor_back, odd_back, valor_lay, odd_lay):
    apostas = []
    if os.path.exists(APOSTAS_ARQUIVO):
        apostas = pd.read_csv(APOSTAS_ARQUIVO)
    
    nova_aposta = {
        "Casa": casa,
        "Valor Back (€)": valor_back,
        "Odd Back": odd_back,
        "Valor Lay (€)": valor_lay,
        "Odd Lay": odd_lay
    }
    
    apostas.append(nova_aposta)
    df_apostas = pd.DataFrame(apostas)
    df_apostas.to_csv(APOSTAS_ARQUIVO, index=False)
    st.success("Aposta registrada com sucesso!")

# Layout do Streamlit
st.title("Gestão de Apostas")
st.header("Registrar Casa de Apostas")

# Registro de casa de apostas
nova_casa = st.text_input("Digite o nome da nova casa de apostas:")
if st.button("Registrar Casa"):
    registrar_casa_apostas(nova_casa)

st.header("Registrar Aposta")

# Seleção de casa de apostas
casas_apostas = carregar_casas()
if casas_apostas:
    casa_aposta = st.selectbox("Selecione a Casa de Apostas", casas_apostas)
    valor_back = st.number_input("Valor Back (€)", min_value=0.0)
    odd_back = st.number_input("Odd Back", min_value=1.0)
    valor_lay = st.number_input("Valor Lay (€)", min_value=0.0)
    odd_lay = st.number_input("Odd Lay", min_value=1.0)
    
    if st.button("Registrar Aposta"):
        registrar_aposta(casa_aposta, valor_back, odd_back, valor_lay, odd_lay)
else:
    st.warning("Nenhuma casa de apostas registrada. Por favor, registre uma casa primeiro.")
