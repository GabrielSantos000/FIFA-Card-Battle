const {useState,useEffect,useCallback,useRef} = React;

const COUNTRIES = [
  {id:'bra',name:'Brasil',flag:'🇧🇷',color:'#009c3b'},
  {id:'arg',name:'Argentina',flag:'🇦🇷',color:'#74ACDF'},
  {id:'fra',name:'França',flag:'🇫🇷',color:'#002395'},
  {id:'eng',name:'Inglaterra',flag:'🏴󠁧󠁢󠁥󠁮󠁧󠁿',color:'#CF091D'},
  {id:'esp',name:'Espanha',flag:'🇪🇸',color:'#c60b1e'},
  {id:'por',name:'Portugal',flag:'🇵🇹',color:'#006600'},
  {id:'ger',name:'Alemanha',flag:'🇩🇪',color:'#333'},
  {id:'ned',name:'Holanda',flag:'🇳🇱',color:'#FF6600'},
  {id:'ita',name:'Itália',flag:'🇮🇹',color:'#003087'},
  {id:'usa',name:'EUA',flag:'🇺🇸',color:'#BF0A30'},
  {id:'mex',name:'México',flag:'🇲🇽',color:'#006847'},
  {id:'jap',name:'Japão',flag:'🇯🇵',color:'#BC002D'},
  {id:'aus',name:'Austrália',flag:'🇦🇺',color:'#00008B'},
  {id:'mar',name:'Marrocos',flag:'🇲🇦',color:'#C1272D'},
  {id:'cro',name:'Croácia',flag:'🇭🇷',color:'#FF0000'},
  {id:'sen',name:'Senegal',flag:'🇸🇳',color:'#00853F'},
];

const QUIZ_DB = [
  {q:'Qual país sediou a Copa do Mundo de 2022?',a:'Qatar',opts:['Russia','Qatar','Brasil','Alemanha'],year:2022,category:'sede'},
  {q:'Quem ganhou a Copa do Mundo de 2022?',a:'Argentina',opts:['França','Argentina','Marrocos','Croácia'],year:2022,category:'campeão'},
  {q:'Quem foi artilheiro da Copa de 2022?',a:'Mbappé',opts:['Messi','Neymar','Mbappé','Lewandowski'],year:2022,category:'artilheiro'},
  {q:'Quantos gols Mbappé marcou na final de 2022?',a:'3',opts:['1','2','3','4'],year:2022,category:'estatística'},
  {q:'Qual seleção surpreendeu chegando às semifinais em 2022?',a:'Marrocos',opts:['Austrália','Senegal','Marrocos','Japão'],year:2022,category:'surpresa'},
  {q:'Quem ganhou a Copa do Mundo de 2018?',a:'França',opts:['Croácia','França','Bélgica','Uruguai'],year:2018,category:'campeão'},
  {q:'Onde foi realizada a Copa do Mundo de 2018?',a:'Rússia',opts:['Alemanha','Rússia','Qatar','EUA'],year:2018,category:'sede'},
  {q:'Quantas vezes o Brasil ganhou a Copa do Mundo?',a:'5',opts:['4','5','6','3'],year:0,category:'história'},
  {q:'Em que ano o Brasil foi goleado 7x1 pela Alemanha?',a:'2014',opts:['2010','2012','2014','2016'],year:2014,category:'marcante'},
  {q:'Qual país tem mais títulos mundiais?',a:'Brasil',opts:['Alemanha','Brasil','Itália','Argentina'],year:0,category:'história'},
  {q:'Em que ano Pelé venceu sua primeira Copa do Mundo?',a:'1958',opts:['1954','1958','1962','1966'],year:1958,category:'lenda'},
  {q:'Qual jogador marcou gol de bicicleta na Copa de 2018?',a:'Cristiano Ronaldo',opts:['Neymar','Messi','Cristiano Ronaldo','Mbappé'],year:2018,category:'golaço'},
  {q:'Onde foi a Copa de 2014?',a:'Brasil',opts:['Brasil','África do Sul','Argentina','Alemanha'],year:2014,category:'sede'},
  {q:'Quantas seleções participam da Copa desde 2026?',a:'48',opts:['32','40','48','64'],year:2026,category:'formato'},
  {q:'Qual seleção defendeu título em 2022?',a:'França',opts:['Argentina','Alemanha','França','Brasil'],year:2022,category:'defensor'},
  {q:'Em que país será a Copa de 2026?',a:'EUA/Canadá/México',opts:['Austrália','EUA/Canadá/México','Arábia Saudita','Japão'],year:2026,category:'sede'},
  {q:'Quem marcou 4 gols em um único jogo na Copa de 1994?',a:'Oleg Salenko',opts:['Romário','Bebeto','Oleg Salenko','Hristo Stoichkov'],year:1994,category:'recorde'},
  {q:'Qual goleiro foi eleito melhor da Copa de 2022?',a:'Emiliano Martínez',opts:['Lloris','Bounou','Emiliano Martínez','Alisson'],year:2022,category:'goleiro'},
  {q:'Quem marcou o gol do título da Argentina em 2022 nos pênaltis?',a:'Gonzalo Montiel',opts:['Messi','Di María','Gonzalo Montiel','Otamendi'],year:2022,category:'final'},
  {q:'Qual foi o placar da final de 2022 após a prorrogação?',a:'3x3',opts:['2x2','3x3','4x2','2x1'],year:2022,category:'placar'},
];

