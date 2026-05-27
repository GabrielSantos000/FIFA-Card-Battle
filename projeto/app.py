# coding: utf-8
import itertools
import random
import time
import requests
import psycopg2

API_KEY = "123"
BASE_API = f"https://www.thesportsdb.com/api/v1/json/{API_KEY}"

# Configuração do Banco de Dados
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "copa2026",
    "user": "postgres",
    "password": "adm",
}

# Dicionário com o nome das seleções
MAPA_SELECOES_API = {
    "Brasil": "Brazil",
    "Alemanha": "Germany",
    "Espanha": "Spain",
    "França": "France",
    "Inglaterra": "England",
    "Portugal": "Portugal",
    "Argentina": "Argentina",
    "México": "Mexico",
    "Estados Unidos": "USA",
    "Marrocos": "Morocco",
    "Escócia": "Scotland",
    "Haiti": "Haiti",
    "Canadá": "Canada",
    "Suíça": "Switzerland",
    "Catar": "Qatar",
    "África do Sul": "South Africa",
    "Coreia do Sul": "South Korea",
    "Austrália": "Australia",
    "Paraguai": "Paraguay",
    "Equador": "Ecuador",
    "Costa do Marfim": "Ivory Coast",
    "Curaçao": "Curacao",
    "Países Baixos": "Netherlands",
    "Japão": "Japan",
    "Tunísia": "Tunisia",
    "Bélgica": "Belgium",
    "Peru": "Peru",
    "Camarões": "Cameroon",
    "Arábia Saudita": "Saudi Arabia",
    "Uruguai": "Uruguay",
    "Cabo Verde": "Cape Verde",
    "Senegal": "Senegal",
    "Noruega": "Norway",
    "Áustria": "Austria",
    "Argélia": "Algeria",
    "Jordânia": "Jordan",
    "Colômbia": "Colombia",
    "Uzbequistão": "Uzbekistan",
    "Croácia": "Croatia",
    "Gana": "Ghana",
    "Panamá": "Panama",
}


# ------------------- FUNÇÕES ---------------------------------
def nome_selecao_api(nome: str) -> str:
    return MAPA_SELECOES_API.get(nome, nome)


def avatar_url(nome: str) -> str:
    nome = str(nome).replace(" ", "+")
    # Aqui gerar imagens com as iniciais dos nomes dos jogadores quando a foto deles estiver indisponível.
    return f"https://ui-avatars.com/api/?name={nome}&background=1f2937&color=ffffff&size=128"


def buscar_foto_jogador_api(nome_jogador: str, selecao: str):
    try:
        response = requests.get(
            f"{BASE_API}/searchplayers.php", params={"p": nome_jogador}, timeout=15
        )
        response.raise_for_status()
        data = response.json()
        players = data.get("player") if data else None

        if not players:
            return None

        selecao_api = nome_selecao_api(selecao).lower()

        for p in players:
            equipe = (p.get("strTeam") or "").lower()
            thumb = p.get("strThumb") or p.get("strCutout") or p.get("strRender")
            if thumb and selecao_api in equipe:
                return thumb

        for p in players:
            thumb = p.get("strThumb") or p.get("strCutout") or p.get("strRender")
            if thumb:
                return thumb

        return None
    except Exception:
        return None


# ------------------- VALORES DISPONÍVEIS ---------------------------------
grupos = {
    "A": [
        ("México", "mx"),
        ("África do Sul", "za"),
        ("Coreia do Sul", "kr"),
        ("Haiti", "ht"),
    ],
    "B": [("Canadá", "ca"), ("Suíça", "ch"), ("Catar", "qa"), ("Curaçao", "cw")],
    "C": [
        ("Brasil", "br"),
        ("Marrocos", "ma"),
        ("Escócia", "gb"),
        ("Arábia Saudita", "sa"),
    ],
    "D": [
        ("Estados Unidos", "us"),
        ("Austrália", "au"),
        ("Paraguai", "py"),
        ("Jordânia", "jo"),
    ],
    "E": [
        ("Alemanha", "de"),
        ("Equador", "ec"),
        ("Costa do Marfim", "ci"),
        ("Panamá", "pa"),
    ],
    "F": [
        ("Países Baixos", "nl"),
        ("Japão", "jp"),
        ("Tunísia", "tn"),
        ("Uruguai", "uy"),
    ],
    "G": [("Bélgica", "be"), ("Peru", "pe"), ("Camarões", "cm"), ("Colômbia", "co")],
    "H": [("Espanha", "es"), ("Portugal", "pt"), ("França", "fr"), ("Argentina", "ar")],
}

