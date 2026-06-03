import streamlit as st
import random
import json
import time
import os
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Copa do Mundo - Jogo de Tabuleiro", layout="wide", initial_sidebar_state="expanded")

paises = [
    {'id': 'bra', 'nome': 'Brasil', 'code': 'BRA'},
    {'id': 'arg', 'nome': 'Argentina', 'code': 'ARG'},
    {'id': 'fra', 'nome': 'França', 'code': 'FRA'},
    {'id': 'eng', 'nome': 'Inglaterra', 'code': 'ENG'},
    {'id': 'esp', 'nome': 'Espanha', 'code': 'ESP'},
    {'id': 'por', 'nome': 'Portugal', 'code': 'POR'},
    {'id': 'ger', 'nome': 'Alemanha', 'code': 'GER'},
    {'id': 'ned', 'nome': 'Holanda', 'code': 'NED'},
    {'id': 'ita', 'nome': 'Itália', 'code': 'ITA'},
    {'id': 'usa', 'nome': 'EUA', 'code': 'USA'},
    {'id': 'mex', 'nome': 'México', 'code': 'MEX'},
    {'id': 'jap', 'nome': 'Japão', 'code': 'JAP'},
    {'id': 'aus', 'nome': 'Austrália', 'code': 'AUS'},
    {'id': 'mar', 'nome': 'Marrocos', 'code': 'MAR'},
    {'id': 'cro', 'nome': 'Croácia', 'code': 'CRO'},
    {'id': 'sen', 'nome': 'Senegal', 'code': 'SEN'},
]

