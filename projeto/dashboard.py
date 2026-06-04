# -*- coding: utf-8 -*-
import random
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from services.data_loader import (
    carregar_dados,
    carregar_ids_favoritos,
    favoritar_partida,
    desfavoritar_partida,
)
from services.api_service import buscar_time_api, buscar_ultimos_eventos_time
from services.previsao import carregar_modelo_previsao, prever_partida
from services.estatisticas import (
    score_forma,
    confronto_direto_stats,
    montar_tabela_ultimos_jogos,
)

st.set_page_config(layout="wide", page_title="Copa do Mundo 2026")

components.html(
    """
<script>
function injectFab() {
    const parentDoc = window.parent.document;

    if (parentDoc.getElementById('fab-games-root')) return;

    const btn = parentDoc.createElement('div');
    btn.id = 'fab-games-root';
    btn.innerHTML = "GAMES";

    Object.assign(btn.style, {
        position: 'fixed',
        bottom: '25px',
        right: '25px',
        zIndex: '999999',
        background: 'linear-gradient(135deg,#22c55e,#16a34a)',
        color: 'white',
        padding: '16px 20px',
        borderRadius: '999px',
        fontWeight: 'bold',
        fontSize: '16px',
        boxShadow: '0 12px 30px rgba(0,0,0,0.5)',
        cursor: 'pointer',
        fontFamily: 'Arial, sans-serif'
    });

    btn.onclick = function() {
        const url = new URL(parentDoc.location.href);
        url.searchParams.set("games", "1");
        parentDoc.location.href = url.toString();
    };

    parentDoc.body.appendChild(btn);
}

setTimeout(injectFab, 500);
</script>
""",
    height=0,
)

if "partida_escolhida" not in st.session_state:
    st.session_state["partida_escolhida"] = None
if "fundo_time" not in st.session_state:
    st.session_state["fundo_time"] = None
if "mostrar_escalacao" not in st.session_state:
    st.session_state["mostrar_escalacao"] = False
if "formacao_casa" not in st.session_state:
    st.session_state["formacao_casa"] = None
if "formacao_fora" not in st.session_state:
    st.session_state["formacao_fora"] = None

if "games_open" not in st.session_state:
    st.session_state["games_open"] = False

if st.query_params.get("games") == "1":
    st.session_state["games_open"] = True


FUNDO_PADRAO = "https://livesport-ott-images.ssl.cdn.cra.cz/r900xfq60/f5d97f56-8392-4885-bc98-15be6ac186b5.avif"
FUNDO_SELECOES = {
    "Brasil": "https://media.gettyimages.com/id/2185657983/pt/foto/salvador-brazil-gerson-of-brazil-celebrates-with-teammates-after-scoring-the-teams-first-goal.jpg?s=612x612&w=0&k=20&c=EQW-CWmcEFbn2qTgnaCxwZ9lI4UkmPIlbaNQhhFNcX4=",
    "Argentina": "https://media.gettyimages.com/id/2233311679/pt/foto/buenos-aires-argentina-lionel-messi-of-argentina-and-his-teammates-celebrate-a-goal-during-the.jpg?s=612x612&w=0&k=20&c=n9qYDNgDXh6gMYDZk7FeaPoN0mBIGErFzSKQzNJqVJ4=",
    "França": "https://media.gettyimages.com/id/2245955244/pt/foto/team-of-france-during-the-fifa-world-cup-2026-qualifiers-match-between-france-and-ukraine-at.jpg?s=612x612&w=0&k=20&c=uHu0UHsjWV2e1iYCMPGnQh6T0uT-oJ4JZR5jlMlfG4k=",
    "México": "https://media.gettyimages.com/id/2247044584/pt/foto/torreon-mexico-israel-reyes-cesar-montes-and-raul-jimenez-of-mexico-walk-prior-an.jpg?s=612x612&w=0&k=20&c=fhthMv4L5gChwbO7JCAPcTGCOFjWPE98zPqoLl0FFP8=",
    "Alemanha": "https://media.gettyimages.com/id/2248390564/pt/foto/leipzig-germany-players-of-germany-look-on-ahead-of-the-fifa-world-cup-2026-qualifier-match.jpg?s=612x612&w=0&k=20&c=nnA2zuo3PyxGT13gy53qVPV4mxUkQ5rVZnrrHEl_-nI=",
    "Espanha": "https://media.gettyimages.com/id/2240459967/pt/foto/elche-spain-yeremy-pino-of-spain-celebrates-scoring-his-teams-first-goal-during-the-fifa-world.jpg?s=612x612&w=0&k=20&c=PRCUuexN5Hn0ZP3o1qHxP5zFQxPyCEYy5v7vVcG0TCU=",
    "Portugal": "https://media.gettyimages.com/id/2240659270/pt/foto/lisbon-portugal-cristiano-ronaldo-of-portugal-celebrates-with-teammates-after-scoring-a-goal.jpg?s=612x612&w=0&k=20&c=ti5hSWglXz3wewojRMnx3yOARlqjXmf0o6Ez_DeO3TE=",
    "Marrocos": "https://media.gettyimages.com/id/2233201940/pt/foto/moroccos-players-celebrate-scoring-during-the-fifa-world-cup-2026-group-e-african.jpg?s=612x612&w=0&k=20&c=FrSIxv46AOQaK9V5vaSTYh9o7z95LLwobed5xUcRpvE=",
}