estadios = [
    ("Atlanta Stadium", "Atlanta", "USA", "https://digitalhub.fifa.com/transform/f5323c22-5aee-4f9d-8c16-b3bcfe33aed9/FWWC-Stadiums?&io=transform:fill,width:1024&quality=75"),
    ("Boston Stadium", "Boston", "USA", "https://digitalhub.fifa.com/transform/ef3e79cd-f30f-4b5c-912f-5d9762f1dd7b/FWC-stadiums-Boston-Gillette?&io=transform:fill,width:1024&quality=75"),
    ("Dallas Stadium", "Dallas", "USA", "https://digitalhub.fifa.com/transform/87ec691a-746b-4e25-a1eb-646ffad7014d/FWC-26-Stadiums-AT-T-Dallas?&io=transform:fill,width:1024&quality=75"),
    ("Houston Stadium", "Houston", "USA", "https://digitalhub.fifa.com/transform/b6858094-2992-474b-b087-f1e6710fac14/FWC-2026-Stadium-Houston-NRG-stadium?&io=transform:fill,width:1024&quality=75"),
    ("Kansas City Stadium", "Kansas City", "USA", "https://digitalhub.fifa.com/transform/824599e6-7b94-4b58-9fd4-4c3081aaf51f/FWWC-2023-Arrowhead-Stadium?&io=transform:fill,width:1024&quality=75"),
    ("Los Angeles Stadium", "Los Angeles", "USA", "https://digitalhub.fifa.com/transform/2563919b-e52e-43ba-a207-7c5556bf45f4/INGLEWOOD-CALIFORNIA-JANUARY-30-A-general-view-of-the-field-is-seen-before-the-NFC-Championship-Game-between-the-Los-Angeles-Rams-and-the-San-Francisco-49ers-at-SoFi-Stadium-on-January-30-2022-in-Inglewood-California-Photo-by-Ronald-Martinez-Getty-Images?&io=transform:fill,width:1024&quality=75"),
    ("Miami Stadium", "Miami", "USA", "https://digitalhub.fifa.com/transform/7f9dbb56-a934-43a1-8282-21e98729f737/Miami-Stadium-Hard-Rock-FWC-26?&io=transform:fill,width:1024&quality=75"),
    ("New York Stadium", "New York", "USA", "https://digitalhub.fifa.com/transform/ba606a0e-00f4-4b4a-af00-cac99d487379/FWWC-Stadiums?&io=transform:fill,width:1024&quality=75"),
    ("Philadelphia Stadium", "Philadelphia", "USA", "https://digitalhub.fifa.com/transform/7eb5c742-1344-4a91-9785-fc2e779009ba/FWWC-Stadiums?&io=transform:fill,width:1024&quality=75"),
    ("San Francisco Stadium", "San Francisco", "USA", "https://digitalhub.fifa.com/transform/1763b669-b92a-4520-acd8-3982f192e468/FWWC-Stadiums?&io=transform:fill,width:1024&quality=75"),
    ("Seattle Stadium", "Seattle", "USA", "https://digitalhub.fifa.com/transform/460c5587-d978-44f7-9ab0-c87781535bff/FWWC-Stadiums?&io=transform:fill,width:1024&quality=75"),
    ("Toronto Stadium", "Toronto", "Canadá", "https://digitalhub.fifa.com/transform/807f9b45-1a94-4a80-8755-5bfd06cfdd88/FIFA-2026-World-Cup-stadium-BMO-Field?&io=transform:fill,width:1024&quality=75"),
    ("Vancouver Stadium", "Vancouver", "Canadá", "https://digitalhub.fifa.com/transform/4f485a1d-f21f-4dfd-b120-eb2b02e79c6d/A-general-view-of-the-exterior-of-BC-Place-Vancouver-one-of-the-stadiums-being-used-for-FIFA-World-Cup-2026?&io=transform:fill,width:1024&quality=75"),
    ("Guadalajara Stadium", "Guadalajara", "México", "https://digitalhub.fifa.com/transform/551b0e79-4de4-4d13-be75-3d0407951977/FIFA-World-Cup-Stadium-Estadio-Akron?&io=transform:fill,width:1024&quality=75"),
    ("Mexico City Stadium", "Cidade do México", "México", "https://digitalhub.fifa.com/transform/c9c5b0fa-5362-41ef-b4a9-1b17cef69408/MEXICO-CITY-MEXICO-MAY-30-Aerial-view-of-Azteca-stadium-prior-the-Final-second-leg-match-between-Cruz-Azul-and-Santos-Laguna-as-part-of-the-Torneo-Guard1anes-2021-Liga-MX-at-Azteca-Stadium-on-May-30-2021-in-Mexico-City-Mexico-Photo-by-Hector-Vivas-Getty-Images?&io=transform:fill,width:1024&quality=75"),
    ("Monterrey Stadium", "Monterrey", "México", "https://digitalhub.fifa.com/transform/8ecdd76d-5391-4eda-9ed3-c8bbcea01849/FIFA-World-Cup-Stadium-Estadio-BBVA?&io=transform:fill,width:1024&quality=75"),
]

