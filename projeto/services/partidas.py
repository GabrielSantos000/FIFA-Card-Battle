import pandas as pd
from services.db import get_engine

def carregar_partidas():
    engine = get_engine()

    return pd.read_sql_query("""
        SELECT
            p.*,
            e.nome AS estadio_nome,
            e.cidade AS estadio_cidade,
            a.nome AS arbitro_nome
        FROM partidas p
        LEFT JOIN estadios e ON e.id = p.estadio_id
        LEFT JOIN arbitros a ON a.id = p.arbitro_id
        ORDER BY p.grupo, p.id
    """, engine)