quiz = [
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
RANKING_FILE = 'wcbg_rankings.json'

def initialize_board():
    """Inicializa o tabuleiro com posições aleatórias"""
    casa = ['normal'] * BOARD_SIZE
    casa[0] = 'start'
    casa[BOARD_SIZE - 1] = 'finish'
    
    pos_disp = list(range(1, BOARD_SIZE - 1))
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
    """Carrega os rankings salvos"""
    try:
        if os.path.exists(RANKING_FILE):
            with open(RANKING_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return []

def save_ranking(vencedor):
    """Salva um novo ranking"""
    rankings = load_rankings()
    resultado = {
        'vencedor': vencedor['nome'],
        'code': vencedor['pais']['code'],
        'score': vencedor['score'],
        'data': datetime.now().strftime("%d/%m/%Y %H:%M")
    }
    rankings.insert(0, resultado)
    rankings = rankings[:20]
    with open(RANKING_FILE, 'w') as f:
        json.dump(rankings, f)

# Inicializar session state
if 'game_state' not in st.session_state:
    st.session_state.game_state = 'menu'  # menu, setup, playing, finished
    st.session_state.players = []
    st.session_state.current_player_idx = 0
    st.session_state.turn = 1
    st.session_state.casa = initialize_board()
    st.session_state.game_messages = []

# ===== PÁGINA PRINCIPAL =====
st.title("🏆 COPA DO MUNDO - JOGO DE TABULEIRO 🏆")

if st.session_state.game_state == 'menu':
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Nova Partida", use_container_width=True, key="btn_nova"):
            st.session_state.game_state = 'setup'
            st.rerun()
    
    with col2:
        if st.button("Ranking Global", use_container_width=True, key="btn_ranking"):
            st.session_state.game_state = 'ranking'
            st.rerun()
    
    with col3:
        if st.button("Sair", use_container_width=True, key="btn_sair"):
            st.write("Obrigado por jogar!")

elif st.session_state.game_state == 'ranking':
    st.header(" Ranking Global")
    rankings = load_rankings()
    
    if not rankings:
        st.info("Nenhuma partida registrada ainda.")
    else:
        for i, r in enumerate(rankings):
            st.write(f"**{i+1}º lugar** | {r['code']} - {r['vencedor']} | {r['score']} pts | {r['data']}")
    
    if st.button("← Voltar ao Menu", key="btn_back_ranking"):
        st.session_state.game_state = 'menu'
        st.rerun()

elif st.session_state.game_state == 'setup':
    st.header("Setup da Partida")
    
    num_players = st.slider("Número de jogadores:", min_value=2, max_value=4, value=2)
    
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
            paises_disponiveis.pop(escolha_pais_idx)
        
        st.session_state.players.append({
            'id': i,
            'nome': nome,
            'pais': pais,
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
        if st.button("← Voltar", use_container_width=True):
            st.session_state.game_state = 'menu'
            st.rerun()

elif st.session_state.game_state == 'playing':
    # Status do jogo
    st.header(f"TURNO {st.session_state.turn}")
    
    # Leaderboard
    st.subheader("Posições")
    col_names = st.columns(4)
    col_names[0].write("**Jogador**")
    col_names[1].write("**País**")
    col_names[2].write("**Posição**")
    col_names[3].write("**Pontos**")
    
    for p in st.session_state.players:
        cols = st.columns(4)
        marker = "🎯" if p['id'] == st.session_state.players[st.session_state.current_player_idx]['id'] else "  "
        cols[0].write(f"{marker} {p['nome']}")
        cols[1].write(f"{p['pais']['code']}")
        cols[2].write(f"{p['position'] + 1}/{BOARD_SIZE}")
        cols[3].write(f"**{p['score']}** pts")
    
    st.markdown("---")
    
    # Turno do jogador atual
    cp = st.session_state.players[st.session_state.current_player_idx]
    st.info(f"🎮 Vez de: **{cp['nome']} ({cp['pais']['code']})**")
    
    # Botão para rolar o dado
    if st.button("🎲 Rolar o Dado", use_container_width=True, key="btn_dado"):
        dado = random.randint(1, 6)
        st.session_state.dado_resultado = dado
    
    if 'dado_resultado' in st.session_state:
        dado = st.session_state.dado_resultado
        st.success(f"Você tirou: **{dado}**")
        
        # Mover jogador
        nova_pos = min(cp['position'] + dado, BOARD_SIZE - 1)
        cp['position'] = nova_pos
        tipo_casa = st.session_state.casa[nova_pos]
        
        st.write(f"{cp['nome']} foi para a **Casa {nova_pos + 1}**...")
        
        # Verificar vitória
        if nova_pos == BOARD_SIZE - 1:
            st.balloons()
            st.success(f"CAMPEÃO! {cp['nome']} ({cp['pais']['code']}) chegou ao FIM!")
            cp['score'] += 50
            save_ranking(cp)
            
            st.subheader("Placar Final:")
            for p in sorted(st.session_state.players, key=lambda x: x['score'], reverse=True):
                st.write(f"- {p['nome']}: {p['score']} pts")
            
            if st.button("← Voltar ao Menu", key="btn_fim_jogo"):
                st.session_state.game_state = 'menu'
                st.session_state.game_messages = []
                del st.session_state.dado_resultado
                st.rerun()
        else:
            # Aplicar efeito da casa
            if tipo_casa == 'quiz':
                st.subheader("QUIZ DA COPA DO MUNDO")
                pergunta = random.choice(quiz)
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
                    
                    st.session_state.current_player_idx = (st.session_state.current_player_idx + 1) % len(st.session_state.players)
                    if st.session_state.current_player_idx == 0:
                        st.session_state.turn += 1
                    del st.session_state.dado_resultado
                    time.sleep(1)
                    st.rerun()
            
            elif tipo_casa == 'bonus':
                st.success("GOL! Avança 2 casas e ganha 10 pontos!")
                cp['position'] = min(cp['position'] + 2, BOARD_SIZE - 1)
                cp['score'] += 10
                
                if st.button("Próximo Turno", key="btn_proximo_bonus"):
                    st.session_state.current_player_idx = (st.session_state.current_player_idx + 1) % len(st.session_state.players)
                    if st.session_state.current_player_idx == 0:
                        st.session_state.turn += 1
                    del st.session_state.dado_resultado
                    st.rerun()
            
            elif tipo_casa == 'penalty':
                st.warning("FALTA! Cartão vermelho, volte 2 casas!")
                cp['position'] = max(0, cp['position'] - 2)
                
                if st.button("Próximo Turno", key="btn_proximo_penalty"):
                    st.session_state.current_player_idx = (st.session_state.current_player_idx + 1) % len(st.session_state.players)
                    if st.session_state.current_player_idx == 0:
                        st.session_state.turn += 1
                    del st.session_state.dado_resultado
                    st.rerun()
            
            elif tipo_casa == 'perigo':
                st.info("VAR EM AÇÃO! Escolha quantas casas quer avançar (1 a 6)")
                extra = st.slider("Casas:", min_value=1, max_value=6, value=3, key="slider_var")
                
                if st.button("Avançar", key="btn_avancar"):
                    cp['position'] = min(cp['position'] + extra, BOARD_SIZE - 1)
                    st.write(f"Avançando {extra} casas...")
                    
                    if st.button("Próximo Turno", key="btn_proximo_perigo"):
                        st.session_state.current_player_idx = (st.session_state.current_player_idx + 1) % len(st.session_state.players)
                        if st.session_state.current_player_idx == 0:
                            st.session_state.turn += 1
                        del st.session_state.dado_resultado
                        st.rerun()
            
            else:  # normal
                if st.button("Próximo Turno", key="btn_proximo_normal"):
                    st.session_state.current_player_idx = (st.session_state.current_player_idx + 1) % len(st.session_state.players)
                    if st.session_state.current_player_idx == 0:
                        st.session_state.turn += 1
                    del st.session_state.dado_resultado
                    st.rerun()
