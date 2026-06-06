import streamlit as st
import time
import random
from jogo_streamlit_dinamico import verificar_vitoria

def casa_bonus(cp, BOARD_SIZE):
    st.success("GOL! Avança 2 casas e ganha 10 pontos!")
    idx_player = st.session_state.current_player_idx
    st.session_state.jogadas_historico[f'jogador{idx_player+1}'].append("BONUS(+2)")
    cp['position'] = min(cp['position'] + 2, BOARD_SIZE - 1)
    cp['score'] += 10
    time.sleep(2)

def casa_sortida(cp, BOARD_SIZE):
    st.info("Eita! Vai ter que contar com a sorte")
    extra = random.randint(-6, 6)
    idx_player = st.session_state.current_player_idx
    st.session_state.jogadas_historico[f'jogador{idx_player+1}'].append(f"Sorte ({extra:+d})")
    cp['position'] = min(cp['position'] + extra, BOARD_SIZE - 1)
    if extra < 0:
        st.write(f"Voltando {extra} casas...")
    else:
        st.write(f"Avançando {extra} casas...")
    time.sleep(2.5)

def casa_penalty(cp):
    st.warning("FALTA! Levou cartada, volte 1 casa!")
    idx_player = st.session_state.current_player_idx
    st.session_state.jogadas_historico[f'jogador{idx_player+1}'].append("FALTA(-1)")
    cp['position'] = max(cp['position'] - 1, 0)
    time.sleep(2)

def casa_quiz(cp, BOARD_SIZE):
    quiz_key = f"pergunta_{st.session_state.turn}_{cp['id']}_{cp['position']}"
    if not st.session_state.get(f'quiz_respondido_{quiz_key}'):
        st.subheader("QUIZ DA COPA DO MUNDO")

        # Evitar repetir questão
        if f'pergunta_{quiz_key}' not in st.session_state:
            st.session_state[f'pergunta_{quiz_key}'] = random.choice(st.session_state.quiz)
    
        pergunta = st.session_state[f'pergunta_{quiz_key}']
        st.write(f"**Pergunta:** {pergunta['q']}")

        opts = pergunta['opts'].copy()
        random.shuffle(opts)

        resposta = st.radio("Escolha sua resposta:", opts, key=quiz_key)

        if st.button("Confirmar Resposta", key=f"btn_resposta_{quiz_key}"):
            idx_player = st.session_state.current_player_idx

            if resposta == pergunta['a']:
                st.success("Correto! +20 pontos e avança 2 casas.")
                cp['score'] += 20
                cp['position'] = min(cp['position'] + 2, BOARD_SIZE - 1)
                st.session_state.jogadas_historico[f'jogador{idx_player+1}'].append("correto")
            else:
                st.error(f"Errado! A resposta certa era: **{pergunta['a']}**. Volta 1 casa.")
                cp['position'] = max(0, cp['position'] - 1)
                st.session_state.jogadas_historico[f'jogador{idx_player+1}'].append("errado")

            # Marca como respondido e avança o turno
            st.session_state[f'quiz_respondido_{quiz_key}'] = True

        # Verificar vitória após movimento do quiz
    if st.session_state.get(f'quiz_respondido_{quiz_key}'):
        verificar_vitoria(cp, st.session_state.players)

