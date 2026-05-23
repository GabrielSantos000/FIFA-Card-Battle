let selectedCard = null;
let energia = 3;

const jogadores = [
  "Lionel Messi",
  "Cristiano Ronaldo",
  "Neymar Jr",
  "Kylian Mbappé",
  "Erling Haaland",
  "Kevin De Bruyne",
  "Luka Modrić",
  "Vinícius Jr",
  "Mohamed Salah",
  "Harry Kane",
  "Antoine Griezmann",
  "Bruno Fernandes",
  "Rodri",
  "Pedri",
  "Jude Bellingham",
  "Joshua Kimmich",
  "Virgil van Dijk",
  "Rúben Dias",
  "Marquinhos",
  "Sergio Ramos",
  "Alisson Becker",
  "Thibaut Courtois",
  "Ederson",
  "Manuel Neuer",
  "Gianluigi Donnarumma"
];

let players = []
const getRandomItem = (min, max) =>
Math.floor(Math.random() * (max - min + 1)) + min

const getRandomPlayer = () => 
  jogadores[getRandomItem(0, jogadores.length - 1)]

for (let i = 0; i < 5; i++){
  let escolhido = getRandomPlayer();
  players.push(escolhido);
  index = jogadores.indexOf(escolhido);
  if(index > -1) {
    jogadores.splice(index, 1);
  }
}
console.log(players)

async function criarCard(jogadores, amount = 5) {

  jogadores.forEach((jogador, amount) => {
    // aqui eu extraio dados dos jogadores do arquivo JSON
      const url = `https://www.thesportsdb.com/api/v1/json/3/searchplayers.php?p=${encodeURIComponent(jogador)}`;
      
      const response = await fetch(url);
      const data = await response.json();
    
      if (!data.player) return "Não encontrado";
    
      const card = [{
      nome_player: data.player[2],
      time_player: data.player[3],
      img_player: data.player[6],
      nacionalidade_player: data.player[7],
      position_player: data.player[11],
      // Tentar conseguir esses dados de outra forma:
      // atk: 90,
      // def: 40,
      // meio: 75,
      // hab: atk*2,
      }]

      const countryCode = paises[`${card.nacionalidade_player}`];
    
      const cardHTML = `
        <div class="card-container">
          <div class="card-inner">
            <div class="card-header">
              <div class="team-flag">
                <img src="https://flagsapi.com/${countryCode}/flat/64.png">
              </div>
              <div class="player-name">
                ${card.nome_player}
              </div>
            </div>
            <div class="player-image-container">
              <img class="player-image" src="${card.img_player}">
            </div>
            <div class="team-name">
              ${card.time_player || "Sem time"}
            </div>
            <div class="attributes-section">
            </div>
          </div>
        </div>
      `;
    
      document.getElementById("card").innerHTML = cardHTML; 
}

            // <div class="attributes-section">
            //   ${createAttribute("Ataque", atk)}
            //   ${createAttribute("Defesa", def)}
            //   ${createAttribute("Meio", meio)}
            //   ${createAttribute("Skill", 95)}
            // </div>

function createAttribute(label, value) {
  return `
    <div class="attribute">
      <div class="attribute-label">${label}</div>
      <div class="attribute-value">${value}</div>
      <div class="attribute-bar">
        <div class="attribute-bar-fill" style="width: ${value}%"></div>
      </div>
    </div>
  `;
}

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

  document.querySelectorAll(".card.small").forEach(c => c.classList.remove("selected"));
  element.classList.add("selected");

  document.getElementById("active-card").innerHTML = `
  <h2>${nome}</h2>
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

  alert(`Você jogou ${selectedCard.nome}!`)
  
    document.getElementsById("turno ativo").classList.remove("ativo");
  document.getElementsById("turno").classList.add("ativo");
}

function useSkill() {
  if (!selectedCard) {
    alert("Selecione uma carta!");
    return;
  }

  alert(`Habilidade ativada: ${selectedCard.skill}`);
}

// function passTurn() {
//   energia = 5;
//   document.getElementById("energia").innerText = energia;
//   alert("Turno passado!");
// }

function resultado() {
  
}