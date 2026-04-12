let selectedCard = null;
let energy = 3;

const cards = [
  { name: "Brasil", atk: 88, def: 80, mid: 82, skill: "Ataque +5" },
  { name: "França", atk: 85, def: 84, mid: 83, skill: "Defesa +5" },
  { name: "Argentina", atk: 86, def: 78, mid: 85, skill: "Meio +5" },
  { name: "Espanha", atk: 80, def: 82, mid: 88, skill: "Controle" },
  { name: "Alemanha", atk: 83, def: 81, mid: 82, skill: "Equilíbrio" }
];

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

function renderHand() {
  const hand = document.getElementById("hand");
  hand.innerHTML = "";

  cards.forEach((card, index) => {
    const div = document.createElement("div");
    div.className = "card small";

    div.innerHTML = `
      <h4>${card.name}</h4>
      <p>Ataque: ${card.atk}</p>
    `;

    div.onclick = () => selectCard(index, div);

    hand.appendChild(div);
  });
}

function selectCard(index, element) {
  selectedCard = cards[index];

  document.querySelectorAll(".card.small").forEach(c => c.classList.remove("selected"));
  element.classList.add("selected");

  document.getElementById("active-card").innerHTML = `
    <h2>${selectedCard.name}</h2>
    <p>Ataque: ${selectedCard.atk}</p>
    <p>Defesa: ${selectedCard.def}</p>
    <p>Meio: ${selectedCard.mid}</p>
    <p>Habilidade: ${selectedCard.skill}</p>
  `;
}

function playCard() {
  if (!selectedCard) {
    alert("Selecione uma carta!");
    return;
  }

  if (energy <= 0) {
    alert("Sem energia!");
    return;
  }
  // Reduz 1 energia a cada jogada
  energy--;
  document.getElementById("energy").innerText = energy;

  alert(`Você jogou ${selectedCard.name}!`);
}

function useSkill() {
  if (!selectedCard) {
    alert("Selecione uma carta!");
    return;
  }

  alert(`Habilidade ativada: ${selectedCard.skill}`);
}

function passTurn() {
  energy = 3;
  document.getElementById("energy").innerText = energy;
  alert("Turno passado!");
}

function jogada(q_gols, posse, disciplina) {
  disciplina = card_amarelo + card_vermelho
  forceCard = q_gols + posse - disciplina
  carta_adversario = 
  carta_atual = 
}