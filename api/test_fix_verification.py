"""
Teste simples para verificar que a correção da Issue #248 funciona
"""
import sys
from pathlib import Path

# Adicionar paths necessários
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.web_scraping import DisciplineWebScraper


def test_fix():
    """Testa a correção da Issue #248"""
    
    # Criar instância do scraper
    scraper = DisciplineWebScraper(
        department="650",
        year="2023",
        period="2",
        url="http://dummy",
        session=None,
        cookie={}
    )
    
    print("="*80)
    print("TESTE DA CORREÇÃO - Issue #248")
    print("="*80)
    
    # Teste 1: Espaços duplos (o bug original)
    print("\n✓ Teste 1: Espaços duplos entre dia e horário")
    data1 = "Terça-feira  14:00 às 15:50"
    result1 = scraper.get_week_days(data1)
    assert len(result1) == 1, f"FALHOU: Esperava 1, obteve {len(result1)}"
    print(f"  Input: {repr(data1)}")
    print(f"  Output: {result1}")
    print(f"  ✓ PASSOU")
    
    # Teste 2: Múltiplos dias com espaços extras
    print("\n✓ Teste 2: Múltiplos dias com espaços extras (caso Issue #248)")
    data2 = "35T23  Terça-feira  14:00 às  15:50  Quinta-feira  14:00  às  15:50"
    result2 = scraper.get_week_days(data2)
    assert len(result2) == 2, f"FALHOU: Esperava 2, obteve {len(result2)}"
    print(f"  Input: {repr(data2)}")
    print(f"  Output: {result2}")
    print(f"  ✓ PASSOU")
    
    # Teste 3: Caso normal (regressão)
    print("\n✓ Teste 3: Caso normal sem espaços extras (regressão)")
    data3 = "Terça-feira 14:00 às 15:50 Quinta-feira 14:00 às 15:50"
    result3 = scraper.get_week_days(data3)
    assert len(result3) == 2, f"FALHOU: Esperava 2, obteve {len(result3)}"
    print(f"  Input: {repr(data3)}")
    print(f"  Output: {result3}")
    print(f"  ✓ PASSOU")
    
    # Teste 4: Três dias
    print("\n✓ Teste 4: Três dias da semana")
    data4 = "246M34 Segunda-feira 10:00 às 11:50 Quarta-feira 10:00 às 11:50 Sexta-feira 10:00 às 11:50"
    result4 = scraper.get_week_days(data4)
    assert len(result4) == 3, f"FALHOU: Esperava 3, obteve {len(result4)}"
    print(f"  Input: {repr(data4)}")
    print(f"  Output: {result4}")
    print(f"  ✓ PASSOU")
    
    print("\n" + "="*80)
    print("✓ TODOS OS TESTES PASSARAM - Correção implementada com sucesso!")
    print("="*80)


if __name__ == "__main__":
    test_fix()
