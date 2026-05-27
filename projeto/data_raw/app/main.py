from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.services.partidas import listar_partidas, listar_selecoes

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    df_partidas = listar_partidas()
    df_selecoes = listar_selecoes()

    partidas = df_partidas.to_dict(orient="records")
    selecoes = df_selecoes.to_dict(orient="records")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "partidas": partidas,
            "selecoes": selecoes,
        }
    )