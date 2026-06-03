import random
import json
import time
import os

paises = [
    {'id': 'bra', 'name': 'Brasil', 'code': 'BRA'},
    {'id': 'arg', 'name': 'Argentina', 'code': 'ARG'},
    {'id': 'fra', 'name': 'França', 'code': 'FRA'},
    {'id': 'eng', 'name': 'Inglaterra', 'code': 'ENG'},
    {'id': 'esp', 'name': 'Espanha', 'code': 'ESP'},
    {'id': 'por', 'name': 'Portugal', 'code': 'POR'},
    {'id': 'ger', 'name': 'Alemanha', 'code': 'GER'},
    {'id': 'ned', 'name': 'Holanda', 'code': 'NED'},
    {'id': 'ita', 'name': 'Itália', 'code': 'ITA'},
    {'id': 'usa', 'name': 'EUA', 'code': 'USA'},
    {'id': 'mex', 'name': 'México', 'code': 'MEX'},
    {'id': 'jap', 'name': 'Japão', 'code': 'JAP'},
    {'id': 'aus', 'name': 'Austrália', 'code': 'AUS'},
    {'id': 'mar', 'name': 'Marrocos', 'code': 'MAR'},
    {'id': 'cro', 'name': 'Croácia', 'code': 'CRO'},
    {'id': 'sen', 'name': 'Senegal', 'code': 'SEN'},
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

# --- CONFIGURAÇÕES DO TABULEIRO ---
BOARD_SIZE = 40
casa = ['normal'] * BOARD_SIZE
casa[0] = 'start'
casa[BOARD_SIZE - 1] = 'finish'

pos_disp = list(range(1,BOARD_SIZE-1))
random.shuffle(pos_disp) #Embaralha a lista de posições

tipo_casa = {
    'quiz': 5,
    'bonus': 3,
    'penalti': 3,
    'perigo': 2
}

index = 0
for tipo, quant in tipo_casa.items():
    for _ in range(quant):
        casa[pos_disp[index]] = tipo
        index +=1

ranking = 'rankings.json'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class JogoCopa:
    def __init__(self):
        self.players = []
        self.current_player_idx = 0
        self.turn = 1
        self.rankings = self.load_rankings()

    def load_rankings(self):
        try:
            if os.path.exists(ranking):
                with open(ranking, 'r') as f:
                    return json.load(f)
        except:
            pass
        return []

    def save_ranking(self, vencedor):
        resultado = {
            'vencedor': vencedor['name'],
            'code': vencedor['pais']['code'],
            'score': vencedor['score'],
            'data': time.strftime("%d/%m/%Y")
        }
        self.rankings.insert(0, resultado)
        self.rankings = self.rankings[:20]  # Manter top 20
        with open(ranking, 'w') as f:
            json.dump(self.rankings, f)

    def menu_principal(self):
        while True:
            clear_screen()
            print("="*40)
            print("   COPA DO MUNDO - JOGO DE TABULEIRO   ")
            print("="*40)
            print("1. Nova Partida")
            print("2. Ranking Global")
            print("3. Sair")
            
            escolha = input("\nEscolha uma opção: ")
            if escolha == '1':
                self.setup_game()
                self.game_loop()
            elif escolha == '2':
                self.show_rankings()
            elif escolha == '3':
                print("Saindo do jogo...")
                break

    def show_rankings(self):
        clear_screen()
        print("="*40)
        print("           RANKING GLOBAL           ")
        print("="*40)
        if not self.rankings:
            print("Nenhuma partida registrada ainda.")
        else:
            for i, r in enumerate(self.rankings):
                print(f"{i+1}º | {r['code']} - {r['vencedor']} | {r['score']} pts | {r['data']}")
        input("\nPressione ENTER para voltar...")

    def setup_game(self):
        clear_screen()
        print("--- SETUP DA PARTIDA ---")
        
        while True:
            try:
                num_players = int(input("Número de jogadores (2 a 4): "))
                if 2 <= num_players <= 4:
                    break
                print("Por favor, digite um número entre 2 e 4.")
            except ValueError:
                print("Entrada inválida.")

        self.players = []
        paises_disponiveis = paises.copy()

        for i in range(num_players):
            print(f"\n--- Jogador {i+1} ---")
            name = input(f"name do Jogador {i+1}: ").strip()
            if not name: name = f"Jogador {i+1}"
            
            print("\nPaíses disponíveis:")
            for j, p in enumerate(paises_disponiveis):
                print(f"[{j}] {p['name']} ({p['code']})")
            
            while True:
                try:
                    escolha_pais = int(input(f"Escolha o número do país para {name}: "))
                    if 0 <= escolha_pais < len(paises_disponiveis):
                        pais = paises_disponiveis.pop(escolha_pais)
                        break
                    print("Escolha inválida.")
                except ValueError:
                    print("Digite um número válido.")

            self.players.append({
                'id': i,
                'name': name,
                'pais': pais,
                'position': 0,
                'score': 0
            })
        
        self.current_player_idx = 0
        self.turn = 1

    def print_status(self):
        print("\n" + "="*40)
        print(f"TURNO {self.turn}")
        print("="*40)
        for p in self.players:
            # Sort players by score to show leaderboard dynamically
            marc = "=>" if p['id'] == self.players[self.current_player_idx]['id'] else "  "
            print(f"{marc} {p['name']} ({p['pais']['code']}) | Casa: {p['position'] + 1}/40 | Pts: {p['score']}")
        print("="*40)

    def trigger_quiz(self, player):
        print("\n[❓ QUIZ DA COPA DO MUNDO]")
        pergunta = random.choice(quiz)
        print(f"Pergunta: {pergunta['q']}")
        
        opts = pergunta['opts'].copy()
        random.shuffle(opts)
        
        for i, opt in enumerate(opts):
            print(f"{i+1}. {opt}")
            
        while True:
            try:
                resp_idx = int(input("\nSua resposta (1-4): ")) - 1
                if 0 <= resp_idx <= 3:
                    if opts[resp_idx] == pergunta['a']:
                        print("✅ Correto! +20 pontos e avança 2 casas.")
                        player['score'] += 20
                        player['position'] = min(player['position'] + 2, BOARD_SIZE - 1)
                    else:
                        print(f"❌ Errado! A resposta certa era: {pergunta['a']}. Volta 1 casa.")
                        player['position'] = max(0, player['position'] - 1)
                    break
                print("Escolha entre 1 e 4.")
            except ValueError:
                print("Entrada inválida.")
        time.sleep(2)

    def game_loop(self):
        while True:
            clear_screen()
            self.print_status()
            
            cp = self.players[self.current_player_idx]
            print(f"\nVez de: {cp['name']} ({cp['pais']['code']})")
            input("Pressione ENTER para rolar o dado...")
            
            dado = random.randint(1, 6)
            print(f"🎲 Você tirou: {dado}")
            time.sleep(1)
            
            nova_pos = min(cp['position'] + dado, BOARD_SIZE - 1)
            cp['position'] = nova_pos
            tipo_casa = casa[nova_pos]
            
            print(f"{cp['name']} foi para a Casa {nova_pos + 1}...")
            time.sleep(1)
            
            # Condição de Vitória
            if nova_pos == BOARD_SIZE - 1:
                clear_screen()
                print("🏆"*10)
                print(f" TEMOS UM CAMPEÃO! {cp['name']} ({cp['pais']['code']}) chegou ao FIM!")
                print("🏆"*10)
                cp['score'] += 50 # Bônus de chegada
                self.save_ranking(cp)
                
                print("\nPlacar Final:")
                for p in sorted(self.players, key=lambda x: x['score'], reverse=True):
                    print(f"- {p['name']}: {p['score']} pts")
                
                input("\nPressione ENTER para voltar ao menu...")
                break

            # Ações das Casas
            if tipo_casa == 'quiz':
                self.trigger_quiz(cp)
            elif tipo_casa == 'bonus':
                print("⚽ GOL! Avança 2 casas e ganha 10 pontos!")
                cp['position'] = min(cp['position'] + 2, BOARD_SIZE - 1)
                cp['score'] += 10
                time.sleep(2)
            elif tipo_casa == 'penalty':
                print("🟥 FALTA! Cartão vermelho, volte 2 casas!")
                cp['position'] = max(0, cp['position'] - 2)
                time.sleep(2)
            elif tipo_casa == 'wild':
                print("📺 VAR EM AÇÃO!")
                while True:
                    try:
                        extra = int(input("Escolha quantas casas quer avançar (1 a 6): "))
                        if 1 <= extra <= 6:
                            cp['position'] = min(cp['position'] + extra, BOARD_SIZE - 1)
                            print(f"Avançando {extra} casas...")
                            break
                        print("Escolha um número de 1 a 6.")
                    except ValueError:
                        print("Entrada inválida.")
                time.sleep(1)

            # Passa o turno
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            if self.current_player_idx == 0:
                self.turn += 1

if __name__ == "__main__":
    jogo = JogoCopa()
    jogo.menu_principal()