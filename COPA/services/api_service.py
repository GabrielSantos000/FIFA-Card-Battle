    # -*- coding: utf-8 -*-
import requests

BASE_URL = "https://www.thesportsdb.com/api/v1/json/3"


# -------------------------
# BUSCAR TIME
# -------------------------
def buscar_time_api(nome_time: str):
    try:
        response = requests.get(
            f"{BASE_URL}/searchteams.php",
            params={"t": nome_time},
            timeout=5
        )

        data = response.json()

        if not data or not data.get("teams"):
            return {}, "Time não encontrado na API"

        team = data["teams"][0]

        return {
            "strTeam": team.get("strTeam"),
            "strCountry": team.get("strCountry"),
            "strLeague": team.get("strLeague"),
            "strStadium": team.get("strStadium"),
            "strBadge": team.get("strBadge"),
        }, None

    except Exception as e:
        return {}, str(e)


# -------------------------
# ÚLTIMOS JOGOS
# -------------------------
def buscar_ultimos_eventos_time(nome_time: str):
    try:
        # primeiro pega o ID do time
        response = requests.get(
            f"{BASE_URL}/searchteams.php",
            params={"t": nome_time},
            timeout=5
        )
        data = response.json()

        if not data or not data.get("teams"):
            return [], "Time não encontrado"

        team_id = data["teams"][0]["idTeam"]

        # agora pega os últimos jogos
        response = requests.get(
            f"{BASE_URL}/eventslast.php",
            params={"id": team_id},
            timeout=5
        )

        data = response.json()

        if not data or not data.get("results"):
            return [], "Sem jogos recentes"

        return data["results"], None

    except Exception as e:
        return [], str(e)