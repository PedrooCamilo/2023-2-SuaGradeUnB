"""
Investigação mais profunda da Issue #248
Testando casos edge e formatações problemáticas
"""
import re


def get_week_days_original(data: str) -> list:
    """Função original"""
    hours_format = r"\d+\:\d+"
    regex = rf"[A-Z]\w?[a-z|ç]+\-?[a-z]*\s{hours_format}\sàs\s{hours_format}"
    occurrences = re.findall(regex, data)
    return occurrences


# Possíveis problemas:
test_cases = [
    # Caso 1: Horários com espaços extras
    ("Terça-feira  14:00 às 15:50  Quinta-feira  14:00 às 15:50", "Espaços duplos"),
    
    # Caso 2: "Quinta" sem hífen e "feira"
    ("Terça-feira 14:00 às 15:50 Quinta feira 14:00 às 15:50", "Quinta sem hífen"),
    
    # Caso 3: Variação na capitalização
    ("TERÇA-FEIRA 14:00 às 15:50 QUINTA-FEIRA 14:00 às 15:50", "Tudo maiúsculo"),
    
    # Caso 4: Quebra de linha entre dias
    ("Terça-feira 14:00 às 15:50\nQuinta-feira 14:00 às 15:50", "Com quebra de linha"),
    
    # Caso 5: Tabs ou outros caracteres
    ("Terça-feira 14:00 às 15:50\tQuinta-feira 14:00 às 15:50", "Com tab"),
    
    # Caso 6: Horário com horas de um dígito
    ("Terça-feira 8:00 às 9:50 Quinta-feira 8:00 às 9:50", "Horas com 1 dígito"),
    
    # Caso 7: "as" minúsculo em vez de "às"
    ("Terça-feira 14:00 as 15:50 Quinta-feira 14:00 as 15:50", "Sem acento em 'as'"),
    
    # Caso 8: Apenas código de horário sem expandir dias
    ("35T23", "Apenas código"),
    
    # Caso 9: Mistura de formatos
    ("35T23 Terça-feira  14:00 às 15:50", "Apenas um dia listado explicitamente"),
]

print("="*80)
print("INVESTIGAÇÃO ISSUE #248 - Casos Edge")
print("="*80)

for data, description in test_cases:
    result = get_week_days_original(data)
    print(f"\n{description}:")
    print(f"  Input: {repr(data)}")
    print(f"  Resultado: {result}")
    print(f"  Quantidade: {len(result)}")
    
    if len(result) == 0:
        print(f"  ⚠️ NENHUM RESULTADO - Este pode ser o problema!")


# HIPÓTESE: O problema pode estar no SCRAPING retornando dados mal formatados
print("\n" + "="*80)
print("HIPÓTESE: Dados reais do scraping podem estar em formato diferente")
print("="*80)
print("\nO regex atual funciona perfeitamente para dados bem formatados.")
print("Se a Issue #248 relata que 'apenas Terça está aparecendo', pode ser:")
print("  1. O scraping está retornando dados mal formatados")
print("  2. O frontend não está exibindo corretamente")
print("  3. Os dados no SIGAA para essa disciplina específica estão inconsistentes")
print("\nVamos verificar o que acontece se houver apenas 1 dia nas informações extraídas:")

# Simulando caso onde o scraping falhou em extrair o segundo dia
problematic_data = "35T23 Terça-feira 14:00 às 15:50"
result = get_week_days_original(problematic_data)
print(f"\n  Se o scraping retornar apenas: {repr(problematic_data)}")
print(f"  Resultado: {result}")
print(f"  Quantidade: {len(result)}")
print(f"  ✓ Regex funciona, mas se o dado vem incompleto, não há o que fazer!")
