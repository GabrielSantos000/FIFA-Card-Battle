import pandas as pd
import streamlit as st
import plotly.express as px

# Ler o dataframe da Copa do Mundo do ano selecionado.
df = pd.read_csv("DB\Fifa_world_cup_matches 2022.csv")

# df = px # Carrega o conjunto de dados
# fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")  # Cria um gráfico de dispersão
# fig.show()  # Exibe o gráfico

# Tirando as colunas desnecessárias (falta analisar aqui ainda)
df.drop(
    [
        "possession in contest",
        "date",
        "hour",
        "category",
        "total attempts team1",
        "total attempts team2",
        "goal inside the penalty area team1",
        "goal inside the penalty area team2",
        "goal outside the penalty area team1",
        "goal outside the penalty area team2",
        "assists team1",
        "assists team2",
        "on target attempts team1",
        "on target attempts team2",
        "off target attempts team1",
        "off target attempts team2",
        "attempts inside the penalty area team1",
        "attempts inside the penalty area  team2",
        "attempts outside the penalty area  team1",
        "attempts outside the penalty area  team2",
        "left channel team1",
        "left channel team2",
        "left inside channel team1",
        "left inside channel team2",
        "central channel team1",
        "central channel team2",
        "right inside channel team1",
        "right inside channel team2",
        "right channel team1",
        "right channel team2",
        "total offers to receive team1",
        "total offers to receive team2",
        "inbehind offers to receive team1",
        "inbehind offers to receive team2",
        "inbetween offers to receive team1",
        "inbetween offers to receive team2",
        "infront offers to receive team1",
        "infront offers to receive team2",
        "receptions between midfield and defensive lines team1",
        "receptions between midfield and defensive lines team2",
        "attempted line breaks team1",
        "attempted line breaks team2",
        "completed line breaksteam1",
        "completed line breaks team2",
        "attempted defensive line breaks team1",
        "attempted defensive line breaks team2",
        "completed defensive line breaksteam1",
        "completed defensive line breaks team2",
        "fouls against team1",
        "fouls against team2",
        "offsides team1",
        "offsides team2",
        "passes team1",
        "passes team2",
        "passes completed team1",
        "passes completed team2",
        "crosses team1",
        "crosses team2",
        "crosses completed team1",
        "crosses completed team2",
        "switches of play completed team1",
        "switches of play completed team2",
        "corners team1",
        "corners team2",
        "free kicks team1",
        "free kicks team2",
        "penalties scored team1",
        "penalties scored team2",
        "forced turnovers team1",
        "forced turnovers team2",
        "defensive pressures applied team1",
        "defensive pressures applied team2",
    ],
    axis=1,
    inplace=True,
)

# Unificando os times
# Agrupamento das colunas
times1 = (
    df.groupby("team1")[
        ["number of goals team1", "yellow cards team1", "red cards team1","conceded team1","goal preventions team1","own goals team1"]
    ]
    .sum()
    .sort_values("team1")
    .reset_index()
)

times2 = (
    df.groupby("team2")[
        ["number of goals team2", "yellow cards team2", "red cards team2","conceded team2", "goal preventions team2","own goals team2"]
    ]
    .sum()
    .sort_values("team2")
    .reset_index()
)
# Alteração dos nomes das colunas
times1.columns = ["selecao", "gols_time1", "cards_amarelo1", "cards_vermelho1", "gols_sofridos1", "defesas_gol1", "gols_contra1"]
times2.columns = ["selecao", "gols_time2", "cards_amarelo2", "cards_vermelho2", "gols_sofridos2", "defesas_gol2", "gols_contra2"]

time = pd.merge(times1, times2, on="selecao")

gols = time["total_golsByselecao"] = time["gols_time1"] + time["gols_time2"]
cartoes = time["total_cardsByselecao"] = time["cards_vermelho1"] + time["cards_vermelho2"] + time["cards_amarelo1"] + time["cards_amarelo2"]

print(gols, cartoes)

"""
Força da Carta = quantidade de gols feitos + posse de bola + defesa de gols - gols contra - quantidade de cartões(vermelho + amarelo) - gols sofridos
OBJETIVO: Conseguir pegar esses valores no dataframe e fazer o cálculo da força da carta.
"""
