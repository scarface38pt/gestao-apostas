import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Gestão de Apostas", layout="wide")

# Estilo CSS para melhorar a aparência
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
    }
    .stApp {
        background-color: #e8f0fe;
    }
    .stDataFrame {
        background-color: white;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título da aplicação
st.title("📊 Gestão de Apostas Controladas")

# Inicializar banca
if "banca" not in st.session_state:
    st.session_state["banca"] = 300.0  # Valor inicial da banca

# Inicializar histórico de apostas
if "dados" not in st.session_state:
    st.session_state["dados"] = []

# Inicializar dados de Matched Betting
if "mb_dados" not in st.session_state:
    st.session_state["mb_dados"] = []

# Inicializar casas de apostas
if "casas" not in st.session_state:
    st.session_state["casas"] = []

# Exibir saldo atual
st.subheader(f"💰 Saldo Atual: €{st.session_state['banca']:.2f}")

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

        # Atualizar banca
        st.session_state["banca"] += lucro
        st.success(f"Aposta registada com sucesso! Novo saldo: €{st.session_state['banca']:.2f}")

# Formulário para adicionar aposta de Matched Betting
with st.form("nova_aposta_mb"):
    st.subheader("🎲 Calculadora Matched Betting")

    col1, col2 = st.columns(2)
    
    with col1:
        valor_back_mb = st.number_input("💰 Valor Back (€) - Matched Betting", min_value=0.0, step=0.1)
        odd_back_mb = st.number_input("📈 Odd Back - Matched Betting", min_value=1.0, step=0.01)

    with col2:
        valor_lay_mb = st.number_input("💰 Valor Lay (€) - Matched Betting", min_value=0.0, step=0.1)
        odd_lay_mb = st.number_input("📉 Odd Lay - Matched Betting", min_value=1.0, step=0.01)

    submitted_mb = st.form_submit_button("✅ Registar Aposta Matched Betting")

    if submitted_mb:
        # Cálculo de Matched Betting
        lucro_mb = (valor_back_mb * (odd_back_mb - 1)) - (valor_lay_mb * (odd_lay_mb - 1))
        st.session_state["mb_dados"].append([data, valor_back_mb, odd_back_mb, valor_lay_mb, odd_lay_mb, lucro_mb])
        st.success(f"Aposta Matched Betting registada com sucesso! Lucro: €{lucro_mb:.2f}")

# Formulário para adicionar casas de apostas
with st.form("nova_casa"):
    st.subheader("🏠 Registo de Casas de Apostas")

    casa_nome = st.text_input("Nome da Casa de Apostas")
    tipo_relacao = st.selectbox("Tipo de Relação", ["Parceria", "Promoção", "Bônus", "Outro"])
    bonus_oferecido = st.text_area("Bônus Oferecido", "Ex: Bônus de Boas-Vindas de 100%")

    submitted_casa = st.form_submit_button("✅ Adicionar Casa")

    if submitted_casa:
        st.session_state["casas"].append([casa_nome, tipo_relacao, bonus_oferecido])
        st.success(f"Casa de Apostas '{casa_nome}' registrada com sucesso!")

# Converter dados em DataFrame
df = pd.DataFrame(st.session_state["dados"], columns=["Data", "Casa", "Valor Back", "Odd Back", "Valor Lay", "Odd Lay", "Lucro (€)"])
df_mb = pd.DataFrame(st.session_state["mb_dados"], columns=["Data", "Valor Back", "Odd Back", "Valor Lay", "Odd Lay", "Lucro (€)"])
df_casas = pd.DataFrame(st.session_state["casas"], columns=["Casa", "Tipo de Relação", "Bônus Oferecido"])

# Mostrar tabela de apostas
st.subheader("📜 Histórico de Apostas")
st.dataframe(df, height=300)

# Mostrar tabela de Matched Betting
st.subheader("📜 Histórico de Matched Betting")
st.dataframe(df_mb, height=300)

# Mostrar tabela de Casas de Apostas
st.subheader("🏠 Registros de Casas de Apostas")
st.dataframe(df_casas, height=300)

# Gráfico de lucros
st.subheader("📊 Evolução da Banca")
fig, ax = plt.subplots()
banca_values = [300] + list(df["Lucro (€)"].cumsum() + 300)
ax.plot(range(len(banca_values)), banca_values, marker='o', linestyle='-', color='green')
ax.set_xlabel("Número de Apostas")
ax.set_ylabel("Saldo (€)")
ax.set_title("Evolução da Banca")
st.pyplot(fig)

# Exportação de dados
st.subheader("📤 Exportar Dados")
st.download_button("📥 Baixar Histórico de Apostas", df.to_csv(index=False).encode("utf-8"), "gestao_apostas.csv", "text/csv")
st.download_button("📥 Baixar Histórico de Matched Betting", df_mb.to_csv(index=False).encode("utf-8"), "gestao_matched_betting.csv", "text/csv")
st.download_button("📥 Baixar Registro de Casas de Apostas", df_casas.to_csv(index=False).encode("utf-8"), "gestao_casas_apostas.csv", "text/csv")
