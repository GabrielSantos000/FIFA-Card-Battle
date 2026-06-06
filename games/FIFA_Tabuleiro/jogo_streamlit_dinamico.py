import streamlit as st
import streamlit.components.v1 as components
import random
import json
import time
import os
from datetime import datetime
from quiz_generator import QuizGenerator
from casas_efeito import *

# Configuração da página
st.set_page_config(page_title="Copa do Mundo - Jogo de Tabuleiro", layout="wide", initial_sidebar_state="collapsed")

img_url = 'https://img.freepik.com/premium-photo/amazing-atmosphere-soccer-stadium-stadium-is-full-people-excitement-is-palpable_36682-254680.jpg'

st.markdown(
    f"""
    <style>
    .stApp {{
        background:
            linear-gradient(
                rgba(0,0,0,0.8),
                rgba(0,0,0,0.8)
            ),
            url("{img_url}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# CONFIGURAÇÃO DO QUIZ DINÂMICO
DATABASE_URL = "projeto/data_raw/fifa-world-cup/wcmatches.csv"
AI_PROVIDER = None # mock
NUM_PERGUNTAS = 10

# Cache do gerador
@st.cache_resource
def load_quiz_generator():
    try:
        generator = QuizGenerator(
            database_url= st.session_state.database_url,
            ai_provider= st.session_state.ai_provider,
            database_type="csv"
        )
        return generator
    except Exception as e:
        st.error(f"Erro ao carregar o gerador: {e}")
        return None

# DADOS ESTÁTICOS
paises = [
    {'id': 'bra', 'nome': 'Brasil', 'code': 'BR'},
    {'id': 'arg', 'nome': 'Argentina', 'code': 'AR'},
    {'id': 'fra', 'nome': 'França', 'code': 'FR'},
    {'id': 'eng', 'nome': 'Inglaterra', 'code': 'GB'},
    {'id': 'esp', 'nome': 'Espanha', 'code': 'ES'},
    {'id': 'por', 'nome': 'Portugal', 'code': 'PT'},
    {'id': 'ger', 'nome': 'Alemanha', 'code': 'DE'},
    {'id': 'ned', 'nome': 'Holanda', 'code': 'NL'},
    {'id': 'ita', 'nome': 'Itália', 'code': 'IT'},
    {'id': 'usa', 'nome': 'EUA', 'code': 'US'},
    {'id': 'mex', 'nome': 'México', 'code': 'MX'},
    {'id': 'jap', 'nome': 'Japão', 'code': 'JP'},
    {'id': 'aus', 'nome': 'Austrália', 'code': 'AU'},
    {'id': 'mar', 'nome': 'Marrocos', 'code': 'MA'},
    {'id': 'cro', 'nome': 'Croácia', 'code': 'HR'},
    {'id': 'sen', 'nome': 'Senegal', 'code': 'SN'},
]

# perguntas padrão
quiz_padrao = [
    {'q': 'Qual país sediou a Copa do Mundo de 2022?', 'a': 'Qatar', 'opts': ['Russia', 'Qatar', 'Brasil', 'Alemanha']},
    {'q': 'Quem ganhou a Copa do Mundo de 2022?', 'a': 'Argentina', 'opts': ['França', 'Argentina', 'Marrocos', 'Croácia']},
    {'q': 'Quem foi artilheiro da Copa de 2022?', 'a': 'Mbappé', 'opts': ['Messi', 'Neymar', 'Mbappé', 'Lewandowski']},
    {'q': 'Quantos gols Mbappé marcou na final de 2022?', 'a': '3', 'opts': ['1', '2', '3', '4']},
    {'q': 'Qual seleção surpreendeu chegando às semifinais em 2022?', 'a': 'Marrocos', 'opts': ['Austrália', 'Senegal', 'Marrocos', 'Japão']},
    {'q': 'Quem ganhou a Copa do Mundo de 2018?', 'a': 'França', 'opts': ['Croácia', 'França', 'Bélgica', 'Uruguai']},
    {'q': 'Onde foi realizada a Copa do Mundo de 2018?', 'a': 'Rússia', 'opts': ['Alemanha', 'Rússia', 'Qatar', 'EUA']},
    {'q': 'Quantas vezes o Brasil ganhou a Copa do Mundo?', 'a': '5', 'opts': ['4', '5', '6', '3']},
    {'q': 'Em que ano o Brasil foi goleado 7x1 pela Alemanha?', 'a': '2014', 'opts': ['2010', '2012', '2014', '2016']},
    {'q': 'Qual país tem mais títulos mundiais?', 'a': 'Brasil', 'opts': ['Alemanha', 'Brasil', 'Itália', 'Argentina']}
]

# Configurações do tabuleiro
BOARD_SIZE = 40
RANKING_FILE = 'rankings.json'

# Funções
def initialize_board():
    casa = ['normal'] * BOARD_SIZE
    casa[0] = 'Largada'
    casa[BOARD_SIZE - 1] = 'Chegada'
    
    pos_disp = list(range(1, BOARD_SIZE - 1))
    random.shuffle(pos_disp)
    
    tipo_casa = {
        'quiz': 5,
        'bonus': 3,
        'penalty': 3,
        'sortido': 2
    }
    
    index = 0
    for tipo, quant in tipo_casa.items():
        for _ in range(quant):
            casa[pos_disp[index]] = tipo
            index += 1
    
    return casa

def load_rankings():
    try:
        if os.path.exists(RANKING_FILE):
            with open(RANKING_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def save_ranking(vencedor):
    rankings = load_rankings()
    resultado = {
        'vencedor': vencedor['nome'],
        'code': vencedor['pais_code'],
        'score': vencedor['score'],
        'data': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    rankings.insert(0, resultado)
    rankings = rankings[:10]
    with open(RANKING_FILE, 'w') as f:
        json.dump(rankings, f)

def verificar_vitoria(cp, players):
    if not st.session_state.jogo_finalizado:
        if cp['position'] >= BOARD_SIZE - 1:
            st.balloons()
            st.success(f"CAMPEÃO! {cp['nome']} ({cp['pais_code']}) chegou ao FIM!")
            cp['score'] += 50
            save_ranking(cp)
            
            st.subheader("Placar Final:")
            for p in sorted(players, key=lambda x: x['score'], reverse=True):
                st.write(f"- {p['nome']}: {p['score']} pts")
            
            if st.button("Voltar ao Menu", key="btn_fim_jogo_final"):
                st.session_state.game_state = 'menu'
                st.session_state.game_messages = []
                if 'dado_resultado' in st.session_state:
                    del st.session_state.dado_resultado
                st.rerun()
            return True
    return None
                        
    # Função para avança para o próximo turno
def avanca_turno(delay):
    if 'movimento_realizado' not in st.session_state:
        time.sleep(delay)
        st.session_state.current_player_idx = (st.session_state.current_player_idx + 1) % len(st.session_state.players)

        if st.session_state.current_player_idx == 0:
            st.session_state.turn += 1

        st.rerun()

# Inicializar session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'menu'
    st.session_state.players = []
    st.session_state.current_player_idx = 0
    st.session_state.turn = 1
    st.session_state.casa = initialize_board()
    st.session_state.game_messages = []
    st.session_state.quiz = None
    st.session_state.dado_resultado = None


if "jogo_finalizado" not in st.session_state:
    st.session_state.jogo_finalizado = False

# PAINEL DE CONFIGURAÇÃO DO QUIZ
with st.sidebar:
    st.header("Configuração do Quiz")
    
    # Campo para URL do banco de dados
    st.session_state.database_url = st.text_input(
        "URL do DB",
        value=st.session_state.get("database_url", ""),
        help="Caminho local ou URL HTTP de um CSV ou JSON"
    )
    
    # Seletor de provedor de IA
    st.session_state.ai_provider = st.selectbox(
        "Provedor de IA",
        ["mock", "openai", "anthropic"],
        index=0,
        help="mock = simulação (rápida)\nopenai ou anthropic = IA real"
    )
    
    # Botão para testar/recarregar quiz
    if st.button("Recarregar Quiz Dinâmico", use_container_width=True):
        with st.spinner("Gerando perguntas..."):
            generator = load_quiz_generator()
            if generator:
                st.session_state.quiz = generator.generate_questions(NUM_PERGUNTAS)
                st.success(f"{len(st.session_state.quiz)} perguntas geradas!")
            else:
                st.warning("Usando quiz padrão como fallback")
                st.session_state.quiz = quiz_padrao
    
    st.markdown("---")
    
    # Info do banco de dados
    if st.button("Ver Info do Banco", use_container_width=True):
        generator = load_quiz_generator()
        if generator:
            info = generator.get_data_summary()
            with st.expander("Informações"):
                st.json(info)

# PÁGINA PRINCIPAL
st.title("JOGO DE TABULEIRO - FIFA")

if st.session_state.game_state == 'menu':
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Nova Partida", use_container_width=True, key="btn_nova"):
            if st.session_state.quiz is None:
                generator = load_quiz_generator()
                if generator:
                    st.session_state.quiz = generator.generate_questions(NUM_PERGUNTAS)
                else:
                    st.error("Não foi possível inicializar o QuizGenerator.")            
            st.session_state.game_state = 'config'
            st.rerun()
    
    with col2:
        if st.button("Ranking Global", use_container_width=True, key="btn_ranking"):
            st.session_state.game_state = 'ranking'
            st.rerun()
    
    with col3:
        if st.button("Sair", use_container_width=True, key="btn_sair"):
            st.write("Valeu por jogar!")

elif st.session_state.game_state == 'ranking':
    st.header("Ranking Global")
    rankings = load_rankings()
    
    if not rankings:
        st.info("Nenhuma partida registrada ainda.")
    else:
        for i, r in enumerate(rankings):
            st.write(f"**{i+1}º lugar** | {r['code']} - {r['vencedor']} | {r['score']} pts | {r['data']}")
    
    if st.button("Voltar ao Menu", key="btn_back_ranking"):
        st.session_state.game_state = 'menu'
        st.rerun()

elif st.session_state.game_state == 'config':
    st.header("Configuração da Partida")
    
    num_players = st.selectbox("Número de jogadores:", list(range(2,5)))
    
    st.session_state.players = []
    paises_disponiveis = paises.copy()
    
    escolhidos = []
    for i in range(num_players):
        st.subheader(f"Jogador {i+1}")
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input(f"Nome do Jogador {i+1}:", value=f"Jogador {i+1}", key=f"nome_{i}")
        
        with col2:
            paises_options = [p for p in paises_disponiveis if p not in escolhidos]

            escolha_pais_idx = st.selectbox(
                f"País para {nome}:",
                range(len(paises_options)),
                format_func=lambda idx: f"{paises_disponiveis[idx]['nome']} ({paises_disponiveis[idx]['code']})",
                key=f"pais_{i}"
            )

            pais = paises_disponiveis[escolha_pais_idx]['nome']
            pais_code = paises_disponiveis[escolha_pais_idx]['code']

        paises_disponiveis.pop(escolha_pais_idx)
        
        st.session_state.players.append({
            'id': i,
            'nome': nome,
            'pais': pais,
            'pais_code': pais_code,
            'position': 0,
            'score': 0
        })
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Começar Partida", use_container_width=True):
            st.session_state.game_state = 'playing'
            st.session_state.current_player_idx = 0
            st.session_state.turn = 1
            st.session_state.casa = initialize_board()
            st.rerun()
    
    with col2:
        if st.button("Voltar", use_container_width=True):
            st.session_state.game_state = 'menu'
            st.rerun()

elif st.session_state.game_state == 'playing':
    # Carregar quiz se não estiver carregado
    if st.session_state.quiz is None:
        generator = load_quiz_generator()
        if generator:
            st.session_state.quiz = generator.generate_questions(NUM_PERGUNTAS)
        else:
            st.error("Não foi possível inicializar o QuizGenerator.")    
    # Status do jogo    
    st.subheader(f"TURNO {st.session_state.turn}")
    st.subheader("Tabuleiro")

    board_html = """
    <div style="
        display:grid;
        grid-template-columns: repeat(10, 1fr);
        gap:4px;
        border-radius: 4px;
    ">
    """

    for pos in range(BOARD_SIZE):
        players_here = [
            p for p in st.session_state.players
            if p["position"] == pos
        ]

        flags_html = ""

        for p in players_here:
            current = (p["id"] == st.session_state.players[st.session_state.current_player_idx]["id"])

            flag_url = f"https://flagsapi.com/{p['pais_code']}/flat/32.png"

            border = "3px solid green" if current else "1px solid transparent"

            flags_html += f"""
            <img src="{flag_url}" 
                 title="{p['nome']}" 
                 style="
                    margin:1px;
                    border:{border};
                    border-radius:4px;
                    cursor:pointer;
                " 
            />
            """

        tipo_atual = st.session_state.casa[pos]
        color_casas = {
            'quiz': "#3ea0dd",
            'bonus': "#ffd900",
            'penalty': "#b93c1d",
            'sortido': "#b254ff",
            'Largada': "#3AB336",
            'Chegada': "#3AB336",
            'normal': "#ffffff"
        }

        board_html += f"""
        <div style="
            height:80px;
            border:1px solid #999;
            border-radius:8px;
            background:{color_casas[tipo_atual]};
            display: flexbox;
            flex-direction:column;
            justify-content:space-between;
            padding:4px;
        ">
            <div style="
                font-size:11px;
                font-weight:bold;
                color:#000;
                background: #f8f8f8f;
                border-radius: 5px
            ">
                {pos}
                {tipo_atual}
            </div>

            <div style="
                display:flex;
                flex-wrap:wrap;
                justify-content:center;
                align-items:center;
                flex-grow:1;
            ">
                {flags_html}
            </div>
        </div>
        """

    board_html += "</div>"

    components.html(board_html, height=400)  

    # Inicializar histórico de jogadas se não existir
    if 'jogadas_historico' not in st.session_state:
        st.session_state.jogadas_historico = {
            f'jogador{i+1}': [] for i in range(len(st.session_state.players))
        }
        
    # Turno do jogador atual
    col1, col2 = st.columns(2)

    with col1:
        cp = st.session_state.players[st.session_state.current_player_idx]
        st.info(f"Vez de: **{cp['nome']} ({cp['pais_code']})**")

        # Botão para rolar o dado
        if st.button("Rolar o Dado", use_container_width=True, key="btn_dado"):
            dado = random.randint(1, 6)
            st.session_state.dado_resultado = dado

            st.session_state.dado_rolado = True # Guarda a informação que o dado rolou mesmo
            # Registrar jogada
            idx_player = st.session_state.current_player_idx
            st.session_state.jogadas_historico[f"jogador{idx_player+1}"].append(f"Dado: {dado}")
            st.success(f"{cp['nome']} tirou: **{dado}**")

    with col2:
        if 'dado_resultado' is not None:
            if st.session_state.get('dado_rolado', False):
                dado = st.session_state.dado_resultado
                if dado is None:
                    st.error("Erro: dado sem valor. Tente rolar novamente.")
                    st.stop()

                # Mover jogador
                nova_pos = min(cp['position'] + dado, BOARD_SIZE - 1)
                cp['position'] = nova_pos

                tipo_casa = st.session_state.casa[nova_pos]

                st.session_state.movimento_processado = True
                idx_player = st.session_state.current_player_idx
                st.session_state.jogadas_historico[f"jogador{idx_player+1}"].append(f"Casa: {nova_pos}")
                st.write(f"{cp['nome']} foi para a **Casa {nova_pos}**...")

                st.session_state.dado_rolado = False
                st.session_state.dado_resultado = None
                
                # Verificar vitória
                if not verificar_vitoria(cp, st.session_state.players):
                    # Aplicar efeito da casa
                    if tipo_casa == 'quiz':
                        respondeu = casa_quiz(cp, BOARD_SIZE)
                        if respondeu:
                            avanca_turno(3)
                    
                    elif tipo_casa == 'bonus':
                        casa_bonus(cp, BOARD_SIZE)
                        
                        # Verificar vitória após movimento do bonus
                        if not verificar_vitoria(cp, st.session_state.players):
                            avanca_turno(3)
                    
                    elif tipo_casa == 'penalty':
                        casa_penalty(cp)
                        avanca_turno(3)
                    
                    elif tipo_casa == 'sortido':
                        casa_sortida(cp, BOARD_SIZE)
                        # Verificar vitória após movimento da Sorte
                        if not verificar_vitoria(cp, st.session_state.players):
                            avanca_turno(3)
                    # normal
                    else: 
                        avanca_turno(1.5)

    # Exibir histórico de jogadas de forma horizontal
    st.markdown("### Histórico de Jogadas")
    
    colunas = st.columns(len(st.session_state.players))

    for idx, player in enumerate(st.session_state.players):
        with colunas[idx]:
            jogadas_player = st.session_state.jogadas_historico.get(f'jogador{idx+1}', [])
            
            # Criar estilos visuais para cada jogada
            if jogadas_player:
                html_jogadas = """
                    <div style='
                        display:flex;
                        flex-wrap:wrap;
                        gap:4px;
                        margin:0;
                        align-items:center;
                    '>
                    """
                for i, jogada in enumerate(jogadas_player, 1):
                    if 'correto' in jogada.lower():
                        cor = '#4CAF50'
                    elif 'errado' in jogada.lower():
                        cor = '#f44336'
                    elif 'quiz' in jogada.lower():
                        cor = '#2196F3'
                    elif 'bonus(+2)' in jogada.lower():
                        cor = '#FFD700'
                    elif 'falta(-1)' in jogada.lower():
                        cor = '#FF6B6B'
                    elif 'dado' in jogada.lower():
                        cor = "#FFFFFF"
                    else:
                        cor = '#757575'
                    
                    html_jogadas += f"""
                    <div style='
                        background-color:{cor}; 
                        color: black; 
                        padding: 6px 12px; 
                        font-size: 12px; 
                        font-weight: bold;
                        white-space: nowrap;
                        border-radius: 2px;
                    '>
                        {jogada}
                    </div>
                    """
                html_jogadas += "</div>"
                
                st.markdown(f"**{player['nome']} ({player['pais_code']}) - {len(jogadas_player)} jogadas:**")

                components.html(html_jogadas, height=120)
            else:
                st.write(f"**{player['nome']} ({player['pais_code']})** - Aguardando primeira jogada...")