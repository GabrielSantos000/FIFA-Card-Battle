import pandas as pd

def stats_time_recente(df, time, n=10):
    jogos = df[
        (df["home_team"] == time) | (df["away_team"] == time)
    ].tail(n)

    v = e = d = 0

    for _, row in jogos.iterrows():
        if row["home_team"] == time:
            if row["home_score"] > row["away_score"]:
                v += 1
            elif row["home_score"] == row["away_score"]:
                e += 1
            else:
                d += 1
        else:
            if row["away_score"] > row["home_score"]:
                v += 1
            elif row["away_score"] == row["home_score"]:
                e += 1
            else:
                d += 1

    return v, e, d


def stats_h2h(df, t1, t2):
    jogos = df[
        ((df["home_team"] == t1) & (df["away_team"] == t2)) |
        ((df["home_team"] == t2) & (df["away_team"] == t1))
    ]

    v1 = v2 = e = 0

    for _, row in jogos.iterrows():
        if row["home_team"] == t1:
            if row["home_score"] > row["away_score"]:
                v1 += 1
            elif row["home_score"] == row["away_score"]:
                e += 1
            else:
                v2 += 1
        else:
            if row["away_score"] > row["home_score"]:
                v1 += 1
            elif row["away_score"] == row["home_score"]:
                e += 1
            else:
                v2 += 1

    return v1, v2, e