"""
INTEGRAÇÃO DO QUIZ GENERATOR COM STREAMLIT
Exemplo de como usar o gerador de perguntas no jogo

Copie e adapte essas funções no seu jogo_streamlit.py
"""

from quiz_generator import QuizGenerator
import streamlit as st
import os

# CONFIGURAÇÃO DO QUIZ GENERATOR
@st.cache_resource
def load_quiz_generator(database_url: str, ai_provider: str = "mock"):

    try:
        generator = QuizGenerator(
            database_url=database_url,
            ai_provider=ai_provider,
            database_type="csv"
        )
        return generator
    except Exception as e:
        st.error(f"Erro ao carregar banco de dados: {e}")
        return None

# GERAÇÃO DINÂMICA DE PERGUNTAS
def generate_dynamic_quiz(database_url: str, num_questions: int = 5, context: str = "", ai_provider: str = "mock") -> list:
    """
    Gera perguntas dinamicamente a partir de um banco de dados
    
    Args:
        database_url: URL ou caminho do banco de dados
        num_questions: Quantidade de perguntas a gerar
        context: Contexto para as perguntas (ex: "sobre Copa 2022")
        ai_provider: Provedor de IA
    
    Returns:
        Lista de perguntas formatadas
    """
    generator = load_quiz_generator(database_url, ai_provider)
    
    if generator is None:
        return []
    
    return generator.generate_questions(
        num_questions=num_questions,
        context=context
    )

# INTERFACE STREAMLIT PARA CONFIGURAR O QUIZ
def show_quiz_configuration_panel():
    st.sidebar.header("Configuração do Quiz")
    
    # Campo para URL do banco de dados
    database_url = st.sidebar.text_input("URL ou Caminho do Banco de Dados",value="projeto/data_raw/fifa-world-cup/wcmatches.csv", help="Pode ser um caminho local ou URL HTTP")
    
    # Selecionar o provedor da IA
    ai_provider = st.sidebar.selectbox("Provedor de IA", ["mock", "openai", "anthropic"], help="""
        - 'mock': Modo teste (não requer API)
        - 'openai': Requer Chave API da Openai
        - 'anthropic': Requer Chave API da Anthropic
        """
    )
    
    # Número de perguntas
    num_questions = st.sidebar.selectbox("Número de Perguntas", list(range(1,11,1)))
    
    # # Campo de contexto
    # context = st.sidebar.text_area(
    #     "Contexto (opcional)",
    #     value="",
    #     help="Ex: 'sobre artilheiros de Copa' para contexto específico"
    # )
    
    # Botão para testar conexão
    if st.sidebar.button("Testar Conexão"):
        generator = load_quiz_generator(database_url, ai_provider)
        if generator:
            summary = generator.get_data_summary()
            with st.sidebar.expander("Informações do Banco de Dados"):
                st.json(summary)
    
    return {
        'database_url': database_url,
        'ai_provider': ai_provider,
        'num_questions': num_questions,
        #'context': context
    }

# EXEMPLO COMPLETO DE USO NO JOGO
def example_game_integration():
    """
    Exemplo de como integrar no seu jogo_streamlit.py
    
    Cole isso no seu arquivo principal onde você quer usar o quiz dinâmico
    """
    
    st.set_page_config(page_title="FIFA Game", layout="wide")
    
    # Painel de configuração
    quiz_config = show_quiz_configuration_panel()
    
    # Título
    st.title("Jogo FIFA - Quiz Dinâmico")
    
    # Gerar novo quiz
    if st.button("Gerar Novo Quiz", use_container_width=True):
        with st.spinner("Gerando perguntas..."):
            questions = generate_dynamic_quiz(
                database_url=quiz_config['database_url'],
                num_questions=quiz_config['num_questions'],
                context=quiz_config['context'],
                ai_provider=quiz_config['ai_provider']
            )
        
        if questions:
            st.success(f"{len(questions)} perguntas geradas!")
            
            # Exibir perguntas
            for i, q in enumerate(questions, 1):
                with st.expander(f"Pergunta {i}: {q['q'][:60]}..."):
                    st.write(f"**Pergunta:** {q['q']}")
                    st.write(f"**Resposta:** {q['a']}")
                    st.write(f"**Opções:** {', '.join(q['opts'])}")
        else:
            st.warning("Nenhuma pergunta foi gerada. Verifique as configurações.")


# ============================================================================
# INSTRUÇÕES DE INSTALAÇÃO E CONFIGURAÇÃO
# ============================================================================

SETUP_INSTRUCTIONS = """
# 📋 INSTRUÇÕES DE INSTALAÇÃO

## 1. Dependências Necessárias

```bash
pip install pandas streamlit requests
```

## 2. Para Usar IA Real (Opcional)

### OpenAI:
```bash
pip install openai
# Configure a variável de ambiente:
# Windows (PowerShell):
$env:OPENAI_API_KEY = 'sua-chave-aqui'

# Windows (CMD):
set OPENAI_API_KEY=sua-chave-aqui

# Linux/Mac:
export OPENAI_API_KEY='sua-chave-aqui'
```

### Anthropic (Claude):
```bash
pip install anthropic
export ANTHROPIC_API_KEY='sua-chave-aqui'
```

## 3. Integrando ao seu Jogo

No seu `jogo_streamlit.py`, adicione no topo:

```python
from quiz_generator import QuizGenerator, generate_dynamic_quiz
```

Depois, substitua a seção de quiz com:

```python
# Configurar quiz dinâmico
DATABASE_URL = "projeto/data_raw/fifa-world-cup/wcmatches.csv"
AI_PROVIDER = "mock"  # Mude para "openai" se tiver API key

quiz = generate_dynamic_quiz(
    database_url=DATABASE_URL,
    num_questions=10,
    ai_provider=AI_PROVIDER
)
```

## 4. Fontes de Dados Compatíveis

### CSV Local:
```python
"projeto/data_raw/fifa-world-cup/wcmatches.csv"
```

### CSV Remota (HTTP):
```python
"https://raw.githubusercontent.com/user/repo/data.csv"
```

### JSON Local:
```python
"dados.json"
```

### JSON Remota:
```python
"https://api.exemplo.com/dados.json"
```

## 5. Exemplo Prático Completo

```python
import streamlit as st
from quiz_generator import QuizGenerator

# Criar gerador
generator = QuizGenerator(
    database_url="projeto/data_raw/fifa-world-cup/wcmatches.csv",
    ai_provider="mock",  # Use "openai" com API key
    database_type="csv"
)

# Gerar perguntas
questions = generator.generate_questions(
    num_questions=5,
    context="sobre Copa do Mundo"
)

# Usar no jogo
for q in questions:
    st.write(q['q'])
    resposta = st.radio("Escolha:", q['opts'])
```
"""

# ENDPOINT PARA SERVIR COMO API
def create_api_endpoint():
    """
    Se quiser usar como API, configure assim:
    
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    import uvicorn
    
    app = FastAPI()
    
    @app.get("/quiz")
    async def get_quiz(
        database_url: str,
        num_questions: int = 5,
        ai_provider: str = "mock",
        context: str = ""
    ):
        generator = QuizGenerator(database_url, ai_provider)
        questions = generator.generate_questions(num_questions, context)
        return JSONResponse(questions)
    
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)
    
    # Use assim:
    # curl "http://localhost:8000/quiz?database_url=dados.csv&num_questions=5"
    """
    pass

if __name__ == "__main__":
    print(SETUP_INSTRUCTIONS)
