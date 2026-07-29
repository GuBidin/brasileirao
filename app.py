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

st.title("⚽ Análise do Campeonato Brasileiro") #Titulo do aplicativo
st.write("Este aplicativo permite explorar os dados do Campeonato Brasileiro de Futebol.") #write é usado para exibir texto no aplicativo
st.write(
    "Os dados foram obtidos do Kaggle: "
    "https://www.kaggle.com/datasets/adaoduque/campeonato-brasileiro-de-futebol"
)

# ============================
# Função para carregar os dados
# ============================
@st.cache_data #Função para carregar os dados do arquivo CSV e realizar algumas transformações
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
# Função para calcular a classificação de um determinado conjunto de jogos
# ============================
def calcular_classificacao(df_ano):
    times_ano = sorted(set(df_ano["mandante"]) | set(df_ano["visitante"]))
    tabela = []

    for time in times_ano:
        casa = df_ano[df_ano["mandante"] == time]
        fora = df_ano[df_ano["visitante"] == time]

        vit_casa = (casa["resultado"] == "Vitória mandante").sum()
        emp_casa = (casa["resultado"] == "Empate").sum()
        der_casa = (casa["resultado"] == "Vitória visitante").sum()

        vit_fora = (fora["resultado"] == "Vitória visitante").sum()
        emp_fora = (fora["resultado"] == "Empate").sum()
        der_fora = (fora["resultado"] == "Vitória mandante").sum()

        vitorias = vit_casa + vit_fora
        empates = emp_casa + emp_fora
        derrotas = der_casa + der_fora
        jogos = len(casa) + len(fora)

        gols_pro = casa["mandante_Placar"].sum() + fora["visitante_Placar"].sum()
        gols_contra = casa["visitante_Placar"].sum() + fora["mandante_Placar"].sum()

        pontos = vitorias * 3 + empates

        tabela.append({
            "Time": time,
            "Pontos": pontos,
            "Jogos": jogos,
            "Vitórias": vitorias,
            "Empates": empates,
            "Derrotas": derrotas,
            "Gols Pró": gols_pro,
            "Gols Contra": gols_contra,
            "Saldo de Gols": gols_pro - gols_contra,
        })

    classificacao = pd.DataFrame(tabela).sort_values(
        by=["Pontos", "Saldo de Gols", "Gols Pró"],
        ascending=False
    ).reset_index(drop=True)

    classificacao.index = classificacao.index + 1  # posição começando em 1

    return classificacao


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

# ============================
# Campeão, Promovidos e Rebaixados do ano
# ============================
if sel_ano != "Todos os tempos":
    st.divider()
    st.subheader(f"🏆 Campeão, Promovidos e Rebaixados — {sel_ano}")

    classificacao_ano = calcular_classificacao(df_filtrado)

    campeao = classificacao_ano.iloc[0]["Time"]

    # Times rebaixados: últimos 4 colocados (padrão atual do Brasileirão desde 2006)
    n_rebaixados = 4
    rebaixados = classificacao_ano.tail(n_rebaixados)["Time"].tolist()

    # Times promovidos: jogaram nesse ano mas não jogaram no ano anterior
    ano_anterior = sel_ano - 1
    df_ano_anterior = df[df["ano"] == ano_anterior]

    if not df_ano_anterior.empty:
        times_ano_atual = set(classificacao_ano["Time"])
        times_ano_anterior = set(df_ano_anterior["mandante"]) | set(df_ano_anterior["visitante"])
        promovidos = sorted(times_ano_atual - times_ano_anterior)
    else:
        promovidos = []

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("### 🥇 Campeão")
        st.success(campeao)

    with col_b:
        st.markdown("### ⬆️ Promovidos")
        if promovidos:
            for time in promovidos:
                st.write(f"- {time}")
        else:
            st.write("Sem dados do ano anterior para comparação.")

    with col_c:
        st.markdown("### ⬇️ Rebaixados")
        for time in rebaixados:
            st.write(f"- {time}")

    with st.expander("Ver classificação completa do ano"):
        st.dataframe(classificacao_ano, use_container_width=True)

st.subheader(f"🏆 Todos os jogos do Brasileirão ({sel_ano})") #Subtítulo
st.dataframe(df_filtrado[["data","mandante","mandante_Placar","visitante_Placar","visitante","resultado","arena"]].sort_values("data"), use_container_width=True)
st.divider() #dataframe é usado para exibir os dados em formato de tabela no aplicativo, divider é usado para criar uma linha divisória no aplicativo

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
#Shape [0] retorna o número de linhas do DataFrame, que corresponde à contagem de jogos com o resultado específico.
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