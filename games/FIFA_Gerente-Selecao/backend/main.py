# Importações
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import jogadores

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    #allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jogadores.router, prefix="/api/jogadores")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)

import databases
import sqlalchemy

DATABASE_URL = "postgresql+psycopg2://postgres:adm@localhost:5432/copa2026?client_encoding=utf8"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

jogadores = sqlalchemy.Table(
    "jogadores",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("nome", sqlalchemy.String),
    sqlalchemy.Column("posicao", sqlalchemy.String),
    sqlalchemy.Column("selecao", sqlalchemy.String),
    sqlalchemy.Column("gols", sqlalchemy.Integer),
    sqlalchemy.Column("defesas", sqlalchemy.Integer),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)

from fastapi import APIRouter, HTTPException
from database import database, jogadores

router = APIRouter()

@router.get("/")
async def listar_jogadores():
    query = jogadores.select()
    return await database.fetch_all(query)

@router.get("/{selecao}")
async def jogadores_por_selecao(selecao: str):
    query = jogadores.select().where(jogadores.c.selecao == selecao)
    return await database.fetch_all(query)