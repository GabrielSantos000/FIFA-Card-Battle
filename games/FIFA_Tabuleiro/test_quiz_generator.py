"""
SCRIPT DE TESTE - Quiz Generator
Execute este arquivo para testar o gerador de quiz com diferentes configurações
"""

import os
import sys
from pathlib import Path

# Adicionar diretório ao path
sys.path.insert(0, str(Path(__file__).parent))

from quiz_generator import QuizGenerator, create_quiz_from_csv


def print_section(title):
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def test_csv_local():
    """Teste 1: Carregar CSV local"""
    print_section("TESTE 1: Carregar CSV Local")
    
    csv_path = os.path.join("projeto","data_raw","fifa-world-cup-2022-complete-dataset","Fifa_world_cup_matches.csv")

    if not os.path.exists(csv_path):
        print(f"Arquivo não encontrado: {csv_path}")
        print("Procurando por arquivos CSV alternativos...")
        
        # Procurar por alternativas
        for root, dirs, files in os.walk("projeto\data_raw"):
            for file in files:
                if file.endswith(".csv"):
                    csv_path = os.path.join(root, file)
                    print(f"Encontrado: {csv_path}")
                    break
    
    try:
        generator = QuizGenerator(
            database_url=csv_path,
            ai_provider="mock",
            database_type="csv"
        )
        
        # Ver informações
        info = generator.get_data_summary()
        print(f"Status: {info['status']}")
        print(f"Linhas: {info['rows']}")
        print(f"Colunas: {info['columns']}")
        print(f"Nomes das colunas: {', '.join(info['column_names'][:5])}...")
        
        # Gerar perguntas
        print("\n📋 Gerando perguntas...")
        questions = generator.generate_questions(num_questions=3)
        
        for i, q in enumerate(questions, 1):
            print(f"\n  Pergunta {i}:")
            print(f"    ❓ {q['q']}")
            print(f"    ✓ Resposta: {q['a']}")
            print(f"    📋 Opções: {q['opts']}")
        
        print("\n✅ Teste concluído com sucesso!")
        return True
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_mock_mode():
    """Teste 2: Modo Mock (sem IA)"""
    print_section("TESTE 2: Modo Mock (Simulação)")
    
    # Usar um CSV simples se existir
    csv_path = "../../projeto/data_raw/fifa-world-cup/wcmatches.csv"
    
    if not os.path.exists(csv_path):
        csv_path = "README_QUIZ_GENERATOR.md"
    
    try:
        generator = QuizGenerator(
            database_url=csv_path,
            ai_provider="mock",
            database_type="csv"
        )
        
        questions = generator.generate_questions(
            num_questions=2,
            context="sobre futebol"
        )
        
        print("✓ Modo Mock funcionando!")
        print(f"  Perguntas geradas: {len(questions)}")
        
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_openai_availability():
    """Teste 3: Verificar disponibilidade de OpenAI"""
    print_section("TESTE 3: Verificar OpenAI")
    
    try:
        from openai import OpenAI
        print("Biblioteca OpenAI está instalada")
        
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            print("OPENAI_API_KEY encontrada")
            print(f"(Primeiros 10 caracteres: {api_key[:10]}...)")
            return True
        else:
            print("Chave API da OpenAI não configurada")
            print("Configure com: $env:OPENAI_API_KEY = 'sua-chave'")
            return False
    
    except ImportError:
        print("OpenAI não instalado")
        print("Instale com: pip install openai")
        return False


def test_anthropic_availability():
    """Teste 4: Verificar disponibilidade de Anthropic"""
    print_section("TESTE 4: Verificar Anthropic")
    
    try:
        import anthropic
        print("✓ Biblioteca Anthropic está instalada")
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key:
            print("✓ ANTHROPIC_API_KEY encontrada")
            print(f"  (Primeiros 10 caracteres: {api_key[:10]}...)")
            return True
        else:
            print("⚠️  ANTHROPIC_API_KEY não configurada")
            print("  Configure com: $env:ANTHROPIC_API_KEY = 'sua-chave'")
            return False
    
    except ImportError:
        print("⚠️  Anthropic não instalado")
        print("  Instale com: pip install anthropic")
        return False


