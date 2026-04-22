import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Ler o dataframe da Copa do Mundo do ano selecionado.
df = pd.read_csv("DB\Fifa_world_cup_matches 2022.csv")

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

for i in time['selecao']:
    open()
# gols = time["total_golsByselecao"] = time["gols_time1"] + time["gols_time2"]
# cartoes = time["total_cardsByselecao"] = time["cards_vermelho1"] + time["cards_vermelho2"] + time["cards_amarelo1"] + time["cards_amarelo2"]

# # Gráfico de barras
# sns.barplot(time,x='selecao',y='total_golsByselecao')
# plt.xlabel('Teams')
# plt.ylabel('Total goals scored')
# plt.title('Total goals by each team')
# plt.xticks(rotation=90)
# plt.show()

# """
# Força da Carta = quantidade de gols feitos + posse de bola + defesa de gols - gols contra - quantidade de cartões(vermelho + amarelo) - gols sofridos
# OBJETIVO: Conseguir pegar esses valores no dataframe e fazer o cálculo da força da carta.
# """
