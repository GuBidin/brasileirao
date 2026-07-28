import pandas as pd
import streamlit as st  # streamlit é uma biblioteca para criar aplicativos web interativos em Python.

# Configurando a página
st.set_page_config(
    page_title="Análise do Campeonato Brasileiro",
    page_icon="⚽"
)  # set_page_config() é um método do streamlit que configura a página, podemos passar parâmetros como page_title e page_icon para definir o título e o ícone da página.

st.title("Análise do Campeonato Brasileiro")  # st.title() é um método do streamlit que coloca um título na página.
st.write("Este aplicativo permite explorar os dados do Campeonato Brasileiro de Futebol.")  # st.write() é um método do streamlit que escreve texto na página.
st.write("Os dados foram obtidos do site [Kaggle](https://www.kaggle.com/datasets/adaoduque/campeonato-brasileiro-de-futebol).")  # st.write() é um método do streamlit que escreve texto na página.

# Função para carregar e tratar os dados do CSV
@st.cache_data
def carregar_dados():
    # lendo o arquivo csv
    df = pd.read_csv('data/campeonato-brasileiro-full.csv')

    # Convertendo a coluna data de texto para data de verdade
    df["data"] = pd.to_datetime(df["data"])

    # Criando uma nova coluna ano, extraindo o ano da data
    df["ano"] = df["data"].dt.year

    # função para definir o resultado da partida
    def resultado(row):
        if row["mandante_Placar"] > row["visitante_Placar"]:
            return "Vitória mandante"
        elif row["mandante_Placar"] < row["visitante_Placar"]:
            return "Vitória visitante"
        else:
            return "Empate"

    # Criando a coluna resultado
    df["resultado"] = df.apply(resultado, axis=1)

    # Retornando o DataFrame tratado
    return df

# Carregando os dados
df = carregar_dados()

# Exibindo as 20 primeiras linhas
st.dataframe(df.head(20))

#Criar um seletor de time
times = sorted(set(df["mandante"]) | set(df["visitante"]))
sel_time = st.selectbox("Selecione um time:", times)
jogos_casa = df[df["mandante"] == sel_time]
jogos_fora = df[df["visitante"] == sel_time]
