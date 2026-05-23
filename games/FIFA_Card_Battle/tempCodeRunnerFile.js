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
Math.floor(Math.random() * (max - min + 1))

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