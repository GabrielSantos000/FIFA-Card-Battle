# 🎮 Quiz Generator - Sistema de Geração de Perguntas com IA

Módulo inteligente para gerar perguntas de quiz dinamicamente a partir de bancos de dados FIFA usando IA.

## 📋 Funcionalidades

- ✅ **Suporte a múltiplas fontes de dados**: CSV local, CSV remota, JSON
- ✅ **Integração com IA**: OpenAI, Anthropic Claude, ou modo simulação
- ✅ **Banco de dados configurável**: Use qualquer banco de dados via URL
- ✅ **Perguntas dinâmicas**: Geradas em tempo real com contexto customizável
- ✅ **Integração com Streamlit**: Pronto para usar no seu jogo
- ✅ **Fallback automático**: Retorna perguntas padrão se algo falhar

## 🚀 Instalação Rápida

### 1. Dependências Básicas

```bash
pip install pandas streamlit requests
```

### 2. Com IA Real (Opcional)

#### OpenAI GPT-3.5/4:

```bash
pip install openai
```

Configurar chave API:

```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY = 'sk-...'

# Linux/Mac
export OPENAI_API_KEY='sk-...'
```

#### Anthropic Claude:

```bash
pip install anthropic
```

```bash
# Windows (PowerShell)
$env:ANTHROPIC_API_KEY = 'sk-ant-...'

# Linux/Mac
export ANTHROPIC_API_KEY='sk-ant-...'
```

## 📖 Exemplos de Uso

### Exemplo Básico (Sem IA - Modo Simulação)

```python
from quiz_generator import QuizGenerator

# Criar gerador a partir de CSV local
generator = QuizGenerator(
    database_url="projeto/data_raw/fifa-world-cup/wcmatches.csv",
    ai_provider="mock",  # Modo simulação
    database_type="csv"
)

# Gerar 5 perguntas
perguntas = generator.generate_questions(
    num_questions=5,
    context="sobre Copa do Mundo"
)

# Ver as perguntas
for p in perguntas:
    print(f"❓ {p['q']}")
    print(f"✓ Resposta: {p['a']}")
    print(f"📋 Opções: {p['opts']}\n")
```

### Exemplo com OpenAI

```python
import os
os.environ['OPENAI_API_KEY'] = 'sua-chave-aqui'

from quiz_generator import QuizGenerator

generator = QuizGenerator(
    database_url="projeto/data_raw/fifa-world-cup/wcmatches.csv",
    ai_provider="openai",  # Usar OpenAI
    database_type="csv"
)

perguntas = generator.generate_questions(
    num_questions=10,
    context="perguntas sobre artilheiros da Copa 2022"
)
```

### Exemplo com Dados Remotos (URL)

```python
from quiz_generator import QuizGenerator

# CSV remota
generator = QuizGenerator(
    database_url="https://raw.githubusercontent.com/user/repo/data.csv",
    ai_provider="mock",
    database_type="csv"
)

perguntas = generator.generate_questions(num_questions=5)
```

### Exemplo com JSON

```python
from quiz_generator import QuizGenerator

# JSON local ou remota
generator = QuizGenerator(
    database_url="dados.json",  # ou URL completa
    ai_provider="anthropic",
    database_type="json"
)

perguntas = generator.generate_questions(
    num_questions=5,
    context="sobre jogadores de futebol"
)
```

## 🎯 Integração no Streamlit

### Opção 1: Adicionar ao `jogo_streamlit.py`

```python
# No topo do arquivo
from quiz_generator import QuizGenerator

# Depois, na seção onde as perguntas são usadas:
DATABASE_URL = "projeto/data_raw/fifa-world-cup/wcmatches.csv"
AI_PROVIDER = "mock"  # Mude para "openai" se tiver API

@st.cache_resource
def load_quiz_generator():
    return QuizGenerator(
        database_url=DATABASE_URL,
        ai_provider=AI_PROVIDER,
        database_type="csv"
    )

# Gerar perguntas dinâmicas
generator = load_quiz_generator()
quiz = generator.generate_questions(num_questions=10)
```

### Opção 2: Painel de Configuração (Recomendado)

```python
import streamlit as st
from quiz_generator import QuizGenerator

st.sidebar.header("⚙️ Configuração do Quiz")

# Campo para URL do banco de dados
db_url = st.sidebar.text_input(
    "URL do Banco de Dados",
    value="projeto/data_raw/fifa-world-cup/wcmatches.csv"
)

# Seletor de IA
ia = st.sidebar.selectbox("Provedor de IA", ["mock", "openai", "anthropic"])

# Número de perguntas
num_q = st.sidebar.slider("Número de Perguntas", 1, 10, 5)

# Contexto
contexto = st.sidebar.text_area("Contexto (opcional)")

# Gerar quiz
if st.sidebar.button("Gerar Quiz"):
    generator = QuizGenerator(db_url, ai_provider=ia, database_type="csv")
    perguntas = generator.generate_questions(num_q, contexto)

    for p in perguntas:
        st.write(f"**{p['q']}**")
        resposta = st.radio("Escolha:", p['opts'], key=p['q'])
```

## 🗄️ Formatos de Banco de Dados Suportados

### CSV Local

```python
database_url = "projeto/data_raw/fifa-world-cup/wcmatches.csv"
database_type = "csv"
```

### CSV Remota (HTTP/HTTPS)

```python
database_url = "https://raw.githubusercontent.com/user/repo/data.csv"
database_type = "csv"
```

### JSON Local

```python
database_url = "dados.json"
database_type = "json"
```

### JSON Remota

