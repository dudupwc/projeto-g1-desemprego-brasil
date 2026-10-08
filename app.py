import os
import sqlite3
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Desemprego no Brasil | G1", page_icon="📊", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "dados", "simulacao_desemprego_brasil.csv")
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "desemprego.db")
os.makedirs(DB_DIR, exist_ok=True)

@st.cache_data
def carregar_dados():
    engine = create_engine(f"sqlite:///{DB_PATH}")
    try:
        with engine.connect() as con:
            df = pd.read_sql(text("SELECT * FROM desemprego"), con)
        if df.empty:
            raise ValueError("Banco vazio")
    except Exception:
        df = pd.read_csv(CSV_PATH)
        df["data"] = pd.to_datetime(df["data"])
        df.to_sql("desemprego", engine, if_exists="replace", index=False)
    df["data"] = pd.to_datetime(df["data"])
    return df

df = carregar_dados()

# Coordenadas aproximadas para visualização comparativa por UF.
coords = {
    "AC": (-9.97, -67.81), "AL": (-9.57, -36.78), "AM": (-3.10, -60.02),
    "BA": (-12.97, -38.50), "CE": (-3.72, -38.54), "DF": (-15.79, -47.88),
    "ES": (-20.32, -40.34), "GO": (-16.68, -49.25), "MA": (-2.53, -44.30),
    "MG": (-19.92, -43.94), "MS": (-20.47, -54.62), "MT": (-15.60, -56.10),
    "PA": (-1.46, -48.50), "PB": (-7.12, -34.86), "PE": (-8.05, -34.88),
    "PR": (-25.43, -49.27), "RJ": (-22.91, -43.17), "RO": (-8.76, -63.90),
    "RS": (-30.03, -51.23), "SC": (-27.59, -48.55), "SP": (-23.55, -46.63),
    "TO": (-10.18, -48.33)
}

st.title("Desemprego no Brasil — 2015 a 2024")
st.markdown(
    "### Análise exploratória e dashboard interativo\n"
    "Este projeto investiga a evolução do desemprego, diferenças regionais e "
    "relações entre taxa de desemprego, renda, vagas formais e inflação."
)
st.info("A base utilizada é uma **simulação de dados**. Os resultados representam exclusivamente os valores presentes no CSV da atividade e não devem ser interpretados como estatísticas oficiais.")

with st.sidebar:
    st.header("Filtros")
    anos = sorted(df["ano"].unique())
    ano_sel = st.multiselect("Ano", anos, default=anos)
    regioes = sorted(df["regiao"].unique())
    regiao_sel = st.multiselect("Região", regioes, default=regioes)
    ufs = sorted(df.loc[df["regiao"].isin(regiao_sel), "uf"].unique())
    uf_sel = st.multiselect("UF", ufs, default=ufs)
    setores = sorted(df["setor_predominante"].unique())
    setor_sel = st.multiselect("Setor predominante", setores, default=setores)
    riscos = sorted(df["nivel_risco"].unique())
    risco_sel = st.multiselect("Nível de risco", riscos, default=riscos)

    filtrado = df[
        df["ano"].isin(ano_sel)
        & df["regiao"].isin(regiao_sel)
        & df["uf"].isin(uf_sel)
        & df["setor_predominante"].isin(setor_sel)
        & df["nivel_risco"].isin(risco_sel)
    ].copy()

st.caption(f"Observações após filtros: {len(filtrado):,}".replace(",", "."))

