# -*- coding: utf-8 -*-
import pandas as pd


# -------------------------
# FORMA RECENTE
# -------------------------
def score_forma(df_hist, team_name: str, n: int = 5):
    if df_hist.empty:
        return 0, []

    jogos = df_hist[
        (df_hist["home_team"] == team_name) |
        (df_hist["away_team"] == team_name)
    ].sort_values("date").tail(n)

    if jogos.empty:
        return 0, []

    pontos = 0
    sequencia = []

    for _, row in jogos.iterrows():

        if row["home_team"] == team_name:
            gm = row["home_score"]
            gs = row["away_score"]
        else:
            gm = row["away_score"]
            gs = row["home_score"]

        if gm > gs:
            pontos += 3
            sequencia.append("V")
        elif gm == gs:
            pontos += 1
            sequencia.append("E")
        else:
            sequencia.append("D")

    score = round((pontos / (len(jogos) * 3)) * 100)

    return score, sequencia


# -------------------------
# CONFRONTO DIRETO
# -------------------------
def confronto_direto_stats(df_hist, time_a: str, time_b: str):

    jogos = df_hist[
        ((df_hist["home_team"] == time_a) & (df_hist["away_team"] == time_b)) |
        ((df_hist["home_team"] == time_b) & (df_hist["away_team"] == time_a))
    ].sort_values("date")

    if jogos.empty:
        return {
            "partidas": 0,
            "desde": "-",
            "vitorias_a": 0,
            "vitorias_b": 0,
            "empates": 0,
            "gols_a": 0,
            "gols_b": 0,
            "media_gols_a": 0,
            "media_gols_b": 0,
            "maior_vitoria_a": None,
            "maior_vitoria_b": None,
        }

    vitorias_a = 0
    vitorias_b = 0
    empates = 0
    gols_a = 0
    gols_b = 0

    maior_vitoria_a = None
    maior_vitoria_b = None

    for _, row in jogos.iterrows():

        if row["home_team"] == time_a:
            ga = row["home_score"]
            gb = row["away_score"]
        else:
            ga = row["away_score"]
            gb = row["home_score"]

        gols_a += ga
        gols_b += gb

        if ga > gb:
            vitorias_a += 1
            diff = ga - gb
            if not maior_vitoria_a or diff > maior_vitoria_a[0]:
                maior_vitoria_a = (diff, f"{ga}x{gb}")
        elif ga < gb:
            vitorias_b += 1
            diff = gb - ga
            if not maior_vitoria_b or diff > maior_vitoria_b[0]:
                maior_vitoria_b = (diff, f"{ga}x{gb}")
        else:
            empates += 1

    total = len(jogos)

    return {
        "partidas": total,
        "desde": str(jogos.iloc[0]["date"].date()),
        "vitorias_a": vitorias_a,
        "vitorias_b": vitorias_b,
        "empates": empates,
        "gols_a": gols_a,
        "gols_b": gols_b,
        "media_gols_a": round(gols_a / total, 2),
        "media_gols_b": round(gols_b / total, 2),
        "maior_vitoria_a": maior_vitoria_a[1] if maior_vitoria_a else None,
        "maior_vitoria_b": maior_vitoria_b[1] if maior_vitoria_b else None,
    }


# -------------------------
# TABELA ÚLTIMOS JOGOS
# -------------------------
def montar_tabela_ultimos_jogos(df_hist, team_name: str, n: int = 5):

    jogos = df_hist[
        (df_hist["home_team"] == team_name) |
        (df_hist["away_team"] == team_name)
    ].sort_values("date").tail(n)

    if jogos.empty:
        return pd.DataFrame()

    linhas = []

    for _, row in jogos.iterrows():

        if row["home_team"] == team_name:
            casa = row["home_team"]
            fora = row["away_team"]
            placar = f"{row['home_score']} x {row['away_score']}"
        else:
            casa = row["away_team"]
            fora = row["home_team"]
            placar = f"{row['away_score']} x {row['home_score']}"

        linhas.append({
            "Data": row["date"].date(),
            "Casa": casa,
            "Fora": fora,
            "Placar": placar,
        })

    return pd.DataFrame(linhas)