```python
database_url = "https://api.exemplo.com/dados.json"
database_type = "json"
```

## 🤖 Provedores de IA

### 1. Mock (Simulação - Recomendado para Testes)

```python
generator = QuizGenerator(
    database_url="dados.csv",
    ai_provider="mock"
)
```

- ✅ Não requer API key
- ✅ Rápido para testes
- ⚠️ Perguntas básicas/genéricas

### 2. OpenAI GPT-3.5/4

```python
import os
os.environ['OPENAI_API_KEY'] = 'sk-...'

generator = QuizGenerator(
    database_url="dados.csv",
    ai_provider="openai"
)
```

- ✅ Perguntas de alta qualidade
- ✅ Modelo GPT-3.5 turbo (rápido e barato)
- ⚠️ Requer créditos

### 3. Anthropic Claude

```python
import os
os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-...'

generator = QuizGenerator(
    database_url="dados.csv",
    ai_provider="anthropic"
)
```

- ✅ Excelente qualidade
- ✅ Menos custo que OpenAI
- ⚠️ Um pouco mais lento

## 📊 Consultar Informações do Banco de Dados

```python
from quiz_generator import QuizGenerator

generator = QuizGenerator(
    database_url="projeto/data_raw/fifa-world-cup/wcmatches.csv",
    database_type="csv"
)

# Ver informações do banco
info = generator.get_data_summary()

print(info)
# Retorna:
# {
#   'status': 'success',
#   'rows': 412,
#   'columns': 15,
#   'column_names': ['Date', 'Home Team', 'Away Team', ...],
#   'data_types': {'Date': 'object', 'Home Team': 'object', ...},
#   'sample': [...]
# }
```

## 🔧 Configuração Avançada

### Usar Chave API Customizada

```python
generator = QuizGenerator(
    database_url="dados.csv",
    ai_provider="openai",
    api_key="sua-chave-customizada-aqui",  # Sobrescreve variável de ambiente
    database_type="csv"
)
```

### Tratamento de Erros

```python
from quiz_generator import QuizGenerator

try:
    generator = QuizGenerator(
        database_url="dados_invalidos.csv",
        ai_provider="openai"
    )

    if generator.data is None:
        print("Erro: Banco de dados não carregado")
    else:
        perguntas = generator.generate_questions(5)

except Exception as e:
    print(f"Erro: {e}")
```

## 💡 Boas Práticas

1. **Use Cache no Streamlit**: Não recarregue o gerador em cada execução

   ```python
   @st.cache_resource
   def load_generator():
       return QuizGenerator(...)
   ```

2. **Validar Banco de Dados**: Sempre teste a conexão

   ```python
   info = generator.get_data_summary()
   if info['status'] != 'success':
       st.error("Erro ao carregar banco")
   ```

3. **Fornecer Contexto**: Seja específico para perguntas melhores

   ```python
   generator.generate_questions(
       num_questions=5,
       context="sobre finais de Copa do Mundo"
   )
   ```

4. **Usar Mode Mock para Testes**: Não gaste API credits desnecessariamente
   ```python
   ai_provider = "mock" if mode_teste else "openai"
   ```

## 📂 Bancos de Dados Recomendados no Projeto

```
projeto/data_raw/fifa-world-cup/
├── wcmatches.csv                 # Histórico de partidas
├── WorldCupMatches.csv           # Detalhes das partidas
├── WorldCupPlayers.csv           # Dados de jogadores
├── WorldCups.csv                 # Torneios
└── FIFA - <ano>.csv              # Por ano (1930-2022)
```

### Exemplo: Usar dados de 2022

```python
generator = QuizGenerator(
    database_url="projeto/data_raw/fifa-football-world-cup-dataset/FIFA - 2022.csv",
    ai_provider="mock"
)

perguntas = generator.generate_questions(
    num_questions=5,
    context="sobre Copa do Mundo 2022"
)
```

## 🐛 Troubleshooting

### "Erro ao carregar banco de dados"

```python
# Verificar se caminho está correto
import os
print(os.path.exists("caminho/do/arquivo.csv"))

# Se remota, testar URL
import requests
response = requests.head("https://url-do-arquivo.csv")
print(response.status_code)  # Deve ser 200
```

### "ModuleNotFoundError: No module named 'openai'"

```bash
pip install openai
```

### "API key inválida"

```bash
# Verificar variável de ambiente
import os
print(os.getenv("OPENAI_API_KEY"))  # Não deve ser None

# Ou passar manualmente
generator = QuizGenerator(
    database_url="dados.csv",
    ai_provider="openai",
    api_key="sua-chave-aqui"
)
```

### Perguntas muito genéricas/ruins

- Mude para `ai_provider="openai"` (melhor qualidade)
- Aumente o `context` com mais detalhes
- Mude o banco de dados para dados mais ricos

## 📝 Estrutura de Resposta

Todas as perguntas retornam no formato:

```python
{
    'q': 'string - a pergunta',
    'a': 'string - resposta correta',
    'opts': ['list', 'de', 'opções', 'resposta']
}
```

⚠️ **Importante**: A resposta correta SEMPRE está incluída em `opts`

## 🤝 Contribuindo

Sugestões de melhorias:

- Adicionar mais provedores de IA (Hugging Face, Google VertexAI, etc.)
- Suporte a banco de dados SQL (MySQL, PostgreSQL)
- Cache de perguntas geradas
- Validação de qualidade de perguntas

## 📄 Licença

MIT License - Use livremente!

---

**Dúvidas?** Verifique os exemplos em `quiz_integration_example.py` ou execute:

```bash
python quiz_generator.py
```
