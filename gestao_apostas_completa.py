import streamlit as st
import pandas as pd
import os

# Arquivos para salvar os dados
CASAS_ARQUIVO = "casas_apostas.csv"
APOSTAS_ARQUIVO = "registros_apostas.csv"
CAIXA_ARQUIVO = "caixa_inicial.csv"

# Função para carregar as casas de apostas registradas
def carregar_casas():
    if os.path.exists(CASAS_ARQUIVO):
        return pd.read_csv(CASAS_ARQUIVO)["Casa"].tolist()
    else:
        return []

# Função para carregar a caixa inicial
def carregar_caixa():
    if os.path.exists(CAIXA_ARQUIVO):
        df = pd.read_csv(CAIXA_ARQUIVO)
        return df["Saldo"].iloc[0]
    else:
        return 300  # Valor inicial da caixa (caso não exista o arquivo)

# Função para salvar a caixa
def salvar_caixa(saldo):
    df = pd.DataFrame({"Saldo": [saldo]})
    df.to_csv(CAIXA_ARQUIVO, index=False)

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
    saldo = carregar_caixa()
    
    apostas = []
    if os.path.exists(APOSTAS_ARQUIVO):
        apostas = pd.read_csv(APOSTAS_ARQUIVO)

    # Calcular o impacto da aposta na caixa
    saldo -= valor_back  # Subtrai o valor de Back
    saldo += valor_lay   # Adiciona o valor de Lay (considerando que foi um sucesso)

    nova_aposta = {
        "Casa": casa,
        "Valor Back (€)": valor_back,
        "Odd Back": odd_back,
        "Valor Lay (€)": valor_lay,
        "Odd Lay": odd_lay,
        "Saldo Após Aposta (€)": saldo
    }

    apostas.append(nova_aposta)
    df_apostas = pd.DataFrame(apostas)
    df_apostas.to_csv(APOSTAS_ARQUIVO, index=False)
    
    salvar_caixa(saldo)
    
    st.success(f"Aposta registrada na casa {casa} com sucesso!")
    st.write(f"Saldo atual: €{saldo:.2f}")

# Layout do Streamlit
st.title("Gestão de Apostas - Matched Betting")

# Registro de casa de apostas
st.header("Registrar Casa de Apostas")
nova_casa = st.text_input("Digite o nome da nova casa de apostas:")
if st.button("Registrar Casa"):
    registrar_casa_apostas(nova_casa)

# Registro de aposta
st.header("Registrar Aposta")
casas_apostas = carregar_casas()

if casas_apostas:
    casa_aposta = st.selectbox("Selecione a Casa de Apostas", casas_apostas)  # Dropdown para seleção
    valor_back = st.number_input("Valor Back (€)", min_value=0.0)
    odd_back = st.number_input("Odd Back", min_value=1.0)
    
    valor_lay = st.number_input("Valor Lay (€)", min_value=0.0)
    odd_lay = st.number_input("Odd Lay", min_value=1.0)

    if st.button("Registrar Aposta"):
        registrar_aposta(casa_aposta, valor_back, odd_back, valor_lay, odd_lay)
else:
    st.warning("Nenhuma casa de apostas registrada. Por favor, registre uma casa primeiro.")

# Exibindo o saldo da caixa
st.header("Saldo da Caixa Inicial")
saldo_atual = carregar_caixa()
st.write(f"Saldo atual da caixa: €{saldo_atual:.2f}")

