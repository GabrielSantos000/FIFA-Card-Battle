let selectedCard = null;
let energia = 3;

const jogadores = ["Lionel Messi", "Cristiano Ronaldo", "Neymar", "Modric", "Van Dijk"];

const paises = {
  "Brazil": "BR",
  "Argentina": "AR",
  "Germany": "DE",
  "France": "FR",
  "Spain": "ES",
  "Portugal": "PT",
  "England": "GB",
  "Italy": "IT",
  "Netherlands": "NL",
  "Belgium": "BE",
  "Uruguay": "UY",
  "Croatia": "HR",
  "Denmark": "DK",
  "Switzerland": "CH",
  "Poland": "PL",
  "Serbia": "RS",
  "Mexico": "MX",
  "United States": "US",
  "Canada": "CA",
  "Japan": "JP",
  "South Korea": "KR",
  "Australia": "AU",
  "Saudi Arabia": "SA",
  "Iran": "IR",
  "Morocco": "MA",
  "Senegal": "SN",
  "Ghana": "GH",
  "Cameroon": "CM",
  "Tunisia": "TN",
  "Qatar": "QA",
  "Ecuador": "EC",
  "Chile": "CL",
  "Colombia": "CO",
  "Peru": "PE",
  "Paraguay": "PY",
  "Bolivia": "BO",
  "Venezuela": "VE"
};

function atributos(nome) {
    // Extração de dados dos jogadores com a API ou banco de dados
  const url = `.query`

}

async function getPlayerData(nome) {
  // Extração de dados dos jogadores com a API da TheSportDB
  const url = `https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p=${encodeURIComponent(nome)}`;
  
  const response = await fetch(url);
  const data = await response.json();

  if (!data.player) return null;

  const jogador = data.jogadores[0];

  const position = jogador.strPosition;

  return {
    nome: jogador.strPlayer,
    time: jogador.strTeam,
    nacionalidade: jogador.strNationality,
    //atk: ataque()
    //def: defesa()
    //meio: meio()
    //skill: habilidade(jogador.strPosition),
    image: jogador.strCutout
  };
}

function criarCard(nome) {

}

const cardsPlayers = [
  { nome: "Lionel Messi", 
    atk: 88, 
    def: 80, 
    meio: 82, 
    skill: "Ataque +5" },

  { nome: "França", 
    atk: 85, 
    def: 84, 
    meio: 83, 
    skill: "Defesa +5" },

  { nome: "Argentina", 
    atk: 86, 
    def: 78, 
    meio: 85, 
    skill: "Meio +5" },

  { nome: "Espanha", 
    atk: 80, 
    def: 82, 
    meio: 88, 
    skill: "Controle" },

  { nome: "Alemanha", 
    atk: 83, 
    def: 81, 
    meio: 82, 
    skill: "Equilíbrio" }
];

// Troca de telas
function startGame() {
  document.getElementById("inicio").classList.remove("active");
  document.getElementById("game").classList.add("active");
  renderHand();
}

function exitGame() {
  document.getElementById("game").classList.remove("active");
  document.getElementById("inicio").classList.add("active");
}

function dashboard() {
  document.getElementById("inicio").classList.remove("active");
  document.getElementById("dashboard").classList.add("active");
}

// Configuração para renderizar as minhas cartas
function renderHand() {
  const hand = document.getElementById("hand");
  hand.innerHTML = "";

  cardsPlayers.forEach((card, index) => {
    const myCards = document.createElement("myCards");
    myCards.className = "card small";

    myCards.innerHTML = `
      <img src="https://www.thesportsdb.com/api/v1/json/123/searchplayers.php?p=${card.nome}">
      <h4>${card.nome}</h4>`;

    myCards.onclick = () => selectCard(index, myCards);

    hand.appendChild(myCards);
  });
}

function selectCard(index, element) {
  selectedCard = cardsPlayers[index];

  document.querySelectorAll(".card.small").forEach(c => c.classList.remove("selected"));
  element.classList.add("selected");

  document.getElementById("active-card").innerHTML = `
  <h2>${selectedCard.nome}</h2>
  <p>Ataque: ${selectedCard.atk}</p>
  <p>Defesa: ${selectedCard.def}</p>
  <p>Meio: ${selectedCard.meio}</p>
  <p>Habilidade: ${selectedCard.skill}</p>
  `
  ;
}

function playCard() {
  if (!selectedCard) {
    alert("Selecione uma carta!");
    return;
  }

  if (energia <= 0) {
    alert("Sem energia!");
    return;
  }
  // Reduz 1 energia a cada jogada
  energia--;
  document.getElementById("energia").innerText = energia;

  alert(`Você jogou ${selectedCard.nome}!`);
}

function useSkill() {
  if (!selectedCard) {
    alert("Selecione uma carta!");
    return;
  }

  alert(`Habilidade ativada: ${selectedCard.skill}`);
}

function passTurn() {
  energia = 5;
  document.getElementById("energia").innerText = energia;
  alert("Turno passado!");
}

function jogada(gols, posse, disciplina) {
  disciplina = card_amarelo + card_vermelho
  forceCard = gols + posse - disciplina
  carta_adversario = 
  carta_atual = arguments
}

function resultado() {
  
}