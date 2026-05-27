from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:adm@localhost:5432/copa2026?client_encoding=utf8"

_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(
            DATABASE_URL,
            connect_args={
                "options": "-c client_encoding=utf8"
            }
        )
    return _engine