import requests

BASE = "https://www.thesportsdb.com/api/v1/json/123"

def buscar_time(nome):
    try:
        r = requests.get(f"{BASE}/searchteams.php?t={nome}", timeout=5)
        return r.json()
    except:
        return None