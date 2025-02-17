import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import os
import datetime

# Função para registrar uma nova casa de apostas
def registrar_casa_apostas(casas_apostas):
    nome_casa = st.text_input("Nome da Casa de Apostas")
    if st.button("Registrar Casa"):
        if nome_casa not in casas_apostas:
            casas_apostas.append(nome_casa)
            st.success(f"Casa de Apostas {nome_casa} registrada com sucesso!")
        else:
            st.warning("Esta casa já está registrada.")
    return casas_apostas

# Função para registrar apostas
def registrar_aposta(casas_apostas, registros_apostas):
    casa_aposta = st.selectbox("Selecione a Casa de Apostas", casas_apostas)
    valor_back = st.number_input("Aposta a favor (€)", min_value=0.0)
    odd_back = st.number_input("Probabilidade (Aposta a favor)", min_value=1.0)
    valor_lay = st.number_input("Aposta contra (€)", min_value=0.0)
    odd_lay = st.number_input("Probabilidade (Aposta contra)", min_value=1.0)
    
    if st.button("Registrar Aposta"):
        aposta = {
            "Data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Casa de Apostas": casa_aposta,
            "Valor Aposta a favor (€)": valor_back,
            "Probabilidade (Aposta a favor)": odd_back,
            "Valor Aposta contra (€)": valor_lay,
            "Probabilidade (Aposta contra)": odd_lay,
        }
        registros_apostas.append(aposta)
        st.success("Aposta registrada com sucesso!")

    return registros_apostas

# Função para exibir gráficos de lucros/perdas
def exibir_graficos_lucros_perdas(registros_apostas):
    if len(registros_apostas) > 0:
        df = pd.DataFrame(registros_apostas)
        df['Lucro Aposta a Favor (€)'] = df['Valor Aposta a favor (€)'] * df['Probabilidade (Aposta a favor)']
        df['Lucro Aposta Contra (€)'] = df['Valor Aposta contra (€)'] * df['Probabilidade (Aposta contra)']
        df['Lucro Total (€)'] = df['Lucro Aposta a Favor (€)'] - df['Lucro Aposta Contra (€)']
        
        st.write("Análise de Lucros/Perdas:")
        st.write(df[['Data', 'Casa de Apostas', 'Lucro Total (€)']])
        
        fig, ax = plt.subplots()
        df['Lucro Total (€)'].plot(kind='line', ax=ax)
        ax.set_title('Lucros/Perdas ao Longo do Tempo')
        st.pyplot(fig)

# Função para calcular o valor de apostas Lay e Back
def calcular_lay_back():
    st.subheader("Calculadora Lay e Back")
    valor_back = st.number_input("Valor a Favor (€)", min_value=0.0)
    odd_back = st.number_input("Probabilidade (Aposta a favor)", min_value=1.0)
    valor_lay = st.number_input("Valor Contra (€)", min_value=0.0)
    odd_lay = st.number_input("Probabilidade (Aposta contra)", min_value=1.0)

    if st.button("Calcular Aposta Lay/Back"):
        if valor_back > 0 and odd_back > 1:
            lucro_back = valor_back * odd_back
            st.write(f"Lucro esperado com Aposta a Favor: {lucro_back}€")

        if valor_lay > 0 and odd_lay > 1:
            lucro_lay = valor_lay * odd_lay
            st.write(f"Lucro esperado com Aposta Contra: {lucro_lay}€")

# Função de alertas para bônus ou promoções
def alertas_bonus_promocoes(casas_apostas):
    st.subheader("Alertas de Bônus ou Promoções")
    for casa in casas_apostas:
        st.write(f"Para a casa {casa}:")
        # Aqui você pode adicionar a lógica para alertas automáticos
        st.write(" - Promoção de Bônus 50% disponível até 01/03!")

# Função para exportar os dados de apostas
def exportar_dados_apostas(registros_apostas):
    if st.button("Exportar Dados para CSV"):
        df = pd.DataFrame(registros_apostas)
        df.to_csv('apostas.csv', index=False)
        st.success("Dados exportados com sucesso!")

# Função para calcular as probabilidades entre casas de apostas
def calcular_probabilidades(casas_apostas):
    st.subheader("Calculadora de Probabilidades")
    casa_1 = st.selectbox("Selecione a Casa de Apostas 1", casas_apostas)
    casa_2 = st.selectbox("Selecione a Casa de Apostas 2", casas_apostas)
    
    odd_casa_1 = st.number_input(f"Probabilidade {casa_1}", min_value=1.0)
    odd_casa_2 = st.number_input(f"Probabilidade {casa_2}", min_value=1.0)
    
    if st.button("Calcular Comparação de Probabilidades"):
        if odd_casa_1 > 1 and odd_casa_2 > 1:
            st.write(f"Comparação de Odds: Casa {casa_1} - {odd_casa_1} / Casa {casa_2} - {odd_casa_2}")
            st.write("A maior odd indica o maior lucro potencial.")

# Função principal para exibir as opções do menu
def main():
    st.title("Gestão de Apostas - Sistema de Apostas Controladas")
    
    # Inicializando listas de dados
    if not os.path.exists("casas_apostas.json"):
        casas_apostas = []
    else:
        with open("casas_apostas.json", "r") as file:
            casas_apostas = json.load(file)

    if not os.path.exists("registros_apostas.json"):
        registros_apostas = []
    else:
        with open("registros_apostas.json", "r") as file:
            registros_apostas = json.load(file)
    
    # Exibir opções de menu
    menu = ["Registrar Casa de Apostas", "Registrar Aposta", "Cálculo de Lay/Back", "Alertas de Promoções", "Exportar Dados", "Análise de Lucros/Perdas", "Comparação de Probabilidades"]
    escolha = st.sidebar.selectbox("Escolha uma opção", menu)

    # Executar funcionalidades com base na escolha
    if escolha == "Registrar Casa de Apostas":
        casas_apostas = registrar_casa_apostas(casas_apostas)
        with open("casas_apostas.json", "w") as file:
            json.dump(casas_apostas, file)
    
    elif escolha == "Registrar Aposta":
        registros_apostas = registrar_aposta(casas_apostas, registros_apostas)
        with open("registros_apostas.json", "w") as file:
            json.dump(registros_apostas, file)

    elif escolha == "Cálculo de Lay/Back":
        calcular_lay_back()

    elif escolha == "Alertas de Promoções":
        alertas_bonus_promocoes(casas_apostas)

    elif escolha == "Exportar Dados":
        exportar_dados_apostas(registros_apostas)

    elif escolha == "Análise de Lucros/Perdas":
        exibir_graficos_lucros_perdas(registros_apostas)

    elif escolha == "Comparação de Probabilidades":
        calcular_probabilidades(casas_apostas)

if __name__ == "__main__":
    main()
