# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://postgres:adm@localhost:5432/copa2026"

_engine = None

# ENGINE
def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(
            DATABASE_URL,
            connect_args={
                "options": "-c client_encoding=utf8",
                "client_encoding": "utf8"
            },
            isolation_level="AUTOCOMMIT"
        )
    return _engine

# CARREGAR DADOS PRINCIPAIS
def carregar_dados():
    engine = get_engine()

    # PARTIDAS COM JOIN (corrige estadio + arbitro)
    df_partidas = pd.read_sql(
        text("""
        SELECT 
            p.*,
            e.nome AS estadio_nome,
            e.cidade AS estadio_cidade,
            a.nome AS arbitro_nome
        FROM partidas p
        LEFT JOIN estadios e ON p.estadio_id = e.id
        LEFT JOIN arbitros a ON p.arbitro_id = a.id
    """),
        engine,
    )

    df_selecoes = pd.read_sql(text("SELECT * FROM selecoes"), engine)
    df_jogadores = pd.read_sql(text("SELECT * FROM jogadores"), engine)
    df_estadios = pd.read_sql(text("SELECT * FROM estadios"), engine)
    df_arbitros = pd.read_sql(text("SELECT * FROM arbitros"), engine)

    # HISTÓRICO (CSV)
    try:
        try:
            df_hist = pd.read_csv(
                "data_raw/fifa-world-cup-2022/international_matches.csv", encoding="utf-8"
            )
        except UnicodeDecodeError:
            df_hist = pd.read_csv(
                "data_raw/fifa-world-cup-2022/international_matches.csv", encoding="latin-1"
            )

        # padroniza nomes
        df_hist = df_hist.rename(
            columns={"home_team_score": "home_score", "away_team_score": "away_score"}
        )

        df_hist["date"] = pd.to_datetime(df_hist["date"], errors="coerce")
        df_hist = df_hist.dropna(subset=["date"])

    except Exception as e:
        print("Erro ao carregar histórico:", e)
        df_hist = pd.DataFrame()

    return (
        df_selecoes,
        df_partidas,
        df_jogadores,
        df_estadios,
        df_arbitros,
        df_hist,
    )


# FAVORITOS
def carregar_ids_favoritos():
    engine = get_engine()

    try:
        df = pd.read_sql(text("SELECT partida_id FROM favoritos"), engine)
        return set(df["partida_id"].tolist())
    except Exception as e:
        print("favoritos não encontrados:", e)
        return set()


def favoritar_partida(partida_id: int):
    engine = get_engine()

    with engine.begin() as conn:
        conn.execute(
            text("""
                INSERT INTO favoritos (partida_id)
                VALUES (:id)
                ON CONFLICT DO NOTHING
            """),
            {"id": partida_id},
        )


def desfavoritar_partida(partida_id: int):
    engine = get_engine()

    with engine.begin() as conn:
        conn.execute(
            text("""
                DELETE FROM favoritos
                WHERE partida_id = :id
            """),
            {"id": partida_id},
        )