arbitros = [
    ("Raphael Claus", "Brasil"),
    ("Wilton Sampaio", "Brasil"),
    ("Facundo Tello", "Argentina"),
    ("Tori Penso", "Estados Unidos"),
    ("César Ramos", "México"),
    ("Danny Makkelie", "Países Baixos"),
    ("Szymon Marciniak", "Polônia"),
    ("Michael Oliver", "Inglaterra"),
    ("Ismail Elfath", "Estados Unidos"),
    ("Anderson Daronco", "Brasil"),
]

elencos_especiais = {
    "Brasil": [
        ("Alisson", 1, "Goleiro"),
        ("Danilo", 2, "Lateral"),
        ("Marquinhos", 3, "Zagueiro"),
        ("Gabriel Magalhães", 4, "Zagueiro"),
        ("Casemiro", 5, "Meio-campo"),
        ("Guilherme Arana", 6, "Lateral"),
        ("Vinícius Júnior", 7, "Atacante"),
        ("Bruno Guimarães", 8, "Meio-campo"),
        ("Richarlison", 9, "Atacante"),
        ("Lucas Paquetá", 10, "Meio-campo"),
        ("Rodrygo", 11, "Atacante"),
        ("Bento", 12, "Goleiro"),
        ("Bremer", 14, "Zagueiro"),
        ("André", 15, "Meio-campo"),
        ("Endrick", 18, "Atacante"),
    ],
    "Argentina": [
        ("Emiliano Martínez", 1, "Goleiro"),
        ("Molina", 4, "Lateral"),
        ("Cristian Romero", 13, "Zagueiro"),
        ("Otamendi", 19, "Zagueiro"),
        ("Tagliafico", 3, "Lateral"),
        ("De Paul", 7, "Meio-campo"),
        ("Enzo Fernández", 8, "Meio-campo"),
        ("Mac Allister", 20, "Meio-campo"),
        ("Messi", 10, "Atacante"),
        ("Julián Álvarez", 9, "Atacante"),
        ("Di María", 11, "Atacante"),
        ("Armani", 12, "Goleiro"),
        ("Paredes", 5, "Meio-campo"),
        ("Lisandro Martínez", 6, "Zagueiro"),
        ("Lautaro Martínez", 22, "Atacante"),
    ],
    "França": [
        ("Maignan", 1, "Goleiro"),
        ("Koundé", 5, "Lateral"),
        ("Upamecano", 4, "Zagueiro"),
        ("Saliba", 17, "Zagueiro"),
        ("Theo Hernández", 22, "Lateral"),
        ("Tchouaméni", 8, "Meio-campo"),
        ("Camavinga", 6, "Meio-campo"),
        ("Griezmann", 7, "Meio-campo"),
        ("Dembélé", 11, "Atacante"),
        ("Mbappé", 10, "Atacante"),
        ("Kolo Muani", 12, "Atacante"),
        ("Samba", 16, "Goleiro"),
        ("Konaté", 15, "Zagueiro"),
        ("Zaïre-Emery", 18, "Meio-campo"),
        ("Coman", 20, "Atacante"),
    ],
    "Marrocos": [
        ("Yassine Bounou", 1, "Goleiro"),
        ("Achraf Hakimi", 2, "Lateral"),
        ("Noussair Mazraoui", 3, "Lateral"),
        ("Sofyan Amrabat", 4, "Meio-campo"),
        ("Nayef Aguerd", 5, "Zagueiro"),
        ("Romain Saïss", 6, "Zagueiro"),
        ("Hakim Ziyech", 7, "Atacante"),
        ("Azzedine Ounahi", 8, "Meio-campo"),
        ("Youssef En-Nesyri", 9, "Atacante"),
        ("Sofiane Boufal", 17, "Atacante"),
        ("Munir El Kajoui", 12, "Goleiro"),
        ("Abde Ezzalzouli", 11, "Atacante"),
        ("Selim Amallah", 15, "Meio-campo"),
        ("Bilal El Khannouss", 23, "Meio-campo"),
        ("Ayoub El Kaabi", 19, "Atacante"),
    ],
}

