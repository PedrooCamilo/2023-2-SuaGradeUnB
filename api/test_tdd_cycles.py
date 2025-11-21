"""
Ciclo TDD para Issue #248 - Display incorreto de horários

BUG IDENTIFICADO: O regex falha quando há espaços múltiplos entre
o nome do dia e o horário (comum em HTML/web scraping).

SOLUÇÃO: Trocar \s por \s+ no regex para aceitar um ou mais espaços.
"""
import re


def get_week_days_original(data: str) -> list:
    """Versão ORIGINAL com o bug (usar \s)"""
    hours_format = r"\d+\:\d+"
    regex = rf"[A-Z]\w?[a-z|ç]+\-?[a-z]*\s{hours_format}\sàs\s{hours_format}"
    occurrences = re.findall(regex, data)
    return occurrences


def get_week_days_fixed(data: str) -> list:
    """Versão CORRIGIDA (usar \s+)"""
    hours_format = r"\d+\:\d+"
    regex = rf"[A-Z]\w?[a-z|ç]+\-?[a-z]*\s+{hours_format}\s+às\s+{hours_format}"
    occurrences = re.findall(regex, data)
    return occurrences


print("="*80)
print("CICLO 1 TDD - Teste que reproduz o bug")
print("="*80)

# TESTE 1: Espaços duplos entre dia e horário
print("\n🔴 FASE RED - Teste deve FALHAR com código original")
data_double_space = "Terça-feira  14:00 às 15:50"
result_original = get_week_days_original(data_double_space)
print(f"Input: {repr(data_double_space)}")
print(f"Resultado Original: {result_original}")
print(f"Esperado: 1 resultado")
print(f"Status: {'✗ FALHOU' if len(result_original) == 0 else '✓ PASSOU (inesperado!)'}")

print("\n🟢 FASE GREEN - Teste deve PASSAR com correção")
result_fixed = get_week_days_fixed(data_double_space)
print(f"Resultado Corrigido: {result_fixed}")
print(f"Status: {'✓ PASSOU' if len(result_fixed) == 1 else '✗ FALHOU'}")

print("\n" + "="*80)
print("CICLO 2 TDD - Múltiplos dias com espaços extras")
print("="*80)

print("\n🔴 FASE RED")
data_multiple = "35T23  Terça-feira  14:00 às  15:50  Quinta-feira  14:00  às  15:50"
result_original_2 = get_week_days_original(data_multiple)
print(f"Input: {repr(data_multiple)}")
print(f"Resultado Original: {result_original_2}")
print(f"Esperado: 2 resultados")
print(f"Status: {'✗ FALHOU' if len(result_original_2) != 2 else '✓ PASSOU (inesperado!)'}")

print("\n🟢 FASE GREEN")
result_fixed_2 = get_week_days_fixed(data_multiple)
print(f"Resultado Corrigido: {result_fixed_2}")
print(f"Status: {'✓ PASSOU' if len(result_fixed_2) == 2 else '✗ FALHOU'}")

print("\n" + "="*80)
print("CICLO 3 TDD - Garantir que casos normais continuam funcionando")
print("="*80)

test_cases_regression = [
    ("Terça-feira 14:00 às 15:50", 1, "Um dia normal"),
    ("Terça-feira 14:00 às 15:50 Quinta-feira 14:00 às 15:50", 2, "Dois dias normais"),
    ("Segunda-feira 10:00 às 11:50 Quarta-feira 10:00 às 11:50 Sexta-feira 10:00 às 11:50", 3, "Três dias"),
]

print("\n🟢 Testes de Regressão (não devem quebrar):")
all_passed = True
for data, expected, desc in test_cases_regression:
    result = get_week_days_fixed(data)
    passed = len(result) == expected
    all_passed = all_passed and passed
    status = "✓" if passed else "✗"
    print(f"  {status} {desc}: esperado={expected}, obtido={len(result)}")

print(f"\nStatus Geral: {'✓ TODOS PASSARAM' if all_passed else '✗ ALGUNS FALHARAM'}")

print("\n" + "="*80)
print("RESUMO DA CORREÇÃO")
print("="*80)
print("\nREGEX ORIGINAL (bugado):")
print("  [A-Z]\\w?[a-z|ç]+\\-?[a-z]*\\s\\d+\\:\\d+\\sàs\\s\\d+\\:\\d+")
print("                              ^ apenas 1 espaço")
print("\nREGEX CORRIGIDO:")
print("  [A-Z]\\w?[a-z|ç]+\\-?[a-z]*\\s+\\d+\\:\\d+\\s+às\\s+\\d+\\:\\d+")
print("                              ^^ 1 ou mais espaços")
print("\nMUDANÇA: Trocar todos os \\s por \\s+ para aceitar múltiplos espaços")
print("IMPACTO: Resolve Issue #248 quando HTML tem espaços extras")
