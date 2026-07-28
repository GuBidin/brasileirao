import pandas as pd
import streamlit as st

# ============================
# Configuração da página
# ============================
st.set_page_config(
    page_title="Análise do Campeonato Brasileiro",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Análise do Campeonato Brasileiro")
st.write("Este aplicativo permite explorar os dados do Campeonato Brasileiro de Futebol.")
st.write(
    "Os dados foram obtidos do Kaggle: "
    "https://www.kaggle.com/datasets/adaoduque/campeonato-brasileiro-de-futebol"
)

# ============================
# Função para carregar os dados
# ============================
@st.cache_data
def carregar_dados():
    df = pd.read_csv("data/campeonato-brasileiro-full.csv")

    # Converter data
    df["data"] = pd.to_datetime(df["data"], dayfirst=True)

    # Criar coluna ano
    df["ano"] = df["data"].dt.year

    # Criar coluna resultado (perspectiva de quem jogou em casa)
    def resultado(row):
        if row["mandante_Placar"] > row["visitante_Placar"]:
            return "Vitória mandante"
        elif row["mandante_Placar"] < row["visitante_Placar"]:
            return "Vitória visitante"
        else:
            return "Empate"

    df["resultado"] = df.apply(resultado, axis=1)

    return df


# ============================
# Carregar dados
# ============================
df = carregar_dados()


# ============================
# Filtro por Ano
# ============================
lista_anos = sorted(df["ano"].dropna().unique().tolist())
lista_anos = ["Todos os tempos"] + lista_anos

col1_filtro, col2_filtro = st.columns(2)

with col1_filtro:
    sel_ano = st.selectbox(
        "Selecione o ano:",
        lista_anos
    )

if sel_ano == "Todos os tempos":
    df_filtrado = df.copy()
else:
    df_filtrado = df[df["ano"] == sel_ano]

# ============================
# Seleção do Time
# ============================
times = sorted(
    set(df_filtrado["mandante"]) |
    set(df_filtrado["visitante"])
)

with col2_filtro:
    sel_time = st.selectbox(
        "Selecione um time:",
        times
    )

st.subheader(f"🏆 Todos os jogos do Brasileirão ({sel_ano})")
st.dataframe(df_filtrado[["data","mandante","mandante_Placar","visitante_Placar","visitante","resultado","arena"]].sort_values("data"), use_container_width=True)
st.divider()

# ============================
# Jogos em casa e fora
# ============================
jogos_casa = df_filtrado[df_filtrado["mandante"] == sel_time]
jogos_fora = df_filtrado[df_filtrado["visitante"] == sel_time]

# ============================
# Tabela dos jogos do time (com resultado na perspectiva do time selecionado)
# ============================
jogos_time = pd.concat([jogos_casa, jogos_fora]).sort_values("data").copy()

# Função que traduz o resultado para a perspectiva do time selecionado
def resultado_para_o_time(row):
    if row["mandante"] == sel_time:
        if row["resultado"] == "Vitória mandante":
            return "Vitória"
        elif row["resultado"] == "Vitória visitante":
            return "Derrota"
        else:
            return "Empate"
    else:  # sel_time jogou como visitante
        if row["resultado"] == "Vitória visitante":
            return "Vitória"
        elif row["resultado"] == "Vitória mandante":
            return "Derrota"
        else:
            return "Empate"

jogos_time["resultado_time"] = jogos_time.apply(resultado_para_o_time, axis=1)

st.subheader(f"📅 Jogos do {sel_time} ({sel_ano})")

st.dataframe(
    jogos_time[
        [
            "data",
            "mandante",
            "mandante_Placar",
            "visitante_Placar",
            "visitante",
            "resultado_time",
            "arena",
        ]
    ].rename(columns={"resultado_time": f"Resultado ({sel_time})"}),
    use_container_width=True
)

# ============================
# Contagem dos resultados
# ============================

# Casa
vitorias_casa = jogos_casa[
    jogos_casa["resultado"] == "Vitória mandante"
].shape[0]

empates_casa = jogos_casa[
    jogos_casa["resultado"] == "Empate"
].shape[0]

derrotas_casa = jogos_casa[
    jogos_casa["resultado"] == "Vitória visitante"
].shape[0]

# Fora
vitorias_fora = jogos_fora[
    jogos_fora["resultado"] == "Vitória visitante"
].shape[0]

empates_fora = jogos_fora[
    jogos_fora["resultado"] == "Empate"
].shape[0]

derrotas_fora = jogos_fora[
    jogos_fora["resultado"] == "Vitória mandante"
].shape[0]

# ============================
# Totais
# ============================
total_casa = len(jogos_casa)
total_fora = len(jogos_fora)

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
# Dashboard de desempenho
# ============================
st.divider()

st.subheader(f"📊 Desempenho do {sel_time}")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🏠 Jogos em Casa")
    st.metric("Total de jogos", total_casa)
    st.metric("Vitórias", f"{pct_vitorias_casa:.1f}%")
    st.metric("Empates", f"{pct_empates_casa:.1f}%")
    st.metric("Derrotas", f"{pct_derrotas_casa:.1f}%")

with col2:
    st.markdown("### ✈️ Jogos Fora")
    st.metric("Total de jogos", total_fora)
    st.metric("Vitórias", f"{pct_vitorias_fora:.1f}%")
    st.metric("Empates", f"{pct_empates_fora:.1f}%")
    st.metric("Derrotas", f"{pct_derrotas_fora:.1f}%")

# ============================
# Resumo
# ============================
st.divider()

st.subheader("📈 Resumo Estatístico")

resumo = pd.DataFrame(
    {
        "Situação": ["Casa", "Fora"],
        "Jogos": [total_casa, total_fora],
        "Vitórias (%)": [round(pct_vitorias_casa, 2), round(pct_vitorias_fora, 2)],
        "Empates (%)": [round(pct_empates_casa, 2), round(pct_empates_fora, 2)],
        "Derrotas (%)": [round(pct_derrotas_casa, 2), round(pct_derrotas_fora, 2)],
    }
)

st.dataframe(
    resumo,
    use_container_width=True
)