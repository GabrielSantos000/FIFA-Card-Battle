import requests

API_KEY = "123"
BASE_API = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"

MAPA_API_TIMES = {
    "Brasil": "Brazil",
    "Alemanha": "Germany",
    "Espanha": "Spain",
    "França": "France",
    "Portugal": "Portugal",
    "Argentina": "Argentina",
    "México": "Mexico",
    "Estados Unidos": "USA",
}

def get_logo_time(nome_time):
    try:
        nome_api = MAPA_API_TIMES.get(nome_time, nome_time)

        url = f"{BASE_API}/searchteams.php?t={nome_api}"
        resp = requests.get(url, timeout=5)

        if resp.status_code == 200:
            data = resp.json()
            if data["teams"]:
                return data["teams"][0]["strTeamBadge"]
    except:
        pass

    return None