# CRIAÇÃO DE TABELAS ---------------------------------
# Criando "uma ponte" entre o sistema e o banco de dados com base nas configurações estabelecidas
conn = psycopg2.connect(**DB_CONFIG)
# O cursor seria tipo uma pessoa que vai buscar ou fazer alguma coisa no banco de dados para você
cursor = conn.cursor()
# Excluir todas as tabelas do DB
cursor.execute("DROP TABLE IF EXISTS favoritos CASCADE")
cursor.execute("DROP TABLE IF EXISTS jogadores CASCADE")
cursor.execute("DROP TABLE IF EXISTS partidas CASCADE")
cursor.execute("DROP TABLE IF EXISTS arbitros CASCADE")
cursor.execute("DROP TABLE IF EXISTS estadios CASCADE")
cursor.execute("DROP TABLE IF EXISTS selecoes CASCADE")

# Criando uma tabela para seleçoes
cursor.execute(
    """
CREATE TABLE selecoes (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    codigo TEXT NOT NULL,
    grupo TEXT NOT NULL
)
"""
)
# Criando uma tabela para estadios
cursor.execute(
    """
CREATE TABLE estadios (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    cidade TEXT NOT NULL,
    pais TEXT NOT NULL,
    foto_url TEXT
)
"""
)
# Criando uma tabela para arbritos
cursor.execute(
    """
CREATE TABLE arbitros (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    pais TEXT NOT NULL
)
"""
)

# Criando uma tabela para partidas
cursor.execute(
    """
CREATE TABLE partidas (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    selecao_casa TEXT NOT NULL,
    selecao_fora TEXT NOT NULL,
    gols_casa INTEGER DEFAULT 0,
    gols_fora INTEGER DEFAULT 0,
    grupo TEXT NOT NULL,
    estadio_id INTEGER,
    arbitro_id INTEGER,
    CONSTRAINT fk_estadio FOREIGN KEY (estadio_id) REFERENCES estadios(id),
    CONSTRAINT fk_arbitro FOREIGN KEY (arbitro_id) REFERENCES arbitros(id)
)
"""
)

# Criando uma tabela para jogadores
cursor.execute(
    """
CREATE TABLE jogadores (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    nome TEXT NOT NULL,
    numero INTEGER NOT NULL,
    posicao TEXT NOT NULL,
    selecao TEXT NOT NULL,
    rating REAL NOT NULL,
    titular INTEGER NOT NULL,
    foto_url TEXT
)
"""
)

# Criando uma tabela para favoritos
cursor.execute(
    """
CREATE TABLE favoritos (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    partida_id INTEGER NOT NULL UNIQUE,
    CONSTRAINT fk_partida_favorita FOREIGN KEY (partida_id) REFERENCES partidas(id) ON DELETE CASCADE
)
"""
)

# INSERÇÃO DE VALORES NAS TABELAS ---------------------------------

# Inserindo dados na tabela com o INSERT INTO ... VALUES
# O "%s" é como se fosse um placeholder, ele reserva os lugares dos valores a serem inseridos, na mesma ordem das colunas.
for grupo, times in grupos.items():
    for nome, codigo in times:
        cursor.execute(
            "INSERT INTO selecoes (nome, codigo, grupo) VALUES (%s, %s, %s)",
            (nome, codigo, grupo),
        )