fundo_atual = FUNDO_SELECOES.get(st.session_state["fundo_time"], FUNDO_PADRAO)

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{fundo_atual}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        background: rgba(5, 10, 18, 0.82);
        z-index: -1;
    }}
    .block-container {{
        padding-top: 1.3rem;
        padding-bottom: 2rem;
    }}
    h1, h2, h3, h4, h5, h6, p, label, div, span {{
        color: white;
    }}
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px;
        background: rgba(8, 12, 20, 0.78);
        padding: 10px;
        border-radius: 16px;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255,255,255,0.06);
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 42px;
        background: linear-gradient(180deg, rgba(22,27,34,0.95), rgba(11,15,20,0.95));
        border-radius: 12px;
        padding: 8px 16px;
        color: #d1d5db;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.08);
        transition: all 0.22s ease;
    }}
    .stTabs [data-baseweb="tab"]:hover {{
        background: linear-gradient(180deg, rgba(30,36,46,0.98), rgba(14,18,26,0.98));
        color: #22c55e;
        border-color: rgba(34,197,94,0.65);
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(0,0,0,0.28);
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg,#0f172a,#14532d) !important;
        color: white !important;
        border: 1px solid rgba(34,197,94,0.7) !important;
        box-shadow: 0 0 18px rgba(34,197,94,0.25);
    }}
    .stTabs [data-baseweb="tab-highlight"] {{
        display: none;
    }}
    .stButton > button {{
        width: 100%;
        background: linear-gradient(180deg, #111827, #0b1220);
        color: #f9fafb;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 12px;
        font-weight: 600;
        padding: 0.55rem 0.9rem;
        transition: all 0.22s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.18);
    }}
    .stButton > button:hover {{
        background: linear-gradient(180deg, #172033, #0f172a);
        color: #22c55e;
        border-color: rgba(34,197,94,0.65);
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 8px 22px rgba(0,0,0,0.28);
    }}
    div[data-baseweb="select"] > div {{
        background: rgba(10, 15, 24, 0.85) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }}
    .custom-card {{
        background: linear-gradient(180deg, rgba(11,15,20,0.88), rgba(17,24,39,0.88));
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.08);
        padding: 16px;
        text-align: center;
        margin-bottom: 12px;
        transition: all 0.22s ease;
        box-shadow: 0 6px 18px rgba(0,0,0,0.18);
    }}
    .custom-card:hover {{
        transform: translateY(-4px) scale(1.02);
        border-color: rgba(34,197,94,0.55);
        box-shadow: 0 10px 28px rgba(0,0,0,0.28);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

df_selecoes, df_partidas, df_jogadores, df_estadios, df_arbitros, df_hist = (
    carregar_dados()
)
favoritos_ids = carregar_ids_favoritos()
map_codigos = dict(zip(df_selecoes["nome"], df_selecoes["codigo"]))


def render_forma_badges(sequencia):
    mapa_cor = {"V": "#16a34a", "E": "#111827", "D": "#ea580c"}

    html = '<div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:8px;">'
    for item in sequencia:
        cor = mapa_cor.get(item, "#374151")
        html += f"""
<div style="
width:34px;
height:34px;
border-radius:10px;
display:flex;
align-items:center;
justify-content:center;
background:{cor};
color:white;
font-weight:bold;
font-size:14px;
box-shadow:0 4px 10px rgba(0,0,0,0.18);
">{item}</div>
"""
    html += "</div>"
    components.html(html, height=60)


FORMACOES_DISPONIVEIS = [
    [4, 3, 3],
    [4, 4, 2],
    [4, 2, 3, 1],
    [4, 1, 4, 1],
    [4, 4, 1, 1],
    [3, 5, 2],
    [3, 4, 3],
    [5, 3, 2],
]


def formacao_para_texto(formacao):
    return " - ".join(str(x) for x in formacao)


def gerar_formacao_aleatoria():
    return random.choice(FORMACOES_DISPONIVEIS)


def posicoes_time_por_formacao(formacao, lado="esquerda"):
    if lado == "esquerda":
        x_gk, x_inicio, x_fim = 10, 24, 52
    else:
        x_gk, x_inicio, x_fim = 90, 76, 48

    coords = [(x_gk, 50, "centro")]
    qtd_linhas = len(formacao)

    if qtd_linhas == 1:
        xs = [x_inicio]
    else:
        passo = (x_fim - x_inicio) / (qtd_linhas - 1)
        xs = [x_inicio + i * passo for i in range(qtd_linhas)]

    for linha_idx, qtd in enumerate(formacao):
        x = xs[linha_idx]

        if qtd == 1:
            ys = [50]
        else:
            margem_topo = 18
            margem_base = 82
            passo_y = (margem_base - margem_topo) / (qtd - 1)
            ys = [margem_topo + i * passo_y for i in range(qtd)]

        for jogador_idx, y in enumerate(ys):
            if qtd == 1:
                setor = "centro"
            elif jogador_idx == 0:
                setor = "direita"
            elif jogador_idx == qtd - 1:
                setor = "esquerda"
            else:
                setor = "centro"

            coords.append((x, y, setor))

    return coords


def posicao_curta(posicao: str, numero: int, idx: int, setor: str = "") -> str:
    pos = (posicao or "").strip().lower()

    if "goleiro" in pos:
        return "GK"
    if "zagueiro" in pos:
        return "CB"
    if "lateral" in pos:
        return "RB" if idx in [1, 2] else "LB"
    if "meio" in pos:
        if setor == "centro":
            return "CM"
        if setor == "esquerda":
            return "LM"
        if setor == "direita":
            return "RM"
        return "CM"
    if "atac" in pos:
        if setor == "centro":
            return "ST"
        if setor == "esquerda":
            return "LW"
        if setor == "direita":
            return "RW"
        return "ST"

    mapa_numero = {
        1: "GK",
        2: "RB",
        3: "CB",
        4: "CB",
        5: "LB",
        6: "CM",
        7: "RW",
        8: "CM",
        9: "ST",
        10: "CM",
        11: "LW",
    }
    return mapa_numero.get(numero, "PL")


def glow_por_rating(rating: float) -> str:
    try:
        r = float(rating)
    except Exception:
        r = 6.5

    if r >= 8.5:
        return "0 0 18px rgba(250,204,21,0.95), 0 0 34px rgba(250,204,21,0.45)"
    if r >= 8.0:
        return "0 0 14px rgba(34,197,94,0.85), 0 0 24px rgba(34,197,94,0.35)"
    if r >= 7.0:
        return "0 0 10px rgba(59,130,246,0.75), 0 0 18px rgba(59,130,246,0.25)"
    return "0 0 8px rgba(255,255,255,0.18)"


def melhor_jogador_do_time(titulares: list) -> int:
    if not titulares:
        return -1

    melhor_idx = 0
    melhor_nota = -999.0
    for i, j in enumerate(titulares):
        try:
            nota = float(j.get("rating", 0))
        except Exception:
            nota = 0.0

        if nota > melhor_nota:
            melhor_nota = nota
            melhor_idx = i

    return melhor_idx


def bandeira_url(codigo: str) -> str:
    codigo = (codigo or "").strip().lower()
    if len(codigo) != 2 or not codigo.isalpha():
        return "https://flagcdn.com/w40/un.png"
    return f"https://flagcdn.com/w40/{codigo}.png"


def render_card_partida(
    casa, fora, codigo_casa, codigo_fora, dia, hora, grupo, estadio, arbitro
):
    html = f"""
    <div style="
        background:linear-gradient(135deg,#111827,#0b1220);
        padding:16px;border-radius:14px;border:1px solid rgba(255,255,255,0.08);
        color:white;font-family:Arial,sans-serif;min-height:140px;box-sizing:border-box;">
        <div style="display:flex;align-items:center;justify-content:space-between;font-size:15px;font-weight:600;gap:10px;">
            <div style="display:flex;align-items:center;gap:8px;">
                <img src="{bandeira_url(codigo_casa)}" width="28"><span>{casa}</span>
            </div>
            <div style="color:#9ca3af;font-weight:bold;">VS</div>
            <div style="display:flex;align-items:center;gap:8px;">
                <span>{fora}</span><img src="{bandeira_url(codigo_fora)}" width="28">
            </div>
        </div>
        <div style="text-align:right;font-size:12px;color:#9ca3af;margin-top:6px;">{dia} • {hora}</div>
        <div style="font-size:12px;color:#cbd5e1;margin-top:8px;">Grupo {grupo}</div>
        <div style="font-size:12px;color:#cbd5e1;margin-top:4px;">🏟 {estadio}</div>
        <div style="font-size:12px;color:#cbd5e1;margin-top:4px;">🧑‍⚖️ {arbitro}</div>
    </div>
    """
    components.html(html, height=170)


def get_elenco(selecao: str):
    elenco = df_jogadores[df_jogadores["selecao"] == selecao].copy()
    if elenco.empty:
        return [], []

    titulares = elenco[elenco["titular"] == 1].copy()
    reservas = elenco[elenco["titular"] == 0].copy()

    if len(titulares) < 11:
        faltam = 11 - len(titulares)
        completar = reservas.head(faltam)
        titulares = pd.concat([titulares, completar])
        reservas = reservas.iloc[faltam:]

    return titulares.head(11).to_dict("records"), reservas.to_dict("records")


def selecionar_partida(casa: str, fora: str):
    atual = st.session_state.get("partida_escolhida")

    mesma_partida_aberta = (
        atual
        and atual.get("casa") == casa
        and atual.get("fora") == fora
        and st.session_state.get("mostrar_escalacao") is True
    )

    if mesma_partida_aberta:
        st.session_state["mostrar_escalacao"] = False
        st.session_state["formacao_casa"] = None
        st.session_state["formacao_fora"] = None
    else:
        st.session_state["partida_escolhida"] = {"casa": casa, "fora": fora}
        st.session_state["mostrar_escalacao"] = True
        st.session_state["formacao_casa"] = gerar_formacao_aleatoria()
        st.session_state["formacao_fora"] = gerar_formacao_aleatoria()


def render_campo_duplo(casa: str, fora: str):
    titulares_casa, reservas_casa = get_elenco(casa)
    titulares_fora, reservas_fora = get_elenco(fora)

    if len(titulares_casa) < 11 or len(titulares_fora) < 11:
        st.warning("Não foi possível montar as duas escalações completas.")
        return

    formacao_casa = st.session_state.get("formacao_casa") or [4, 3, 3]
    formacao_fora = st.session_state.get("formacao_fora") or [4, 3, 3]

    st.markdown("---")
    head1, head2 = st.columns([7, 1])

    with head1:
        st.subheader(f"Escalações: {casa} x {fora}")
        st.caption(
            f"{casa}: {formacao_para_texto(formacao_casa)} | {fora}: {formacao_para_texto(formacao_fora)}"
        )

    with head2:
        if st.button(
            "Fechar escalação", key="fechar_escalacao_topo", use_container_width=True
        ):
            st.session_state["mostrar_escalacao"] = False
            st.session_state["formacao_casa"] = None
            st.session_state["formacao_fora"] = None
            st.rerun()

    pos_esquerda = posicoes_time_por_formacao(formacao_casa, lado="esquerda")
    pos_direita = posicoes_time_por_formacao(formacao_fora, lado="direita")

    melhor_casa = melhor_jogador_do_time(titulares_casa)
    melhor_fora = melhor_jogador_do_time(titulares_fora)

    def player_html(jogador, left, top, bg, idx, melhor=False, setor="centro"):
        foto = str(jogador.get("foto_url") or "").strip()
        numero = jogador.get("numero", "")
        nome = jogador.get("nome", "Jogador")
        rating = jogador.get("rating", "")
        posicao = jogador.get("posicao", "")
        pos_curta = posicao_curta(
            posicao, int(numero) if str(numero).isdigit() else 0, idx, setor
        )
        glow = glow_por_rating(rating)

        melhor_badge = ""
        if melhor:
            melhor_badge = """
            <div style="
                position:absolute;
                top:-10px;
                right:-10px;
                width:24px;
                height:24px;
                border-radius:50%;
                background:linear-gradient(135deg,#fde68a,#f59e0b);
                color:#111827;
                display:flex;
                align-items:center;
                justify-content:center;
                font-size:14px;
                font-weight:900;
                box-shadow:0 0 16px rgba(250,204,21,0.85);
                z-index:8;
            ">★</div>
            """

        if foto:
            foto_html = f"""
            <img src="{foto}" style="
                width:42px;
                height:42px;
                border-radius:50%;
                object-fit:cover;
                border:2px solid rgba(255,255,255,0.85);
                box-shadow:{glow};
                background:#0f172a;
            ">
            """
        else:
            foto_html = f"""
            <div style="
                width:42px;
                height:42px;
                border-radius:50%;
                background:#0f172a;
                border:2px solid rgba(255,255,255,0.85);
                box-shadow:{glow};
            "></div>
            """

        return f"""
        <div style="
            position:absolute;
            left:{left}%;
            top:{top}%;
            transform:translate(-50%, -50%);
            text-align:center;
            width:96px;
            font-family:Arial, sans-serif;
            color:white;
            animation: fadeUp 0.45s ease;
            z-index:6;
        ">
            <div style="position:relative; display:inline-block;">
                {foto_html}
                {melhor_badge}
            </div>

            <div style="
                margin-top:6px;
                display:inline-flex;
                align-items:center;
                gap:6px;
                justify-content:center;
                background:{bg};
                color:white;
                border-radius:999px;
                padding:5px 10px;
                font-size:11px;
                font-weight:800;
                box-shadow:0 8px 16px rgba(0,0,0,0.25);
            ">
                <span>#{numero}</span>
                <span>{pos_curta}</span>
            </div>

            <div style="
                margin-top:6px;
                font-size:11px;
                line-height:1.15;
                background:rgba(3, 7, 18, 0.76);
                border-radius:10px;
                padding:5px 6px;
                white-space:nowrap;
                overflow:hidden;
                text-overflow:ellipsis;
                box-shadow:0 6px 12px rgba(0,0,0,0.18);
            ">
                {nome}
            </div>

            <div style="
                margin-top:4px;
                display:inline-block;
                background:#0f172a;
                color:#facc15;
                border-radius:8px;
                padding:2px 6px;
                font-weight:800;
                font-size:11px;
                box-shadow:{glow};
            ">
                 {rating}
            </div>
        </div>
        """

    def substitutions_html(reservas, titulo, alinhamento):
        itens = ""
        for j in reservas[:5]:
            numero = j.get("numero", "")
            nome = j.get("nome", "")
            rating = j.get("rating", "")
            posicao = posicao_curta(
                j.get("posicao", ""),
                int(numero) if str(numero).isdigit() else 0,
                0,
                "centro",
            )

            itens += f"""
            <div style="
                display:flex;
                align-items:center;
                justify-content:space-between;
                background:rgba(255,255,255,0.06);
                border-radius:10px;
                padding:6px 8px;
                margin-bottom:6px;
                font-size:11px;
                gap:8px;
            ">
                <div style="display:flex; flex-direction:column; text-align:left;">
                    <span><b>{numero}</b> {nome}</span>
                    <span style="color:#93c5fd; font-size:10px;">{posicao}</span>
                </div>
                <div style="
                    background:#0f172a;
                    color:#facc15;
                    border-radius:8px;
                    padding:2px 6px;
                    font-weight:bold;
                ">
                    {rating}
                </div>
            </div>
            """

        side = "left:12px;" if alinhamento == "left" else "right:12px;"
        return f"""
        <div style="
            position:absolute;
            {side}
            bottom:12px;
            width:230px;
            background:rgba(0,0,0,0.30);
            border:1px solid rgba(255,255,255,0.10);
            border-radius:14px;
            padding:10px;
            color:white;
            font-family:Arial, sans-serif;
            backdrop-filter: blur(4px);
            z-index:7;
        ">
            <div style="font-weight:bold; margin-bottom:8px;">{titulo}</div>
            {itens}
        </div>
        """

    jogadores_html = ""
    for idx, (jogador, (left, top, setor)) in enumerate(
        zip(titulares_casa, pos_esquerda)
    ):
        jogadores_html += player_html(
            jogador,
            left,
            top,
            "linear-gradient(135deg, #22c55e, #16a34a)",
            idx=idx,
            melhor=(idx == melhor_casa),
            setor=setor,
        )

    for idx, (jogador, (left, top, setor)) in enumerate(
        zip(titulares_fora, pos_direita)
    ):
        jogadores_html += player_html(
            jogador,
            left,
            top,
            "linear-gradient(135deg, #f59e0b, #ef4444)",
            idx=idx,
            melhor=(idx == melhor_fora),
            setor=setor,
        )

    heatspots = """
    <div style="
        position:absolute;
        left:28%;
        top:28%;
        width:150px;
        height:150px;
        border-radius:50%;
        background:radial-gradient(circle, rgba(250,204,21,0.22) 0%, rgba(250,204,21,0.08) 35%, rgba(250,204,21,0.0) 72%);
        filter: blur(10px);
        z-index:1;
    "></div>

    <div style="
        position:absolute;
        left:58%;
        top:18%;
        width:180px;
        height:180px;
        border-radius:50%;
        background:radial-gradient(circle, rgba(239,68,68,0.18) 0%, rgba(239,68,68,0.07) 35%, rgba(239,68,68,0.0) 75%);
        filter: blur(12px);
        z-index:1;
    "></div>

    <div style="
        position:absolute;
        left:43%;
        top:52%;
        width:220px;
        height:220px;
        border-radius:50%;
        background:radial-gradient(circle, rgba(59,130,246,0.13) 0%, rgba(59,130,246,0.05) 38%, rgba(59,130,246,0.0) 78%);
        filter: blur(14px);
        z-index:1;
    "></div>
    """

    campo_html = f"""
    <html>
    <head>
    <style>
        body {{
            margin:0;
            background:transparent;
        }}
        @keyframes fadeUp {{
            from {{ opacity:0; transform:translate(-50%, -44%); }}
            to {{ opacity:1; transform:translate(-50%, -50%); }}
        }}
    </style>
    </head>
    <body>
    <div style="
        position:relative;
        width:100%;
        height:760px;
        border-radius:20px;
        overflow:hidden;
        background:
            linear-gradient(rgba(0,0,0,0.08), rgba(0,0,0,0.08)),
            repeating-linear-gradient(
                90deg,
                #14532d 0%,
                #14532d 7%,
                #166534 7%,
                #166534 14%
            );
        border:1px solid rgba(255,255,255,0.12);
        box-shadow:0 12px 28px rgba(0,0,0,0.25);
        font-family:Arial, sans-serif;
    ">
        {heatspots}

        <div style="position:absolute; inset:0; z-index:2;">
            <div style="position:absolute; left:50%; top:0; width:2px; height:100%; background:rgba(255,255,255,0.75); transform:translateX(-50%);"></div>
            <div style="position:absolute; left:50%; top:50%; width:110px; height:110px; border:2px solid rgba(255,255,255,0.75); border-radius:50%; transform:translate(-50%, -50%);"></div>

            <div style="position:absolute; left:0; top:22%; width:15%; height:56%; border:2px solid rgba(255,255,255,0.75); border-left:none;"></div>
            <div style="position:absolute; left:0; top:36%; width:5.5%; height:28%; border:2px solid rgba(255,255,255,0.75); border-left:none;"></div>

            <div style="position:absolute; right:0; top:22%; width:15%; height:56%; border:2px solid rgba(255,255,255,0.75); border-right:none;"></div>
            <div style="position:absolute; right:0; top:36%; width:5.5%; height:28%; border:2px solid rgba(255,255,255,0.75); border-right:none;"></div>
        </div>

        <div style="
            position:absolute;
            left:1%;
            top:2%;
            background:rgba(6, 18, 28, 0.72);
            color:white;
            padding:6px 12px;
            border-radius:10px;
            font-weight:700;
            z-index:8;
        ">{casa}</div>

        <div style="
            position:absolute;
            right:1%;
            top:2%;
            background:rgba(6, 18, 28, 0.72);
            color:white;
            padding:6px 12px;
            border-radius:10px;
            font-weight:700;
            z-index:8;
        ">{fora}</div>

        {jogadores_html}
        {substitutions_html(reservas_casa, "Reservas", "left")}
        {substitutions_html(reservas_fora, "Reservas", "right")}
    </div>
    </body>
    </html>
    """
    components.html(campo_html, height=780, scrolling=False)


def render_lista_partidas(df_filtrado: pd.DataFrame, origem: str):
    global favoritos_ids

    if df_filtrado.empty:
        st.info("Nenhum jogo encontrado.")
        return

    grupos = sorted(df_filtrado["grupo"].dropna().unique())

    for i in range(0, len(grupos), 2):
        col1, col2 = st.columns(2)

        for idx, col in enumerate([col1, col2]):
            if i + idx >= len(grupos):
                continue

            grupo = grupos[i + idx]

            with col:
                st.markdown(f"### Grupo {grupo}")
                jogos = df_filtrado[df_filtrado["grupo"] == grupo].reset_index(
                    drop=True
                )

                for j, row in jogos.iterrows():
                    partida_id = int(row["id"])
                    casa = row["selecao_casa"]
                    fora = row["selecao_fora"]

                    dia = f"{10 + (j % 10):02d}/06"
                    hora = f"{14 + (j % 6):02d}:00"

                    estadio = (
                        f"{row['estadio_nome']} - {row['estadio_cidade']}"
                        if pd.notna(row["estadio_nome"])
                        else "Estádio a definir"
                    )
                    arbitro = (
                        row["arbitro_nome"]
                        if pd.notna(row["arbitro_nome"])
                        else "Árbitro a definir"
                    )

                    codigo_casa = map_codigos.get(casa, "")
                    codigo_fora = map_codigos.get(fora, "")

                    c1, c2, c3 = st.columns([4, 1.1, 1.1])

                    with c1:
                        render_card_partida(
                            casa,
                            fora,
                            codigo_casa,
                            codigo_fora,
                            dia,
                            hora,
                            grupo,
                            estadio,
                            arbitro,
                        )

                    with c2:
                        atual = st.session_state.get("partida_escolhida")
                        aberta = (
                            atual
                            and atual.get("casa") == casa
                            and atual.get("fora") == fora
                            and st.session_state.get("mostrar_escalacao") is True
                        )
                        texto_botao = "Fechar" if aberta else "Escalação"

                        if st.button(
                            texto_botao,
                            key=f"{origem}_esc_{partida_id}",
                            use_container_width=True,
                        ):
                            selecionar_partida(casa, fora)
                            st.rerun()

                    with c3:
                        eh_favorito = partida_id in favoritos_ids
                        texto = "★ Favorito" if eh_favorito else "☆ Favoritar"

                        if st.button(
                            texto,
                            key=f"{origem}_fav_{partida_id}",
                            use_container_width=True,
                        ):
                            if eh_favorito:
                                desfavoritar_partida(partida_id)
                            else:
                                favoritar_partida(partida_id)

                            st.cache_data.clear()
                            st.rerun()


if st.session_state["partida_escolhida"] and st.session_state["mostrar_escalacao"]:
    render_campo_duplo(
        st.session_state["partida_escolhida"]["casa"],
        st.session_state["partida_escolhida"]["fora"],
    )

st.title("Copa do Mundo 2026")
st.caption("Plataforma interativa de análise da Copa do Mundo FIFA")

abas = st.tabs(
    [
        "Todos",
        "Favoritos",
        "Competições",
        "Seleções",
        "Estatísticas",
        "API",
        "Previsão",
        "Estádios",
        "Árbitros",
        "Jogadores",
    ]
)

with abas[0]:
    st.subheader("Todos os jogos")
    render_lista_partidas(df_partidas, "todos")

with abas[1]:
    st.subheader("Favoritos")
    favoritos_ids = carregar_ids_favoritos()
    if not favoritos_ids:
        st.info("Você ainda não favoritou nenhuma partida.")
    else:
        df_fav = df_partidas[df_partidas["id"].isin(list(favoritos_ids))].copy()
        render_lista_partidas(df_fav, "favoritos")

with abas[2]:
    st.subheader("Competições")
    grupos = sorted(df_partidas["grupo"].dropna().unique())
    grupo_sel = st.selectbox("Filtrar por grupo", ["Todos"] + grupos)
    df_comp = (
        df_partidas
        if grupo_sel == "Todos"
        else df_partidas[df_partidas["grupo"] == grupo_sel]
    )
    render_lista_partidas(df_comp, "competicoes")

with abas[3]:
    st.subheader("Seleções interativas")
    st.caption("Passe o mouse para destacar. Clique para trocar o fundo.")

    cols = st.columns(4)
    idx = 0
    for _, row in df_selecoes.iterrows():
        nome = row["nome"]
        codigo = row["codigo"]

        with cols[idx % 4]:
            st.markdown(
                f"""
            <div class="custom-card">
                <img src="{bandeira_url(codigo)}" width="60">
                <div style="margin-top:8px;color:white;font-weight:600;">{nome}</div>
            </div>
            """,
                unsafe_allow_html=True,
            )

            if st.button(
                f"Selecionar {nome}", key=f"sel_{nome}", use_container_width=True
            ):
                st.session_state["fundo_time"] = nome
                st.rerun()
        idx += 1

    if st.button("Restaurar fundo padrão", use_container_width=True):
        st.session_state["fundo_time"] = None
        st.rerun()

with abas[4]:
    st.subheader("Estatísticas comparativas")

    selecoes_validas_stats = sorted(df_selecoes["nome"].unique())

    c1, c2 = st.columns(2)
    with c1:
        time_a = st.selectbox("Seleção A", selecoes_validas_stats, key="stats_a")
    with c2:
        idx_b = 1 if len(selecoes_validas_stats) > 1 else 0
        time_b = st.selectbox(
            "Seleção B", selecoes_validas_stats, index=idx_b, key="stats_b"
        )

    if time_a == time_b:
        st.info("Escolha duas seleções diferentes para comparar.")
    else:
        forma_a, seq_a = score_forma(df_hist, time_a, n=5)
        forma_b, seq_b = score_forma(df_hist, time_b, n=5)
        h2h = confronto_direto_stats(df_hist, time_a, time_b)

        st.markdown("### Forma recente")
        f1, f2 = st.columns(2)

        with f1:
            st.markdown(f"#### {time_a}")
            st.metric("Overall Form", f"{forma_a}/100")
            render_forma_badges(seq_a)

        with f2:
            st.markdown(f"#### {time_b}")
            st.metric("Overall Form", f"{forma_b}/100")
            render_forma_badges(seq_b)

        st.markdown("---")
        st.markdown("### Confronto direto")

        if h2h["partidas"] == 0:
            st.info(
                "Não há confrontos diretos suficientes entre essas seleções no histórico carregado."
            )
        else:
            st.caption(f"Partidas jogadas: {h2h['partidas']} | Desde {h2h['desde']}")

            a1, a2, a3 = st.columns(3)
            with a1:
                st.metric(f"Vitórias {time_a}", h2h["vitorias_a"])
            with a2:
                st.metric("Empates", h2h["empates"])
            with a3:
                st.metric(f"Vitórias {time_b}", h2h["vitorias_b"])

            b1, b2 = st.columns(2)
            with b1:
                st.markdown(
                    f"""
                <div class="custom-card">
                    <h4 style="margin-bottom:10px;">{time_a}</h4>
                    <p><b>Maior vitória:</b> {h2h["maior_vitoria_a"] or "N/A"}</p>
                    <p><b>Total de gols:</b> {h2h["gols_a"]}</p>
                    <p><b>Média de gols:</b> {h2h["media_gols_a"]}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

            with b2:
                st.markdown(
                    f"""
                <div class="custom-card">
                    <h4 style="margin-bottom:10px;">{time_b}</h4>
                    <p><b>Maior vitória:</b> {h2h["maior_vitoria_b"] or "N/A"}</p>
                    <p><b>Total de gols:</b> {h2h["gols_b"]}</p>
                    <p><b>Média de gols:</b> {h2h["media_gols_b"]}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )

        st.markdown("---")
        st.markdown("### Últimos jogos")

        ult_a = montar_tabela_ultimos_jogos(df_hist, time_a, n=5)
        ult_b = montar_tabela_ultimos_jogos(df_hist, time_b, n=5)

        u1, u2 = st.columns(2)
        with u1:
            st.markdown(f"#### {time_a}")
            if ult_a.empty:
                st.info("Sem jogos suficientes.")
            else:
                st.dataframe(ult_a, use_container_width=True, hide_index=True)

        with u2:
            st.markdown(f"#### {time_b}")
            if ult_b.empty:
                st.info("Sem jogos suficientes.")
            else:
                st.dataframe(ult_b, use_container_width=True, hide_index=True)

with abas[5]:
    st.subheader("API TheSportsDB")
    st.caption("Fonte: TheSportsDB (API gratuita).")

    opcoes_times = sorted(df_selecoes["nome"].unique())
    time_sel = st.selectbox("Seleção para consultar na API", opcoes_times)

    if st.button("Buscar estatísticas", key="buscar_api", use_container_width=True):
        team_info, err_team = buscar_time_api(time_sel)

        if err_team:
            st.error(f"Erro ao buscar time: {err_team}")
        else:
            c1, c2 = st.columns([1, 3])

            with c1:
                badge = team_info.get("strBadge")
                if badge:
                    st.image(badge, use_container_width=True)

            with c2:
                st.markdown(f"### {team_info.get('strTeam', time_sel)}")
                st.write(f"País: {team_info.get('strCountry', 'N/A')}")
                st.write(f"Liga: {team_info.get('strLeague', 'N/A')}")
                st.write(f"Estádio: {team_info.get('strStadium', 'N/A')}")

            eventos, err_eventos = buscar_ultimos_eventos_time(time_sel)
            st.markdown("#### Últimos jogos")

            if err_eventos:
                st.warning(err_eventos)
            elif not eventos:
                st.info("Nenhum evento encontrado.")
            else:
                linhas = []
                for ev in eventos[:8]:
                    linhas.append(
                        {
                            "Data": ev.get("dateEvent"),
                            "Competição": ev.get("strLeague"),
                            "Casa": ev.get("strHomeTeam"),
                            "Placar": f"{ev.get('intHomeScore', '-')}"
                            + " x "
                            + f"{ev.get('intAwayScore', '-')}",
                            "Fora": ev.get("strAwayTeam"),
                        }
                    )
                st.dataframe(
                    pd.DataFrame(linhas), use_container_width=True, hide_index=True
                )

with abas[6]:
    st.subheader("Previsão com IA")

    model, scaler, classes, feature_names = carregar_modelo_previsao()

    if model is None:
        st.warning("Modelo ainda não treinado. Rode: python treinar_modelo_xgboost.py")
    else:
        selecoes_validas = sorted(df_jogadores["selecao"].unique())

        c1, c2 = st.columns(2)
        with c1:
            time_casa = st.selectbox("Time da casa", selecoes_validas, key="pred_casa")
        with c2:
            time_fora = st.selectbox(
                "Time visitante",
                selecoes_validas,
                index=1 if len(selecoes_validas) > 1 else 0,
                key="pred_fora",
            )

        if time_casa == time_fora:
            st.info("Escolha seleções diferentes.")
        else:
            if st.button("Gerar previsão", use_container_width=True):
                probs = prever_partida(
                    model, scaler, classes, feature_names, time_casa, time_fora
                )

                st.markdown(f"### {time_casa} x {time_fora}")

                d1, d2, d3 = st.columns(3)
                with d1:
                    st.metric("Vitória casa", f"{probs['casa'] * 100:.1f}%")
                with d2:
                    st.metric("Empate", f"{probs['empate'] * 100:.1f}%")
                with d3:
                    st.metric("Vitória visitante", f"{probs['fora'] * 100:.1f}%")

                mapa_final = {
                    "casa": f"Tendência: {time_casa}",
                    "empate": "Tendência: Empate",
                    "fora": f"Tendência: {time_fora}",
                }

                st.success(mapa_final[probs["predicao_final"]])

                df_probs = pd.DataFrame(
                    {
                        "Resultado": ["Vitória casa", "Empate", "Vitória visitante"],
                        "Probabilidade": [
                            probs["casa"],
                            probs["empate"],
                            probs["fora"],
                        ],
                    }
                )
                st.bar_chart(df_probs.set_index("Resultado"))

with abas[7]:
    st.subheader("Estádios")
    cols = st.columns(2)

    for i, (_, row) in enumerate(df_estadios.iterrows()):
        with cols[i % 2]:
            if row["foto_url"]:
                st.image(row["foto_url"], use_container_width=True)
            st.markdown(f"**{row['nome']}**")
            st.write(f"{row['cidade']} - {row['pais']}")
            st.markdown("---")

with abas[8]:
    st.subheader("Árbitros")

    for _, arb in df_arbitros.iterrows():
        st.markdown(f"### {arb['nome']} ({arb['pais']})")

        jogos = df_partidas[df_partidas["arbitro_nome"] == arb["nome"]][
            ["selecao_casa", "selecao_fora", "grupo", "estadio_nome"]
        ].copy()

        if jogos.empty:
            st.info("Nenhuma partida vinculada.")
        else:
            jogos.columns = ["Casa", "Fora", "Grupo", "Estádio"]
            st.dataframe(jogos, use_container_width=True, hide_index=True)

with abas[9]:
    st.subheader("Jogadores")
    selecao_sel = st.selectbox("Seleção", sorted(df_jogadores["selecao"].unique()))

    elenco = df_jogadores[df_jogadores["selecao"] == selecao_sel].copy()
    elenco = elenco.rename(
        columns={
            "nome": "Jogador",
            "numero": "Número",
            "posicao": "Posição",
            "rating": "Nota",
            "titular": "Titular",
        }
    )
    elenco["Titular"] = elenco["Titular"].map({1: "Sim", 0: "Reserva"})

    st.dataframe(
        elenco[["Número", "Jogador", "Posição", "Nota", "Titular"]],
        use_container_width=True,
        hide_index=True,
    )