def test_with_openai():
    """Teste 5: Gerar perguntas com OpenAI (se disponível)"""
    print_section("TESTE 5: Gerar com OpenAI")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("⚠️  OPENAI_API_KEY não configurada")
        print("  Pulando este teste...")
        return None
    
    csv_path = "../../projeto/data_raw/fifa-world-cup/wcmatches.csv"
    if not os.path.exists(csv_path):
        csv_path = "README_QUIZ_GENERATOR.md"
    
    try:
        print("🚀 Enviando requisição para OpenAI (isso pode levar alguns segundos)...")
        
        generator = QuizGenerator(
            database_url=csv_path,
            ai_provider="openai",
            database_type="csv"
        )
        
        questions = generator.generate_questions(
            num_questions=2,
            context="sobre Copa do Mundo 2022"
        )
        
        print("✓ Perguntas geradas com sucesso!")
        
        for i, q in enumerate(questions, 1):
            print(f"\n  Pergunta {i}:")
            print(f"    ❓ {q['q']}")
            print(f"    ✓ {q['a']}")
        
        return True
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_different_contexts():
    """Teste 6: Gerar perguntas com diferentes contextos"""
    print_section("TESTE 6: Diferentes Contextos")
    
    csv_path = "../../projeto/data_raw/fifa-world-cup/wcmatches.csv"
    if not os.path.exists(csv_path):
        print("⚠️  CSV não encontrado, pulando teste...")
        return None
    
    try:
        generator = QuizGenerator(
            database_url=csv_path,
            ai_provider="mock",
            database_type="csv"
        )
        
        contextos = [
            "sobre países campeões",
            "sobre artilheiros",
            "sobre anos 1950-1980",
        ]
        
        for ctx in contextos:
            print(f"\nContexto: '{ctx}'")
            questions = generator.generate_questions(
                num_questions=1,
                context=ctx
            )
            if questions:
                print(f"  ✓ {questions[0]['q'][:70]}...")
        
        return True
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def test_rapid_generation():
    """Teste 7: Teste de velocidade"""
    print_section("TESTE 7: Teste de Velocidade")
    
    csv_path = "../../projeto/data_raw/fifa-world-cup/wcmatches.csv"
    if not os.path.exists(csv_path):
        print("⚠️  CSV não encontrado, pulando teste...")
        return None
    
    try:
        import time
        
        generator = QuizGenerator(
            database_url=csv_path,
            ai_provider="mock",
            database_type="csv"
        )
        
        start = time.time()
        questions = generator.generate_questions(num_questions=10)
        elapsed = time.time() - start
        
        print(f"✓ Gerou 10 perguntas em {elapsed:.2f} segundos")
        print(f"  Velocidade: {10/elapsed:.1f} perguntas/segundo")
        
        return True
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def show_summary(results):
    """Mostra resumo dos testes"""
    print_section("RESUMO DOS TESTES")
    
    tests = [
        ("CSV Local", results.get('csv_local')),
        ("Modo Mock", results.get('mock')),
        ("OpenAI Disponível", results.get('openai_avail')),
        ("Anthropic Disponível", results.get('anthropic_avail')),
        ("Geração com OpenAI", results.get('openai_gen')),
        ("Diferentes Contextos", results.get('contexts')),
        ("Teste de Velocidade", results.get('speed')),
    ]
    
    passed = sum(1 for _, r in tests if r is True)
    failed = sum(1 for _, r in tests if r is False)
    skipped = sum(1 for _, r in tests if r is None)
    
    print("Status dos Testes:")
    for name, result in tests:
        if result is True:
            symbol = "✅"
        elif result is False:
            symbol = "❌"
        else:
            symbol = "⏭️ "
        print(f"  {symbol} {name}")
    
    print(f"\nTotal: {passed} passou | {failed} falhou | {skipped} pulado")
    
    if failed == 0:
        print("\n🎉 Todos os testes obrigatórios passaram!")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os erros acima.")


def main():
    """Executa todos os testes"""
    print("\n" + "="*80)
    print("  TESTE DO QUIZ GENERATOR")
    print("="*80)
    print(f"\nDiretório atual: {os.getcwd()}")
    
    results = {}
    
    # Executar testes
    results['csv_local'] = test_csv_local()
    results['mock'] = test_mock_mode()
    results['openai_avail'] = test_openai_availability()
    results['anthropic_avail'] = test_anthropic_availability()
    results['openai_gen'] = test_with_openai()
    results['contexts'] = test_different_contexts()
    results['speed'] = test_rapid_generation()
    
    # Mostrar resumo
    show_summary(results)
    
    # Instruções finais
    print("\n" + "="*80)
    print("  PRÓXIMOS PASSOS")
    print("="*80)
    print("""
1. Para usar no seu jogo Streamlit:
   - Copie quiz_generator.py para seu projeto
   - Importe com: from quiz_generator import QuizGenerator
   
2. Exemplos de uso:
   - Veja quiz_integration_example.py
   - Leia README_QUIZ_GENERATOR.md
   
3. Para usar com IA real:
   - OpenAI: pip install openai
   - Anthropic: pip install anthropic
   - Configure suas chaves de API
   
4. Personalizar:
   - Mude database_url para seu banco de dados
   - Mude ai_provider para "openai" ou "anthropic"
   - Customize o context para melhor relevância
    """)


if __name__ == "__main__":
    main()
