import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração inicial da página
st.set_page_config(page_title="Gestão de Apostas", layout="wide")

# Título da aplicação
st.title("📊 Gestão de Apostas Controladas")

# Inicializar dados
if "dados" not in st.session_state:
    st.session_state["dados"] = []

# Formulário para adicionar aposta
with st.form("nova_aposta"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        data = st.date_input("📅 Data da Aposta")
        casa = st.text_input("🏠 Casa de Apostas")

    with col2:
        valor_back = st.number_input("💰 Valor Back (€)", min_value=0.0, step=0.1)
        odd_back = st.number_input("📈 Odd Back", min_value=1.0, step=0.01)

    with col3:
        valor_lay = st.number_input("💰 Valor Lay (€)", min_value=0.0, step=0.1)
        odd_lay = st.number_input("📉 Odd Lay", min_value=1.0, step=0.01)

    submitted = st.form_submit_button("✅ Registar Aposta")

    if submitted:
        # Cálculo do lucro da aposta
        lucro = (valor_back * (odd_back - 1)) - (valor_lay * (odd_lay - 1))
        st.session_state["dados"].append([data, casa, valor_back, odd_back, valor_lay, odd_lay, lucro])
        st.success("Aposta registada com sucesso!")

# Converter dados em DataFrame
df = pd.DataFrame(st.session_state["dados"], columns=["Data", "Casa", "Valor Back", "Odd Back", "Valor Lay", "Odd Lay", "Lucro (€)"])

# Mostrar tabela de apostas
st.subheader("📜 Histórico de Apostas")
st.dataframe(df, height=300)

# Gráfico de lucros
st.subheader("📊 Evolução do Lucro")
fig, ax = plt.subplots()
ax.plot(df["Data"], df["Lucro (€)"], marker='o', linestyle='-', color='green')
ax.set_xlabel("Data")
ax.set_ylabel("Lucro (€)")
ax.set_title("Evolução dos Lucros")
st.pyplot(fig)

# Exportação de dados
st.subheader("📤 Exportar Dados")
st.download_button("📥 Baixar Excel", df.to_csv(index=False).encode("utf-8"), "gestao_apostas.csv", "text/csv")