for estadio in estadios:
    cursor.execute(
        """
        INSERT INTO estadios (nome, cidade, pais, foto_url)
        VALUES (%s, %s, %s, %s)
    """,
        estadio,
    )

for arbitro in arbitros:
    cursor.execute(
        """
        INSERT INTO arbitros (nome, pais)
        VALUES (%s, %s)
    """,
        arbitro,
    )

# fetchall() é uma ferramenta que retorna todas os resultados que foram armazenados no cursor. Nesse caso, com o row[0], sempre vai pegar a primeira linha
cursor.execute("SELECT id FROM estadios ORDER BY id")
estadios_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM arbitros ORDER BY id")
arbitros_ids = [row[0] for row in cursor.fetchall()]

# Escolha do estádo e do árbitro de cada partida
idx_estadio = 0
idx_arbitro = 0

for grupo, times in grupos.items():
    nomes = [t[0] for t in times]  # Sempre vai pegar o primeiro item da tupla
    # O intertools.combination gera todas as combinações possíveis de dois times dentro do mesmo grupo.
    for casa, fora in itertools.combinations(nomes, 2):
        # Aqui garante que os índices dos estádios e árbitros não saim da lista, devido a incrementação no final do loop.
        estadio_id = estadios_ids[idx_estadio % len(estadios_ids)]
        arbitro_id = arbitros_ids[idx_arbitro % len(arbitros_ids)]

        cursor.execute(
            """
            INSERT INTO partidas (
                selecao_casa, selecao_fora, gols_casa, gols_fora, grupo, estadio_id, arbitro_id
            )
            VALUES (%s, %s, 0, 0, %s, %s, %s)
        """,
            (casa, fora, grupo, estadio_id, arbitro_id),
        )

        idx_estadio += 1
        idx_arbitro += 1

cursor.execute("SELECT nome FROM selecoes ORDER BY nome")
selecoes_db = [row[0] for row in cursor.fetchall()]

for selecao in selecoes_db:
    jogadores = elencos_especiais.get(selecao)

    if jogadores is None:
        jogadores = [
            (f"{selecao} Goleiro", 1, "Goleiro"),
            (f"{selecao} Lateral D", 2, "Lateral"),
            (f"{selecao} Zagueiro 1", 3, "Zagueiro"),
            (f"{selecao} Zagueiro 2", 4, "Zagueiro"),
            (f"{selecao} Meio 1", 5, "Meio-campo"),
            (f"{selecao} Lateral E", 6, "Lateral"),
            (f"{selecao} Atacante 1", 7, "Atacante"),
            (f"{selecao} Meio 2", 8, "Meio-campo"),
            (f"{selecao} Atacante 2", 9, "Atacante"),
            (f"{selecao} Meio 3", 10, "Meio-campo"),
            (f"{selecao} Atacante 3", 11, "Atacante"),
            (f"{selecao} Reserva 1", 12, "Goleiro"),
            (f"{selecao} Reserva 2", 13, "Zagueiro"),
            (f"{selecao} Reserva 3", 14, "Meio-campo"),
            (f"{selecao} Reserva 4", 15, "Atacante"),
        ]

    for idx, (nome, numero, posicao) in enumerate(jogadores):
        titular = 1 if idx < 11 else 0
        rating = round(random.uniform(6.2, 8.9), 1)

        cursor.execute(
            """
            INSERT INTO jogadores (nome, numero, posicao, selecao, rating, titular, foto_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
            (nome, numero, posicao, selecao, rating, titular, None),
        )

conn.commit()

print("Buscando fotos dos jogadores na API...")
cursor.execute("SELECT id, nome, selecao, foto_url FROM jogadores")
todos_jogadores = cursor.fetchall()

for jogador_id, nome_jogador, selecao, foto_atual in todos_jogadores:
    if foto_atual:
        continue

    foto = buscar_foto_jogador_api(nome_jogador, selecao)
    if not foto:
        foto = avatar_url(nome_jogador)

    cursor.execute(
        "UPDATE jogadores SET foto_url = %s WHERE id = %s", (foto, jogador_id)
    )
    print(f"{selecao} - {nome_jogador}")
    time.sleep(0.15)

conn.commit()
cursor.close()
conn.close()

print("Banco PostgreSQL criado com sucesso.")