# KPIs dinâmicos
c1, c2, c3, c4 = st.columns(4)
taxa_media = filtrado["taxa_desemprego"].mean() if not filtrado.empty else 0
desemp_total = filtrado["desempregados"].sum() if not filtrado.empty else 0
renda_media = filtrado["renda_media"].mean() if not filtrado.empty else 0
vagas_total = filtrado["vagas_formais"].sum() if not filtrado.empty else 0
c1.metric("Taxa média de desemprego", f"{taxa_media:.2f}%")
c2.metric("Desempregados acumulados", f"{desemp_total:,.0f}".replace(",", "."))
c3.metric("Renda média", f"R$ {renda_media:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c4.metric("Vagas formais acumuladas", f"{vagas_total:,.0f}".replace(",", "."))

if filtrado.empty:
    st.warning("Nenhum registro corresponde aos filtros selecionados.")
    st.stop()

st.divider()
st.header("1. Evolução temporal")
temporal = filtrado.groupby("data", as_index=False).agg(
    taxa_desemprego=("taxa_desemprego", "mean"),
    desempregados=("desempregados", "sum")
)
fig, ax = plt.subplots(figsize=(12, 4.8))
sns.lineplot(data=temporal, x="data", y="taxa_desemprego", marker="o", ax=ax)
ax.set_title("Evolução da taxa média de desemprego")
ax.set_xlabel("Período")
ax.set_ylabel("Taxa de desemprego (%)")
ax.grid(alpha=.25)
st.pyplot(fig, use_container_width=True)
st.caption("A série mostra a média das taxas registradas nas observações selecionadas em cada trimestre.")

st.header("2. Comparação regional")
regional = filtrado.groupby("regiao", as_index=False)["taxa_desemprego"].mean().sort_values("taxa_desemprego", ascending=False)
fig, ax = plt.subplots(figsize=(10, 4.5))
ax.barh(regional["regiao"], regional["taxa_desemprego"])
ax.invert_yaxis()
ax.set_title("Taxa média de desemprego por região")
ax.set_xlabel("Taxa média (%)")
ax.set_ylabel("Região")
for i, v in enumerate(regional["taxa_desemprego"]):
    ax.text(v + .05, i, f"{v:.2f}%", va="center")
st.pyplot(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Setor predominante")
    setor = filtrado.groupby("setor_predominante", as_index=False)["taxa_desemprego"].mean().sort_values("taxa_desemprego", ascending=False)
    fig2 = px.bar(setor, x="setor_predominante", y="taxa_desemprego", text_auto=".2f",
                  labels={"setor_predominante":"Setor", "taxa_desemprego":"Taxa média (%)"},
                  title="Desemprego médio por setor")
    st.plotly_chart(fig2, use_container_width=True)
with col2:
    st.subheader("Nível de risco")
    risco = filtrado["nivel_risco"].value_counts().reset_index()
    risco.columns = ["nivel_risco", "quantidade"]
    fig3 = px.pie(risco, names="nivel_risco", values="quantidade", hole=.35,
                  title="Distribuição das observações por nível de risco")
    st.plotly_chart(fig3, use_container_width=True)

st.header("3. Relação entre indicadores")
fig4 = px.scatter(
    filtrado, x="renda_media", y="taxa_desemprego", size="vagas_formais",
    color="regiao", hover_data=["uf", "ano", "trimestre"],
    labels={"renda_media":"Renda média (R$)", "taxa_desemprego":"Taxa de desemprego (%)", "regiao":"Região"},
    title="Renda média × taxa de desemprego"
)
st.plotly_chart(fig4, use_container_width=True)

corr = filtrado[["taxa_desemprego","renda_media","vagas_formais","inflacao"]].corr()
st.subheader("Matriz de correlação")
fig5, ax = plt.subplots(figsize=(7, 4.5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
ax.set_title("Correlação entre indicadores numéricos")
st.pyplot(fig5, use_container_width=True)
st.caption("Correlação próxima de 0 indica relação linear fraca na amostra; isso não implica ausência de outras relações nem causalidade.")

st.header("4. Análise geográfica")
mapa = filtrado.groupby("uf", as_index=False).agg(
    taxa_desemprego=("taxa_desemprego", "mean"),
    desempregados=("desempregados", "sum"),
    renda_media=("renda_media", "mean")
)
mapa["lat"] = mapa["uf"].map(lambda x: coords.get(x, (np.nan, np.nan))[0])
mapa["lon"] = mapa["uf"].map(lambda x: coords.get(x, (np.nan, np.nan))[1])
mapfig = px.scatter_geo(
    mapa, lat="lat", lon="lon", size="desempregados", color="taxa_desemprego",
    hover_name="uf", hover_data={"taxa_desemprego":":.2f", "renda_media":":.2f", "desempregados":":,.0f", "lat":False, "lon":False},
    scope="south america", projection="natural earth",
    title="Indicadores médios por UF — pontos posicionados pelas capitais",
    color_continuous_scale="Turbo"
)
mapfig.update_geos(showcountries=True)
st.plotly_chart(mapfig, use_container_width=True)

st.header("5. Tabela detalhada")
tabela = filtrado.sort_values(["ano", "trimestre", "uf"])[
    ["ano","trimestre","regiao","uf","populacao_ativa","empregados","desempregados",
     "taxa_desemprego","renda_media","setor_predominante","vagas_formais","inflacao","nivel_risco"]
]
st.dataframe(tabela, use_container_width=True, height=360)

st.header("6. Interpretação")
top_reg = regional.iloc[0]
bottom_reg = regional.iloc[-1]
top_uf = mapa.sort_values("taxa_desemprego", ascending=False).iloc[0]
st.markdown(
    f"- **Diferenças regionais:** {top_reg['regiao']} apresenta a maior taxa média entre as regiões selecionadas "
    f"({top_reg['taxa_desemprego']:.2f}%), enquanto {bottom_reg['regiao']} apresenta a menor "
    f"({bottom_reg['taxa_desemprego']:.2f}%).\n"
    f"- **UF em destaque:** {top_uf['uf']} possui a maior taxa média entre as UFs selecionadas "
    f"({top_uf['taxa_desemprego']:.2f}%).\n"
    f"- **Dimensão temporal:** a leitura da série permite identificar períodos de aumento e redução do desemprego "
    f"sem perder a comparação entre regiões.\n"
    f"- **Relações estatísticas:** a matriz de correlação ajuda a avaliar relações lineares entre desemprego, "
    f"renda, vagas formais e inflação, mas não permite concluir causalidade."
)

st.header("Conclusão executiva")
st.write(
    "A análise mostra que o desemprego não se distribui de forma homogênea entre as regiões e UFs. "
    "O dashboard permite explorar essa desigualdade por período, região, estado, setor e nível de risco. "
    "A combinação de indicadores de emprego, renda, vagas formais e inflação amplia a leitura do problema. "
    "Como a base é simulada, as conclusões devem ser utilizadas exclusivamente para fins acadêmicos e de demonstração das técnicas de análise de dados."
)

st.divider()
st.caption("Projeto G1 — Análise e Visualização de Dados com Python | Base simulada fornecida para a atividade.")
