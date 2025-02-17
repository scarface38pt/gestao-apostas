import streamlit as st
import pandas as pd

# Criar ou carregar dados
if "dados" not in st.session_state:
    st.session_state["dados"] = []

st.title("Gestão de Apostas")

# Formulário para adicionar aposta
with st.form("nova_aposta"):
    data = st.date_input("Data da Aposta")
    casa = st.text_input("Casa de Apostas")
    valor_back = st.number_input("Valor Back (€)", min_value=0.0)
    odd_back = st.number_input("Odd Back", min_value=1.0)
    valor_lay = st.number_input("Valor Lay (€)", min_value=0.0)
    odd_lay = st.number_input("Odd Lay", min_value=1.0)
    
    submitted = st.form_submit_button("Registar Aposta")
    if submitted:
        lucro = (valor_back * odd_back - valor_back) - (valor_lay * (odd_lay - 1))
        st.session_state["dados"].append([data, casa, valor_back, odd_back, valor_lay, odd_lay, lucro])
        st.success("Aposta registada com sucesso!")

# Mostrar tabela de apostas
df = pd.DataFrame(st.session_state["dados"], columns=["Data", "Casa", "Valor Back", "Odd Back", "Valor Lay", "Odd Lay", "Lucro"])
st.dataframe(df)