const BOARD_SIZE = 40;
const CELL_TYPES = (() => {
  const types = Array(BOARD_SIZE).fill('normal');
  types[0]='start'; types[BOARD_SIZE-1]='finish';
  [5,12,19,26,33].forEach(i=>types[i]='quiz');
  [8,22,36].forEach(i=>types[i]='bonus');
  [14,28,31].forEach(i=>types[i]='penalty');
  [18,25].forEach(i=>types[i]='wild');
  return types;
})();

const CELL_INFO = {
  quiz:{label:'QUIZ',icon:'❓'},
  bonus:{label:'GOL!',icon:'⚽'},
  penalty:{label:'FALTA',icon:'🟥'},
  wild:{label:'VAR',icon:'📺'},
  start:{label:'INÍCIO',icon:'🏟️'},
  finish:{label:'TAÇA',icon:'🏆'},
  normal:{label:'',icon:''},
};

const DICE_FACES = ['⚀','⚁','⚂','⚃','⚄','⚅'];
const PLAYER_COLORS = ['#FFD700','#00D4FF','#FF6B6B','#A78BFA'];
const STORAGE_KEY = 'wcbg_rankings_v2';

function App(){
  const [screen,setScreen]=useState('home');
  const [numPlayers,setNumPlayers]=useState(2);
  const [players,setPlayers]=useState([]);
  const [setupStep,setSetupStep]=useState(0);
  const [selectedCountries,setSelectedCountries]=useState([]);
  const [playerNames,setPlayerNames]=useState(['Jogador 1','Jogador 2','Jogador 3','Jogador 4']);
  const [gameState,setGameState]=useState(null);
  const [rankings,setRankings]=useState(()=>{
    try{return JSON.parse(localStorage.getItem(STORAGE_KEY)||'[]');}catch{return [];}
  });
  const [toast,setToast]=useState(null);
  const [modal,setModal]=useState(null);
  const [diceRolling,setDiceRolling]=useState(false);
  const [lastDice,setLastDice]=useState(null);
  const [quizState,setQuizState]=useState(null);
  const [loadingAI,setLoadingAI]=useState(false);

  const showToast=(msg,dur=2500)=>{
    setToast(msg);
    setTimeout(()=>setToast(null),dur);
  };

  const saveRanking=(result)=>{
    const newRankings=[{...result,date:new Date().toLocaleDateString('pt-BR')},...rankings].slice(0,20);
    setRankings(newRankings);
    try{localStorage.setItem(STORAGE_KEY,JSON.stringify(newRankings));}catch{}
  };

  const startSetup=()=>{setSetupStep(0);setSelectedCountries([]);setScreen('setup');};

  const selectCountry=(country,playerIdx)=>{
    if(isCountryTaken(country.id,playerIdx)) return;
    setSelectedCountries(prev=>[...prev.filter(s=>s.playerIdx!==playerIdx),{country,playerIdx}]);
  };

  const isCountryTaken=(countryId,currentPlayerIdx)=>
    selectedCountries.some(s=>s.country.id===countryId&&s.playerIdx!==currentPlayerIdx);

  const getSelectedForPlayer=(playerIdx)=>
    selectedCountries.find(s=>s.playerIdx===playerIdx)?.country||null;

  const startGame=()=>{
    const finalPlayers=Array.from({length:numPlayers},(_,i)=>({
      id:i,name:playerNames[i]||`Jogador ${i+1}`,
      country:getSelectedForPlayer(i)||COUNTRIES[i],
      position:0,score:0,quizCorrect:0,quizTotal:0,color:PLAYER_COLORS[i],
    }));
    setPlayers(finalPlayers);
    setGameState({currentPlayer:0,turn:1,phase:'roll',quizUsed:[]});
    setLastDice(null);
    setQuizState(null);
    setModal(null);
    setScreen('game');
  };

  const rollDice=()=>{
    if(diceRolling) return;
    setDiceRolling(true);
    let count=0;
    const interval=setInterval(()=>{
      setLastDice(Math.floor(Math.random()*6));
      count++;
      if(count>=8){
        clearInterval(interval);
        const final=Math.floor(Math.random()*6);
        setLastDice(final);
        setDiceRolling(false);
        movePlayer(final+1);
      }
    },60);
  };

  const movePlayer=(steps)=>{
    const cp=gameState.currentPlayer;
    setPlayers(prev=>{
      const updated=prev.map((p,i)=>{
        if(i!==cp) return p;
        const newPos=Math.min(p.position+steps,BOARD_SIZE-1);
        return {...p,position:newPos};
      });
      const newPos=updated[cp].position;
      const cellType=CELL_TYPES[newPos];
      if(newPos===BOARD_SIZE-1){setTimeout(()=>endGame(cp,updated),500);}
      else if(cellType==='quiz'){setTimeout(()=>triggerQuiz(),400);}
      else if(cellType==='bonus'){
        showToast('⚽ GOL! Avança 2 casas!');
        setTimeout(()=>{
          setPlayers(p2=>p2.map((p,i)=>i===cp?{...p,position:Math.min(p.position+2,BOARD_SIZE-1),score:p.score+10}:p));
          nextTurn();
        },1200);
      } else if(cellType==='penalty'){
        showToast('🟥 Falta! Volta 2 casas!');
        setTimeout(()=>{
          setPlayers(p2=>p2.map((p,i)=>i===cp?{...p,position:Math.max(0,p.position-2)}:p));
          nextTurn();
        },1200);
      } else if(cellType==='wild'){
        setTimeout(()=>setModal({type:'wild'}),400);
      } else {
        setTimeout(nextTurn,400);
      }
      return updated;
    });
  };

  const triggerQuiz=async()=>{
    setLoadingAI(true);
    const pool=QUIZ_DB;
    try {
      const randomBase=pool[Math.floor(Math.random()*pool.length)];
      const prompt=`Você é um especialista em Copa do Mundo. Gere UMA pergunta de quiz inédita sobre Copa do Mundo relacionada ao tema "${randomBase.category}". Responda APENAS em JSON válido com este formato exato sem markdown: {"q":"pergunta aqui","a":"resposta correta","opts":["opcao1","opcao2","opcao3","opcao4"]}. A resposta correta deve estar dentro de opts. Use apenas fatos reais.`;
      const resp=await fetch('https://api.anthropic.com/v1/messages',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({model:'claude-sonnet-4-20250514',max_tokens:400,messages:[{role:'user',content:prompt}]})
      });
      if(resp.ok){
        const data=await resp.json();
        const text=data.content?.map(c=>c.text||'').join('');
        const match=text.match(/\{[\s\S]*?\}/);
        if(match){
          const parsed=JSON.parse(match[0]);
          if(parsed.q&&parsed.a&&Array.isArray(parsed.opts)&&parsed.opts.length===4){
            setLoadingAI(false);
            setQuizState({...parsed,answered:false,selected:null,aiGenerated:true});
            return;
          }
        }
      }
    } catch(e){}
    const q=pool[Math.floor(Math.random()*pool.length)];
    setLoadingAI(false);
    setQuizState({...q,answered:false,selected:null,aiGenerated:false});
  };

  const answerQuiz=(opt)=>{
    if(!quizState||quizState.answered) return;
    const correct=opt===quizState.a;
    const cp=gameState.currentPlayer;
    setQuizState(prev=>({...prev,answered:true,selected:opt}));
    setPlayers(prev=>prev.map((p,i)=>i===cp?{
      ...p,quizCorrect:p.quizCorrect+(correct?1:0),quizTotal:p.quizTotal+1,
      score:p.score+(correct?20:0),
      position:correct?Math.min(p.position+2,BOARD_SIZE-1):Math.max(0,p.position-1),
    }:p));
    showToast(correct?'✅ Correto! +20pts e avança 2!':'❌ Errado! Volta 1 casa');
    setTimeout(()=>{setQuizState(null);nextTurn();},2200);
  };

  const nextTurn=()=>{
    setGameState(prev=>({...prev,currentPlayer:(prev.currentPlayer+1)%numPlayers,turn:prev.turn+1,phase:'roll'}));
  };

  const endGame=(winnerId,finalPlayers)=>{
    const pList=finalPlayers||players;
    const winner=pList[winnerId];
    const sorted=[...pList].sort((a,b)=>b.score-a.score);
    saveRanking({winner:winner.name,country:winner.country.name,flag:winner.country.flag,score:winner.score,players:pList.length});
    setModal({type:'gameover',winner,sorted});
  };

  const wildChoice=(extra)=>{
    const cp=gameState.currentPlayer;
    setPlayers(prev=>prev.map((p,i)=>i===cp?{...p,position:Math.min(p.position+extra,BOARD_SIZE-1)}:p));
    setModal(null);
    showToast(`📺 VAR: Avança ${extra} casas!`);
    setTimeout(nextTurn,600);
  };

  const getCellBg=(type)=>({
    start:'linear-gradient(135deg,#FFD700,#FFA500)',
    finish:'linear-gradient(135deg,#C8102E,#8B0000)',
    quiz:'linear-gradient(135deg,#003DA5,#001a5e)',
    bonus:'linear-gradient(135deg,#00A651,#004d25)',
    penalty:'linear-gradient(135deg,#8B0000,#4a0000)',
    wild:'linear-gradient(135deg,#6B21A8,#3b0764)',
    normal:'#1a6b2e',
  }[type]||'#1a6b2e');

  // Build board rows (serpentine)
  const boardRows=[];
  for(let r=0;r<4;r++){
    const row=[];
    for(let c=0;c<10;c++){
      const idx=r%2===0?(3-r)*10+c:(3-r)*10+(9-c);
      row.push(idx);
    }
    boardRows.push(row);
  }

  const currentPlayer=players[gameState?.currentPlayer]||null;

  return (
    <div>
      {toast&&<div className="toast">{toast}</div>}

      {/* Modal Gameover */}
      {modal?.type==='gameover'&&(
        <div className="modal-bg">
          <div className="modal" style={{textAlign:'center'}}>
            <div style={{fontSize:'3rem',marginBottom:'8px'}}>🏆</div>
            <div style={{fontFamily:'Bebas Neue',fontSize:'2.5rem',color:'var(--gold)',letterSpacing:'3px',lineHeight:1}}>CAMPEÃO!</div>
            <div style={{fontSize:'2rem',margin:'12px 0'}}>{modal.winner.country.flag}</div>
            <div style={{fontSize:'1.3rem',fontWeight:'800',marginBottom:'4px'}}>{modal.winner.name}</div>
            <div style={{color:'rgba(255,255,255,0.5)',fontSize:'0.9rem',marginBottom:'1.5rem'}}>{modal.winner.country.name} • {modal.winner.score}pts</div>
            <div style={{height:'1px',background:'rgba(255,255,255,0.08)',margin:'1rem 0'}}/>
            <div style={{display:'flex',flexDirection:'column',gap:'8px',marginTop:'1rem'}}>
              {modal.sorted.map((p,i)=>(
                <div key={p.id} className="rank-row" style={{opacity:i===0?1:0.7}}>
                  <span style={{fontSize:'1.2rem'}}>{['🥇','🥈','🥉','4️⃣'][i]}</span>
                  <span>{p.country.flag}</span>
                  <span style={{flex:1,fontWeight:'700',fontSize:'0.9rem'}}>{p.name}</span>
                  <span className="badge badge-gold">{p.score}pts</span>
                  <span style={{fontSize:'0.75rem',color:'rgba(255,255,255,0.4)'}}>{p.quizCorrect}/{p.quizTotal}</span>
                </div>
              ))}
            </div>
            <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:'10px',marginTop:'1.5rem'}}>
              <button className="btn btn-secondary" style={{padding:'12px'}} onClick={()=>{setModal(null);startSetup();}}>Nova Partida</button>
              <button className="btn btn-primary" style={{padding:'12px'}} onClick={()=>{setModal(null);setScreen('home');}}>Início</button>
            </div>
          </div>
        </div>
      )}

      {/* Modal VAR */}
      {modal?.type==='wild'&&(
        <div className="modal-bg">
          <div className="modal">
            <div style={{textAlign:'center',marginBottom:'1.5rem'}}>
              <div style={{fontSize:'2.5rem'}}>📺</div>
              <h2 style={{fontFamily:'Bebas Neue',fontSize:'1.8rem',color:'#c084fc',letterSpacing:'2px',marginTop:'8px'}}>VAR EM AÇÃO!</h2>
              <p style={{color:'rgba(255,255,255,0.6)',fontSize:'0.9rem',marginTop:'4px'}}>Escolha quantas casas avançar</p>
            </div>
            <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:'10px'}}>
              {[1,2,3,4,5,6].map(n=>(
                <button key={n} className="btn btn-secondary" style={{fontSize:'1.4rem',fontWeight:'800',padding:'16px',borderRadius:'12px'}} onClick={()=>wildChoice(n)}>{n}</button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* HOME */}
      {screen==='home'&&(
        <div className="screen fade-in" style={{background:'radial-gradient(ellipse at 50% -10%,rgba(0,166,81,0.2) 0%,transparent 60%)'}}>
          <div style={{textAlign:'center',marginBottom:'2.5rem'}}>
            <div style={{fontSize:'3.5rem',marginBottom:'8px'}}>⚽</div>
            <div className="logo">Copa do Mundo</div>
            <div style={{fontFamily:'Bebas Neue',fontSize:'clamp(1.2rem,4vw,2rem)',color:'#fff'}}>Jogo de Tabuleiro</div>
            <div className="subtitle" style={{marginTop:'8px'}}>MULTIPLAYER • QUIZ COM IA • RANKING</div>
          </div>
          <div style={{display:'flex',flexDirection:'column',gap:'12px',width:'100%',maxWidth:'320px',marginBottom:'2rem'}}>
            <button className="btn btn-primary" style={{width:'100%',padding:'16px',fontSize:'1.05rem'}} onClick={startSetup}>🏟️ &nbsp;Nova Partida</button>
            <button className="btn btn-secondary" style={{width:'100%',padding:'14px'}} onClick={()=>setScreen('ranking')}>🏆 &nbsp;Ranking Global ({rankings.length})</button>
          </div>
          <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:'10px',maxWidth:'340px',width:'100%',marginBottom:'1.5rem'}}>
            {[{icon:'👥',num:'2–4',lbl:'Jogadores'},{icon:'❓',num:'IA+DB',lbl:'Quiz'},{icon:'⚽',num:'40',lbl:'Casas'}].map(item=>(
              <div key={item.lbl} className="stat-box">
                <div style={{fontSize:'1.3rem'}}>{item.icon}</div>
                <div className="stat-num" style={{fontSize:'1rem'}}>{item.num}</div>
                <div className="stat-lbl">{item.lbl}</div>
              </div>
            ))}
          </div>
          <div style={{display:'flex',gap:'8px',flexWrap:'wrap',justifyContent:'center',maxWidth:'380px'}}>
            {[['quiz','❓ Quiz'],['bonus','⚽ Bônus'],['penalty','🟥 Falta'],['wild','📺 VAR']].map(([k,v])=>(
              <span key={k} className="badge" style={{background:k==='quiz'?'rgba(0,61,165,0.3)':k==='bonus'?'rgba(0,166,81,0.2)':k==='penalty'?'rgba(200,16,46,0.2)':'rgba(107,33,168,0.3)',color:'#fff',border:'none',fontSize:'0.72rem'}}>{v}</span>
            ))}
          </div>
        </div>
      )}

      {/* RANKING */}
      {screen==='ranking'&&(
        <div className="screen fade-in" style={{justifyContent:'flex-start',paddingTop:'1.5rem'}}>
          <div style={{width:'100%',maxWidth:'500px'}}>
            <div style={{display:'flex',alignItems:'center',gap:'12px',marginBottom:'1.5rem'}}>
              <button className="btn btn-secondary" style={{fontSize:'0.85rem',padding:'8px 14px'}} onClick={()=>setScreen('home')}>← Voltar</button>
              <div>
                <div style={{fontFamily:'Bebas Neue',fontSize:'1.8rem',color:'var(--gold)',letterSpacing:'2px',lineHeight:1}}>Ranking Global</div>
                <div style={{fontSize:'0.8rem',color:'rgba(255,255,255,0.4)'}}>{rankings.length} partidas registradas</div>
              </div>
            </div>
            {rankings.length===0?(
              <div style={{textAlign:'center',padding:'3rem',color:'rgba(255,255,255,0.3)'}}>
                <div style={{fontSize:'3rem',marginBottom:'1rem'}}>🏆</div>
                <div style={{fontWeight:'700'}}>Nenhuma partida ainda</div>
                <div style={{fontSize:'0.85rem',marginTop:'4px'}}>Jogue e apareça aqui!</div>
              </div>
            ):(
              <div style={{display:'flex',flexDirection:'column',gap:'10px'}}>
                {rankings.map((r,i)=>(
                  <div key={i} className="rank-row">
                    <span style={{fontSize:'1.2rem',minWidth:'28px',textAlign:'center'}}>{i===0?'🥇':i===1?'🥈':i===2?'🥉':`${i+1}º`}</span>
                    <span style={{fontSize:'1.3rem'}}>{r.flag}</span>
                    <div style={{flex:1}}>
                      <div style={{fontWeight:'800',fontSize:'0.9rem'}}>{r.winner}</div>
                      <div style={{fontSize:'0.75rem',color:'rgba(255,255,255,0.4)'}}>{r.country} • {r.players} jogadores • {r.date}</div>
                    </div>
                    <span className="badge badge-gold">{r.score}pts</span>
                  </div>
                ))}
              </div>
            )}
            {rankings.length>0&&(
              <button className="btn btn-danger" style={{marginTop:'1rem',fontSize:'0.8rem',padding:'8px 18px'}}
                onClick={()=>{if(confirm('Limpar ranking?')){setRankings([]);localStorage.removeItem(STORAGE_KEY);}}}>
                Limpar Ranking
              </button>
            )}
          </div>
        </div>
      )}

      {/* SETUP */}
      {screen==='setup'&&setupStep===0&&(
        <div className="screen fade-in">
          <div style={{width:'100%',maxWidth:'420px'}}>
            <button className="btn btn-secondary" style={{marginBottom:'1.5rem',fontSize:'0.85rem'}} onClick={()=>setScreen('home')}>← Voltar</button>
            <div style={{fontFamily:'Bebas Neue',fontSize:'2rem',color:'var(--gold)',letterSpacing:'2px',marginBottom:'4px'}}>Nova Partida</div>
            <p style={{color:'rgba(255,255,255,0.5)',fontSize:'0.9rem',marginBottom:'1.5rem'}}>Quantos jogadores vão jogar?</p>
            <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:'10px',marginBottom:'2rem'}}>
              {[2,3,4].map(n=>(
                <button key={n} onClick={()=>setNumPlayers(n)} style={{padding:'20px 10px',borderRadius:'12px',border:`2px solid ${numPlayers===n?'var(--gold)':'rgba(255,255,255,0.1)'}`,background:numPlayers===n?'rgba(255,215,0,0.1)':'var(--card2)',color:numPlayers===n?'var(--gold)':'#fff',cursor:'pointer',fontFamily:'Bebas Neue',fontSize:'2rem'}}>
                  {n}
                </button>
              ))}
            </div>
            <p style={{color:'rgba(255,255,255,0.6)',fontSize:'0.85rem',fontWeight:'600',marginBottom:'12px',textTransform:'uppercase',letterSpacing:'0.5px'}}>Nomes dos jogadores</p>
            <div style={{display:'flex',flexDirection:'column',gap:'8px',marginBottom:'2rem'}}>
              {Array.from({length:numPlayers},(_,i)=>(
                <div key={i} style={{display:'flex',alignItems:'center',gap:'10px'}}>
                  <div style={{width:'28px',height:'28px',borderRadius:'50%',background:PLAYER_COLORS[i],display:'flex',alignItems:'center',justifyContent:'center',fontSize:'0.75rem',fontWeight:'800',color:'#000',flexShrink:0}}>{i+1}</div>
                  <input value={playerNames[i]} onChange={e=>{const n=[...playerNames];n[i]=e.target.value;setPlayerNames(n);}}
                    style={{flex:1,background:'var(--card2)',border:'1px solid rgba(255,255,255,0.12)',borderRadius:'10px',padding:'10px 14px',color:'#fff',fontFamily:'Nunito',fontSize:'0.95rem',outline:'none'}}
                    placeholder={`Jogador ${i+1}`}/>
                </div>
              ))}
            </div>
            <button className="btn btn-primary" style={{width:'100%',padding:'15px'}} onClick={()=>setSetupStep(1)}>Escolher Países →</button>
          </div>
        </div>
      )}

      {screen==='setup'&&setupStep>0&&(()=>{
        const currentPlayerSetup=setupStep-1;
        return (
          <div className="screen fade-in" style={{justifyContent:'flex-start',paddingTop:'1.5rem'}}>
            <div style={{width:'100%',maxWidth:'500px'}}>
              <div style={{display:'flex',alignItems:'center',gap:'10px',marginBottom:'1.5rem'}}>
                <button className="btn btn-secondary" style={{fontSize:'0.8rem',padding:'6px 12px'}} onClick={()=>currentPlayerSetup===0?setSetupStep(0):setSetupStep(setupStep-1)}>←</button>
                <div style={{flex:1}}>
                  <div style={{display:'flex',justifyContent:'space-between',marginBottom:'6px',fontSize:'0.8rem',color:'rgba(255,255,255,0.5)'}}>
                    <span style={{color:'var(--gold)',fontWeight:'700'}}>{playerNames[currentPlayerSetup]||`Jogador ${currentPlayerSetup+1}`}</span>
                    <span>{setupStep}/{numPlayers}</span>
                  </div>
                  <div className="progress-bar"><div className="progress-fill" style={{width:`${(setupStep/numPlayers)*100}%`}}/></div>
                </div>
              </div>
              <div style={{fontFamily:'Bebas Neue',fontSize:'1.5rem',color:'var(--gold)',letterSpacing:'2px',marginBottom:'4px'}}>Escolha seu país</div>
              <div style={{display:'flex',alignItems:'center',gap:'8px',marginBottom:'1.2rem'}}>
                <div style={{width:'22px',height:'22px',borderRadius:'50%',background:PLAYER_COLORS[currentPlayerSetup],flexShrink:0}}/>
                <span style={{fontSize:'0.9rem',color:'rgba(255,255,255,0.6)'}}>{playerNames[currentPlayerSetup]||`Jogador ${currentPlayerSetup+1}`}</span>
                {getSelectedForPlayer(currentPlayerSetup)&&(
                  <span className="badge badge-green" style={{marginLeft:'auto'}}>✓ {getSelectedForPlayer(currentPlayerSetup).flag} {getSelectedForPlayer(currentPlayerSetup).name}</span>
                )}
              </div>
              <div className="country-grid" style={{marginBottom:'1.5rem'}}>
                {COUNTRIES.map(c=>{
                  const taken=isCountryTaken(c.id,currentPlayerSetup);
                  const selected=getSelectedForPlayer(currentPlayerSetup)?.id===c.id;
                  return (
                    <button key={c.id} className={`country-btn${selected?' selected':''}`} disabled={taken} onClick={()=>selectCountry(c,currentPlayerSetup)}>
                      <div style={{fontSize:'1.8rem',marginBottom:'4px'}}>{c.flag}</div>
                      <div style={{fontSize:'0.78rem',fontWeight:'700'}}>{c.name}</div>
                      {taken&&<div style={{fontSize:'0.65rem',color:'rgba(255,255,255,0.3)',marginTop:'2px'}}>Tomado</div>}
                    </button>
                  );
                })}
              </div>
              {setupStep<numPlayers?(
                <button className="btn btn-primary" style={{width:'100%',padding:'14px'}} disabled={!getSelectedForPlayer(currentPlayerSetup)} onClick={()=>setSetupStep(setupStep+1)}>
                  Próximo →
                </button>
              ):(
                <button className="btn btn-green" style={{width:'100%',padding:'14px',fontSize:'1.05rem'}} disabled={!getSelectedForPlayer(currentPlayerSetup)} onClick={startGame}>
                  🏟️ Iniciar Partida!
                </button>
              )}
            </div>
          </div>
        );
      })()}

      {/* GAME */}
      {screen==='game'&&gameState&&currentPlayer&&(
        <div style={{display:'flex',flexDirection:'column',alignItems:'center',padding:'0.75rem',minHeight:'100vh'}}>
          {/* Header */}
          <div style={{width:'100%',maxWidth:'720px',display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:'0.75rem',flexWrap:'wrap',gap:'6px'}}>
            <div style={{fontFamily:'Bebas Neue',fontSize:'1.3rem',color:'var(--gold)',letterSpacing:'2px'}}>⚽ COPA DO MUNDO</div>
            <div style={{display:'flex',gap:'8px',alignItems:'center'}}>
              <span style={{fontSize:'0.8rem',color:'rgba(255,255,255,0.4)'}}>Turno {gameState.turn}</span>
              <button className="btn btn-danger" style={{padding:'6px 14px',fontSize:'0.78rem'}} onClick={()=>{setScreen('home');setModal(null);setQuizState(null);}}>Sair</button>
            </div>
          </div>

          {/* Players strip */}
          <div style={{display:'flex',gap:'6px',width:'100%',maxWidth:'720px',marginBottom:'0.75rem',overflowX:'auto',paddingBottom:'4px'}}>
            {players.map((p,i)=>(
              <div key={p.id} className={`player-card-mini${i===gameState.currentPlayer?' active':''}`} style={{flexShrink:0}}>
                <div style={{width:'22px',height:'22px',borderRadius:'50%',background:p.color,display:'flex',alignItems:'center',justifyContent:'center',fontSize:'0.7rem',fontWeight:'800',color:'#000'}}>{i===gameState.currentPlayer?'▶':i+1}</div>
                <span>{p.country.flag}</span>
                <span style={{maxWidth:'65px',overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap',color:i===gameState.currentPlayer?'var(--gold)':'#fff'}}>{p.name}</span>
                <span className="badge badge-gold" style={{fontSize:'0.65rem',padding:'2px 7px'}}>{p.score}pts</span>
              </div>
            ))}
          </div>

          {/* Board */}
          <div style={{width:'100%',maxWidth:'720px',display:'grid',gridTemplateRows:'repeat(4,1fr)',gap:'3px',marginBottom:'0.75rem'}}>
            {boardRows.map((row,rowIdx)=>(
              <div key={rowIdx} style={{display:'grid',gridTemplateColumns:'repeat(10,1fr)',gap:'3px'}}>
                {row.map(cellIdx=>{
                  const type=CELL_TYPES[cellIdx];
                  const info=CELL_INFO[type];
                  const here=players.filter(p=>p.position===cellIdx);
                  return (
                    <div key={cellIdx} title={`Casa ${cellIdx+1}${info.label?' - '+info.label:''}`} style={{background:getCellBg(type),borderRadius:'5px',display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',position:'relative',aspectRatio:'1',border:type!=='normal'?'1px solid rgba(255,255,255,0.18)':'1px solid rgba(0,0,0,0.25)',overflow:'hidden',minWidth:0}}>
                      {type!=='normal'&&<span style={{fontSize:'clamp(0.5rem,1.5vw,0.9rem)',lineHeight:1}}>{info.icon}</span>}
                      {type==='normal'&&<span style={{fontSize:'clamp(0.4rem,1vw,0.6rem)',color:'rgba(255,255,255,0.25)',fontWeight:'700'}}>{cellIdx+1}</span>}
                      {here.length>0&&(
                        <div style={{position:'absolute',inset:0,display:'flex',flexWrap:'wrap',alignItems:'center',justifyContent:'center',gap:'1px',padding:'1px'}}>
                          {here.map(p=>(
                            <div key={p.id} style={{width:'clamp(9px,2.2vw,16px)',height:'clamp(9px,2.2vw,16px)',borderRadius:'50%',background:p.color,border:'1.5px solid #fff',boxShadow:'0 1px 4px rgba(0,0,0,0.6)',flexShrink:0}}/>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            ))}
          </div>

          {/* Quiz */}
          {(loadingAI||quizState)&&(
            <div style={{width:'100%',maxWidth:'720px',background:'var(--card)',border:'1px solid rgba(0,212,255,0.3)',borderRadius:'16px',padding:'1.25rem',marginBottom:'0.75rem',animation:'fadeIn 0.3s ease'}}>
              {loadingAI&&(
                <div style={{textAlign:'center',padding:'1rem'}}>
                  <div style={{fontSize:'1.5rem',marginBottom:'8px'}} className="pulse">🤖</div>
                  <div style={{color:'var(--accent)',fontWeight:'700',fontSize:'0.9rem'}}>Gerando pergunta com IA...</div>
                  <div style={{fontSize:'0.75rem',color:'rgba(255,255,255,0.4)',marginTop:'4px'}}>Claude está pensando numa boa pergunta</div>
                </div>
              )}
              {quizState&&!loadingAI&&(
                <>
                  <div style={{display:'flex',alignItems:'center',gap:'8px',marginBottom:'12px',flexWrap:'wrap'}}>
                    <span className="badge badge-blue">❓ QUIZ</span>
                    {quizState.aiGenerated&&<span className="badge" style={{background:'rgba(167,139,250,0.15)',color:'#a78bfa',border:'1px solid rgba(167,139,250,0.3)',fontSize:'0.65rem'}}>🤖 IA</span>}
                    <span style={{fontSize:'0.8rem',color:'rgba(255,255,255,0.5)',marginLeft:'auto'}}>+20pts se acertar • {currentPlayer.name}</span>
                  </div>
                  <p style={{fontWeight:'700',fontSize:'clamp(0.85rem,2.5vw,1rem)',marginBottom:'14px',lineHeight:1.4}}>{quizState.q}</p>
                  <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fit,minmax(180px,1fr))',gap:'8px'}}>
                    {quizState.opts.map(opt=>(
                      <button key={opt} className={`quiz-option${quizState.answered&&opt===quizState.a?' correct':quizState.answered&&opt===quizState.selected&&opt!==quizState.a?' wrong':''}`}
                        onClick={()=>!quizState.answered&&answerQuiz(opt)} disabled={quizState.answered}>
                        {opt}
                      </button>
                    ))}
                  </div>
                </>
              )}
            </div>
          )}

          {/* Controles */}
          {!quizState&&!loadingAI&&(
            <div style={{width:'100%',maxWidth:'720px',display:'flex',alignItems:'center',gap:'16px',background:'var(--card)',borderRadius:'16px',padding:'1rem 1.25rem',border:'1px solid rgba(255,255,255,0.08)',marginBottom:'0.75rem'}}>
              <div style={{flex:1}}>
                <div style={{fontSize:'0.72rem',color:'rgba(255,255,255,0.4)',fontWeight:'600',textTransform:'uppercase',letterSpacing:'0.5px',marginBottom:'6px'}}>Vez de jogar</div>
                <div style={{display:'flex',alignItems:'center',gap:'10px'}}>
                  <span style={{fontSize:'1.6rem'}}>{currentPlayer.country.flag}</span>
                  <div>
                    <div style={{fontWeight:'800',fontSize:'1rem',color:'var(--gold)'}}>{currentPlayer.name}</div>
                    <div style={{fontSize:'0.75rem',color:'rgba(255,255,255,0.4)'}}>Casa {currentPlayer.position+1}/40 • {currentPlayer.score}pts</div>
                  </div>
                </div>
              </div>
              <div style={{display:'flex',alignItems:'center',gap:'12px'}}>
                {lastDice!==null&&<div style={{fontSize:'2.5rem',lineHeight:1,minWidth:'36px',textAlign:'center'}}>{DICE_FACES[lastDice]}</div>}
                <div className={`dice${diceRolling?' rolling':''}`} onClick={rollDice} style={{cursor:diceRolling?'not-allowed':'pointer',opacity:diceRolling?0.7:1}}>
                  {diceRolling?'🎲':DICE_FACES[lastDice??0]}
                </div>
              </div>
            </div>
          )}

          {/* Placar */}
          <div style={{width:'100%',maxWidth:'720px',display:'grid',gridTemplateColumns:`repeat(${numPlayers},1fr)`,gap:'8px'}}>
            {[...players].sort((a,b)=>b.score-a.score).map((p,rank)=>(
              <div key={p.id} style={{background:'var(--card2)',borderRadius:'10px',padding:'8px 6px',textAlign:'center',border:`1px solid ${p.id===players[gameState.currentPlayer].id?'rgba(255,215,0,0.3)':'rgba(255,255,255,0.05)'}`}}>
                <div style={{fontSize:'0.75rem',marginBottom:'2px'}}>{['🥇','🥈','🥉','4️⃣'][rank]}</div>
                <div style={{fontSize:'1rem'}}>{p.country.flag}</div>
                <div style={{fontSize:'0.7rem',fontWeight:'700',color:p.id===players[gameState.currentPlayer].id?'var(--gold)':'#fff',overflow:'hidden',textOverflow:'ellipsis',whiteSpace:'nowrap',padding:'0 2px'}}>{p.name}</div>
                <div style={{fontSize:'0.85rem',fontWeight:'800',color:'var(--gold)'}}>{p.score}pts</div>
                <div style={{fontSize:'0.6rem',color:'rgba(255,255,255,0.35)'}}>Casa {p.position+1}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

ReactDOM.render(React.createElement(App), document.getElementById('root'));