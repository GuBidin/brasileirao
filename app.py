import pandas as pd
import streamlit as st  # streamlit é uma biblioteca para criar aplicativos web interativos em Python.

# Configurando a página
st.set_page_config(
    page_title="Análise do Campeonato Brasileiro",
    page_icon="⚽"
)

st.title("Análise do Campeonato Brasileiro")
st.write("Este aplicativo permite explorar os dados do Campeonato Brasileiro de Futebol.")
st.write("Os dados foram obtidos do site [Kaggle](https://www.kaggle.com/datasets/adaoduque/campeonato-brasileiro-de-futebol).")

# Função para carregar e tratar os dados do CSV
@st.cache_data
def carregar_dados():
    # lendo o arquivo csv
    df = pd.read_csv('data/campeonato-brasileiro-full.csv')

    # Convertendo a coluna data de texto para data de verdade (dayfirst=True porque o formato é dd/mm/aaaa)
    df["data"] = pd.to_datetime(df["data"], dayfirst=True)

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

# ============================
# Filtro por ano
# ============================
lista_anos = sorted(df["ano"].dropna().unique().tolist())
lista_anos = ["Todos os tempos"] + lista_anos

sel_ano = st.selectbox("Selecione o ano:", lista_anos)

if sel_ano == "Todos os tempos":
    df_filtrado = df.copy()
else:
    df_filtrado = df[df["ano"] == sel_ano]

# ============================
# Seletor de time
# ============================
# A lista de times agora vem do df_filtrado, pra não mostrar times
# que não jogaram no ano selecionado
times = sorted(set(df_filtrado["mandante"]) | set(df_filtrado["visitante"]))
sel_time = st.selectbox("Selecione um time:", times)

# ============================
# Exibindo a tabela filtrada
# ============================
st.dataframe(df_filtrado.head(20))

# ============================
# Filtros de casa/fora
# ============================
jogos_casa = df_filtrado[df_filtrado["mandante"] == sel_time]
jogos_fora = df_filtrado[df_filtrado["visitante"] == sel_time]

# ============================
# Contagem dos resultados
# ============================
# Em casa
vitorias_casa = jogos_casa[jogos_casa["resultado"] == "Vitória mandante"].shape[0]
empates_casa = jogos_casa[jogos_casa["resultado"] == "Empate"].shape[0]
derrotas_casa = jogos_casa[jogos_casa["resultado"] == "Vitória visitante"].shape[0]
# Fora
vitorias_fora = jogos_fora[jogos_fora["resultado"] == "Vitória visitante"].shape[0]
empates_fora = jogos_fora[jogos_fora["resultado"] == "Empate"].shape[0]
derrotas_fora = jogos_fora[jogos_fora["resultado"] == "Vitória mandante"].shape[0]

# ============================
# Totais
# ============================
total_casa = jogos_casa.shape[0]
total_fora = jogos_fora.shape[0]

# ============================
# Percentuais
# ============================
if total_casa > 0:
    pct_vitorias_casa = (vitorias_casa / total_casa) * 100
    pct_empates_casa = (empates_casa / total_casa) * 100
    pct_derrotas_casa = (derrotas_casa / total_casa) * 100
else:
    pct_vitorias_casa = 0
    pct_empates_casa = 0
    pct_derrotas_casa = 0

if total_fora > 0:
    pct_vitorias_fora = (vitorias_fora / total_fora) * 100
    pct_empates_fora = (empates_fora / total_fora) * 100
    pct_derrotas_fora = (derrotas_fora / total_fora) * 100
else:
    pct_vitorias_fora = 0
    pct_empates_fora = 0
    pct_derrotas_fora = 0

# ============================
# Exibição no Streamlit
# ============================
st.subheader("📊 Desempenho da Equipe")
col1, col2 = st.columns(2)
with col1:
    st.markdown("## 🏠 Jogos em Casa")
    st.write(f"**Total de jogos:** {total_casa}")
    st.metric("Vitórias", f"{pct_vitorias_casa:.1f}%")
    st.metric("Empates", f"{pct_empates_casa:.1f}%")
    st.metric("Derrotas", f"{pct_derrotas_casa:.1f}%")
with col2:
    st.markdown("## ✈️ Jogos Fora")
    st.write(f"**Total de jogos:** {total_fora}")
    st.metric("Vitórias", f"{pct_vitorias_fora:.1f}%")
    st.metric("Empates", f"{pct_empates_fora:.1f}%")
    st.metric("Derrotas", f"{pct_derrotas_fora:.1f}%")

# ============================
# Resumo opcional
# ============================
st.divider()
st.write("### Resumo Numérico")
resumo = {
    "Situação": ["Casa", "Fora"],
    "Jogos": [total_casa, total_fora],
    "Vitórias (%)": [round(pct_vitorias_casa, 2), round(pct_vitorias_fora, 2)],
    "Empates (%)": [round(pct_empates_casa, 2), round(pct_empates_fora, 2)],
    "Derrotas (%)": [round(pct_derrotas_casa, 2), round(pct_derrotas_fora, 2)],
}
st.dataframe(pd.DataFrame(resumo), width="stretch")