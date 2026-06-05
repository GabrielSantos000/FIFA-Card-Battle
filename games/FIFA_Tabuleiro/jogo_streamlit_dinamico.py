import streamlit as st
import streamlit.components.v1 as components
import random
import json
import time
import os
from datetime import datetime
from quiz_generator import QuizGenerator

# Configuração da página
st.set_page_config(page_title="Copa do Mundo - Jogo de Tabuleiro", layout="wide", initial_sidebar_state="expanded")

# CONFIGURAÇÃO DO QUIZ DINÂMICO
DATABASE_URL = "projeto/data_raw/fifa-world-cup/wcmatches.csv"
AI_PROVIDER = "mock"
NUM_PERGUNTAS = 10

# Cache do gerador
@st.cache_resource
def load_quiz_generator():
    try:
        generator = QuizGenerator(
            database_url=DATABASE_URL,
            ai_provider=AI_PROVIDER,
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

def initialize_board():
    casa = ['normal'] * BOARD_SIZE
    casa[0] = 'start'
    casa[BOARD_SIZE - 1] = 'finish'
    
    pos_disp = list(range(1, BOARD_SIZE))
    random.shuffle(pos_disp)
    
    tipo_casa = {
        'quiz': 5,
        'bonus': 3,
        'penalty': 3,
        'perigo': 2
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

# Inicializar session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'menu'
    st.session_state.players = []
    st.session_state.current_player_idx = 0
    st.session_state.turn = 1
    st.session_state.casa = initialize_board()
    st.session_state.game_messages = []
    st.session_state.quiz = None

# PAINEL DE CONFIGURAÇÃO DO QUIZ
with st.sidebar:
    st.header("Configuração do Quiz")
    
    # Campo para URL do banco de dados
    custom_db_url = st.text_input(
        "URL do DB",
        value=DATABASE_URL,
        help="Caminho local ou URL HTTP de um CSV ou JSON"
    )
    
    # Seletor de provedor de IA
    ai_choice = st.selectbox(
        "Provedor de IA",
        ["mock", "openai", "anthropic"],
        index=0,
        help="mock = simulação (rápida)\nopenai ou anthropic = IA real"
    )
    
    # Número de perguntas
    num_q = st.slider(
        "Número de Perguntas",
        min_value=1,
        max_value=10,
        value=NUM_PERGUNTAS
    )
    
    # Contexto (opcional)
    # quiz_context = st.text_area(
    #     "Contexto do Quiz (opcional)",
    #     value="",
    #     help="Ex: 'sobre Copa 2022' ou 'sobre artilheiros'"
    # )
    
    # Botão para testar/recarregar quiz
    if st.button("Recarregar Quiz Dinâmico", use_container_width=True):
        with st.spinner("Gerando perguntas..."):
            generator = load_quiz_generator()
            if generator:
                st.session_state.quiz = generator.generate_questions(
                    num_questions=num_q
                    # context=quiz_context if quiz_context else "sobre Copa do Mundo"
                )
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
                    st.session_state.quiz = generator.generate_questions(
                        num_questions=NUM_PERGUNTAS
                    )
                else:
                    st.session_state.quiz = quiz_padrao
            
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
    
    for i in range(num_players):
        st.subheader(f"Jogador {i+1}")
        col1, col2 = st.columns(2)
        
        with col1:
            nome = st.text_input(f"Nome do Jogador {i+1}:", value=f"Jogador {i+1}", key=f"nome_{i}")
        
        with col2:
            paises_nomes = [p['nome'] for p in paises_disponiveis]
            escolha_pais_idx = st.selectbox(
                f"País para {nome}:",
                range(len(paises_disponiveis)),
                format_func=lambda idx: f"{paises_disponiveis[idx]['nome']} ({paises_disponiveis[idx]['code']})",
                key=f"pais_{i}"
            )
            pais = paises_disponiveis[escolha_pais_idx]
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
            st.session_state.quiz = quiz_padrao
    
    # Status do jogo
    st.header(f"TURNO {st.session_state.turn}")
    
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
                    margin:2px;
                    border:{border};
                    border-radius:4px;
                    cursor:pointer;
                " 
            />
            """

        tipo_atual = st.session_state.casa[pos]
        color_casas = {
            'quiz': '#add9f4',
            'bonus': "#005f9e",
            'penalty': '#f7603b',
            'perigo': '#a30015',
            'start': '#00c853',
            'finish': '#ffd700',
            'normal': '#f8f8f8'
        }
        board_html += f"""
        <div style="
            height:80px;
            border:1px solid #999;
            border-radius:8px;
            background:{color_casas[tipo_atual]};
            display:flex;
            flex-direction:column;
            justify-content:space-between;
            padding:4px;
        ">
            <div style="
                font-size:11px;
                font-weight:bold;
                color:#fff;
            ">
                {pos + 1}
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

    st.markdown("---")
    
    # Turno do jogador atual
    cp = st.session_state.players[st.session_state.current_player_idx]
    st.info(f"Vez de: **{cp['nome']} ({cp['pais_code']})**")
    
    # Botão para rolar o dado
    if st.button("Rolar o Dado", use_container_width=True, key="btn_dado"):
        dado = random.randint(1, 6)
        st.session_state.dado_resultado = dado
        st.success(f"Você tirou: **{dado}**")
    
    if 'dado_resultado' in st.session_state:
        dado = st.session_state.dado_resultado
        time.sleep(3)
        # Mover jogador
        nova_pos = min(cp['position'] + dado, BOARD_SIZE - 1)
        cp['position'] = nova_pos
        tipo_casa = st.session_state.casa[nova_pos]
        
        st.write(f"{cp['nome']} foi para a **Casa {nova_pos}**...")
        
        # Verificar vitória
        if nova_pos == BOARD_SIZE:
            st.balloons()
            st.success(f"CAMPEÃO! {cp['nome']} ({cp['pais_code']}) chegou ao FIM!")
            cp['score'] += 50
            save_ranking(cp)
            
            st.subheader("Placar Final:")
            for p in sorted(st.session_state.players, key=lambda x: x['score'], reverse=True):
                st.write(f"- {p['nome']}: {p['score']} pts")
            
            if st.button("Voltar ao Menu", key="btn_fim_jogo"):
                st.session_state.game_state = 'menu'
                st.session_state.game_messages = []
                del st.session_state.dado_resultado
                st.rerun()
        else:
            # Aplicar efeito da casa
            if tipo_casa == 'quiz':
                st.subheader("QUIZ DA COPA DO MUNDO")
                pergunta = random.choice(st.session_state.quiz)
                st.write(f"**Pergunta:** {pergunta['q']}")
    
                opts = pergunta['opts'].copy()
                random.shuffle(opts)
                
                resposta = st.radio("Escolha sua resposta:", opts, key=f"quiz_{st.session_state.turn}_{cp['id']}")
                
                if st.button("Confirmar Resposta", key="btn_resposta"):
                    if resposta == pergunta['a']:
                        st.success("Correto! +20 pontos e avança 2 casas.")
                        cp['score'] += 20
                        cp['position'] = min(cp['position'] + 2, BOARD_SIZE - 1)
                        
                    else:
                        st.error(f"Errado! A resposta certa era: **{pergunta['a']}**. Volta 1 casa.")
                        cp['position'] = max(0, cp['position'] - 1)
                    # Avança para o próximo turno
                    st.session_state.current_player_idx = (st.session_state.current_player_idx + 1) % len(st.session_state.players)
                    if st.session_state.current_player_idx == 0:
                        st.session_state.turn += 1
                    del st.session_state.dado_resultado
                    time.sleep(3)
                    st.rerun()
            
            elif tipo_casa == 'bonus':
                st.success("GOL! Avança 2 casas e ganha 10 pontos!")

                cp['position'] = min(cp['position'] + 2, BOARD_SIZE - 1)
                cp['score'] += 10
                time.sleep(3)
                
                # Avança para o próximo turno
                st.session_state.current_player_idx = (st.session_state.current_player_idx + 1) % len(st.session_state.players)
                if st.session_state.current_player_idx == 0:
                    st.session_state.turn += 1
                del st.session_state.dado_resultado
                st.rerun()
            
            elif tipo_casa == 'penalty':
                st.warning("FALTA! Cartão vermelho, volte 2 casas!")

                cp['position'] = max(0, cp['position'] - 2)
                time.sleep(3)

                # Avança para o próximo turno
                st.session_state.current_player_idx = (st.session_state.current_player_idx + 1) % len(st.session_state.players)
                if st.session_state.current_player_idx == 0:
                    st.session_state.turn += 1
                del st.session_state.dado_resultado
                st.rerun()
            
            elif tipo_casa == 'perigo':
                st.info("Eita! Vai ter que contar com a sorte")
                lista = [x for x in range(-6,7) if x != 0]
                extra = random.randint(lista)
                cp['position'] = min(cp['position'] + extra, BOARD_SIZE - 1)
                if extra < 0:
                    st.write(f"Voltando {extra} casas...")
                else:
                    st.write(f"Avamçando {extra} casas...")
                    
                # Avança para o próximo turno
                st.session_state.current_player_idx = (st.session_state.current_player_idx + 1) % len(st.session_state.players)
                if st.session_state.current_player_idx == 0:
                    st.session_state.turn += 1
                del st.session_state.dado_resultado
                st.rerun()
            
            else:  # normal
                st.session_state.current_player_idx = (st.session_state.current_player_idx + 1) % len(st.session_state.players)
                if st.session_state.current_player_idx == 0:
                    st.session_state.turn += 1
                del st.session_state.dado_resultado
                st.rerun()
