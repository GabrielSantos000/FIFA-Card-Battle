from sqlalchemy import create_engine

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5432/copa2026"
engine = create_engine(DATABASE_URL)