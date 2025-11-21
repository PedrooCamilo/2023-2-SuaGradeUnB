"""
Teste simples da função get_week_days para Issue #248
Teste unitário puro sem dependências do Django
"""
import sys
from pathlib import Path

# Adicionar o diretório pai ao path para importar o módulo
sys.path.insert(0, str(Path(__file__).parent.parent))

from re import findall


def get_week_days_original(data: str) -> list:
    """Função original com o bug"""
    hours_format = r"\d+\:\d+"
    regex = rf"[A-Z]\w?[a-z|ç]+\-?[a-z]*\s{hours_format}\sàs\s{hours_format}"
    occurrences = findall(regex, data)
    return occurrences


def test_issue_248_terca_quinta():
    """
    Test para Issue #248: Paradigmas de Programação deveria mostrar 2 aulas
    mas apenas Terça está sendo exibida.
    """
    data = "35T23 Terça-feira 14:00 às 15:50 Quinta-feira 14:00 às 15:50"
    result = get_week_days_original(data)
    
    print(f"\nTeste Issue #248 - Terça e Quinta:")
    print(f"Input: {data}")
    print(f"Resultado: {result}")
    print(f"Quantidade encontrada: {len(result)}")
    print(f"Esperado: 2 dias")
    
    # Este teste DEVE FALHAR com o código original
    assert len(result) == 2, f"FALHOU: Esperava 2 dias, encontrou {len(result)}"
    assert "Terça-feira 14:00 às 15:50" in result
    assert "Quinta-feira 14:00 às 15:50" in result
    
    print("✓ Teste PASSOU!")


def test_single_day():
    """Test básico com um único dia"""
    data = "Terça-feira 14:00 às 15:50"
    result = get_week_days_original(data)
    
    print(f"\nTeste Único Dia:")
    print(f"Input: {data}")
    print(f"Resultado: {result}")
    print(f"Quantidade: {len(result)}")
    
    assert len(result) == 1
    print("✓ Teste PASSOU!")


def test_tres_dias():
    """Test com três dias (Segunda, Quarta, Sexta)"""
    data = "246M34 Segunda-feira 10:00 às 11:50 Quarta-feira 10:00 às 11:50 Sexta-feira 10:00 às 11:50"
    result = get_week_days_original(data)
    
    print(f"\nTeste Três Dias:")
    print(f"Input: {data}")
    print(f"Resultado: {result}")
    print(f"Quantidade: {len(result)}")
    print(f"Esperado: 3 dias")
    
    assert len(result) == 3, f"FALHOU: Esperava 3 dias, encontrou {len(result)}"
    print("✓ Teste PASSOU!")


def test_quinta_feira_only():
    """Test específico para Quinta-feira sozinha"""
    data = "Quinta-feira 14:00 às 15:50"
    result = get_week_days_original(data)
    
    print(f"\nTeste Quinta-feira sozinha:")
    print(f"Input: {data}")
    print(f"Resultado: {result}")
    print(f"Quantidade: {len(result)}")
    
    assert len(result) == 1, f"FALHOU: Esperava 1 dia, encontrou {len(result)}"
    assert "Quinta-feira" in result[0]
    print("✓ Teste PASSOU!")


def test_regex_breakdown():
    """Testa componentes individuais do regex"""
    test_cases = [
        ("Segunda-feira 10:00 às 11:50", "Segunda-feira"),
        ("Terça-feira 10:00 às 11:50", "Terça-feira"),
        ("Quarta-feira 10:00 às 11:50", "Quarta-feira"),
        ("Quinta-feira 10:00 às 11:50", "Quinta-feira"),
        ("Sexta-feira 10:00 às 11:50", "Sexta-feira"),
        ("Sábado 10:00 às 11:50", "Sábado"),
    ]
    
    print(f"\nTeste Individual de Cada Dia:")
    for data, expected_day in test_cases:
        result = get_week_days_original(data)
        status = "✓" if len(result) == 1 and expected_day in result[0] else "✗"
        print(f"{status} {expected_day}: {len(result)} encontrado(s) - {result}")


if __name__ == "__main__":
    print("="*70)
    print("TESTES PARA ISSUE #248 - Display incorreto de horários")
    print("="*70)
    
    try:
        test_single_day()
    except AssertionError as e:
        print(f"✗ FALHOU: {e}")
    
    try:
        test_quinta_feira_only()
    except AssertionError as e:
        print(f"✗ FALHOU: {e}")
    
    try:
        test_issue_248_terca_quinta()
    except AssertionError as e:
        print(f"✗ FALHOU: {e}")
    
    try:
        test_tres_dias()
    except AssertionError as e:
        print(f"✗ FALHOU: {e}")
    
    try:
        test_regex_breakdown()
    except AssertionError as e:
        print(f"✗ FALHOU: {e}")
    
    print("\n" + "="*70)
    print("ANÁLISE DO REGEX:")
    print("="*70)
    print(f"Regex atual: [A-Z]\\w?[a-z|ç]+\\-?[a-z]*\\s\\d+\\:\\d+\\sàs\\s\\d+\\:\\d+")
    print("\nComponentes:")
    print("  [A-Z]         - Uma letra maiúscula inicial")
    print("  \\w?           - ZERO ou UM caractere word (letras, dígitos, _)")
    print("  [a-z|ç]+      - UM ou MAIS de: a-z OU | OU ç")
    print("  \\-?           - Hífen opcional")
    print("  [a-z]*        - ZERO ou MAIS letras minúsculas")
    print("  \\s            - Espaço")
    print("  \\d+\\:\\d+      - Hora (HH:MM)")
    print("  \\sàs\\s        - ' às '")
    print("  \\d+\\:\\d+      - Hora (HH:MM)")
    print("\nProblema encontrado com '\\w?':")
    print("  - Para 'Terça-feira': T + e -> Teça??? NÃO!")
    print("  - O regex [a-z|ç]+ aceita 'r', 'ç', 'a' porque são a-z")
    print("  - Mas o '\\w?' está pegando apenas O 'e' de 'Terça'!")
    print("\nTESTE DETALHADO:")
    import re
    
    # Vamos testar o padrão passo a passo
    test_str = "Quinta-feira 14:00 às 15:50"
    hours_format = r"\d+\:\d+"
    
    patterns = [
        (r"[A-Z]", "Letra maiúscula"),
        (r"[A-Z]\w", "Maiúscula + 1 word char"),
        (r"[A-Z]\w?", "Maiúscula + 0ou1 word char"),
        (r"[A-Z]\w+", "Maiúscula + 1+ word chars"),
        (r"[A-Z]\w?[a-z|ç]+", "Padrão até minúsculas"),
        (r"[A-Z]\w?[a-z|ç]+\-?[a-z]*", "Padrão completo do nome"),
        (rf"[A-Z]\w?[a-z|ç]+\-?[a-z]*\s{hours_format}\sàs\s{hours_format}", "Padrão COMPLETO")
    ]
    
    print(f"\n  Testando: '{test_str}'")
    for pattern, desc in patterns:
        matches = re.findall(pattern, test_str)
        print(f"    {desc:40s}: {matches}")
