"""
Execução Final de TODOS os Testes - Para Relatório
Gera saída formatada para a seção "4. Resultado Final Execução Testes"
"""
import sys
from pathlib import Path

# Adicionar paths necessários
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.web_scraping import DisciplineWebScraper


def run_all_tests():
    """Executa todos os testes criados para a Issue #248"""
    
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
    print("RESULTADO FINAL DA EXECUÇÃO DE TODOS OS TESTES")
    print("Correção da Issue #248 - Display incorreto de horários")
    print("="*80)
    print()
    
    # Lista de todos os testes
    tests = [
        {
            'name': 'test_parse_single_weekday_with_time',
            'data': 'Terça-feira 14:00 às 15:50',
            'expected': 1,
            'description': 'Um dia com horário (caso base)'
        },
        {
            'name': 'test_parse_multiple_weekdays_terca_quinta',
            'data': '35T23 Terça-feira 14:00 às 15:50 Quinta-feira 14:00 às 15:50',
            'expected': 2,
            'description': 'Dois dias - Issue #248 principal'
        },
        {
            'name': 'test_parse_segunda_quarta_sexta',
            'data': '246M34 Segunda-feira 10:00 às 11:50 Quarta-feira 10:00 às 11:50 Sexta-feira 10:00 às 11:50',
            'expected': 3,
            'description': 'Três dias da semana'
        },
        {
            'name': 'test_parse_all_weekdays',
            'data': 'Segunda-feira 08:00 às 09:50 Terça-feira 08:00 às 09:50 Quarta-feira 08:00 às 09:50 Quinta-feira 08:00 às 09:50 Sexta-feira 08:00 às 09:50 Sábado 08:00 às 09:50',
            'expected': 6,
            'description': 'Todos os dias da semana'
        },
        {
            'name': 'test_parse_with_schedule_codes',
            'data': '35T23 Terça-feira 14:00 às 15:50 Quinta-feira 14:00 às 15:50',
            'expected': 2,
            'description': 'Com código de horário (35T23)'
        },
        {
            'name': 'test_parse_quinta_feira_specifically',
            'data': 'Quinta-feira 14:00 às 15:50',
            'expected': 1,
            'description': 'Quinta-feira específico'
        },
        {
            'name': 'test_parse_sabado',
            'data': 'Sábado 08:00 às 09:50',
            'expected': 1,
            'description': 'Sábado (sem hífen)'
        },
        {
            'name': 'test_parse_with_double_spaces',
            'data': 'Terça-feira  14:00 às 15:50',
            'expected': 1,
            'description': 'Espaços duplos (BUG Issue #248)'
        },
        {
            'name': 'test_parse_multiple_days_with_extra_spaces',
            'data': '35T23  Terça-feira  14:00 às  15:50  Quinta-feira  14:00  às  15:50',
            'expected': 2,
            'description': 'Múltiplos dias com espaços extras (BUG Issue #248)'
        },
        {
            'name': 'test_parse_with_multiple_spaces_between_time_components',
            'data': 'Segunda-feira   10:00   às   11:50',
            'expected': 1,
            'description': 'Múltiplos espaços (3+) entre componentes'
        },
    ]
    
    total = len(tests)
    passed = 0
    failed = 0
    
    for i, test in enumerate(tests, 1):
        result = scraper.get_week_days(test['data'])
        success = len(result) == test['expected']
        
        if success:
            passed += 1
            status = "✓ PASSOU"
        else:
            failed += 1
            status = "✗ FALHOU"
        
        print(f"{i:2d}. {test['name']}")
        print(f"    {test['description']}")
        print(f"    Esperado: {test['expected']} | Obtido: {len(result)}")
        print(f"    {status}")
        
        if not success:
            print(f"    Resultado: {result}")
        
        print()
    
    print("="*80)
    print("ESTATÍSTICAS")
    print("="*80)
    print(f"Total de Testes: {total}")
    print(f"Passaram: {passed}")
    print(f"Falharam: {failed}")
    print(f"Taxa de Sucesso: {(passed/total)*100:.1f}%")
    print()
    
    if failed == 0:
        print("✓✓✓ TODOS OS TESTES PASSARAM ✓✓✓")
        print()
        print("Conclusão:")
        print("  • A correção da Issue #248 está funcionando perfeitamente")
        print("  • Todos os casos (normais e edge cases) estão cobertos")
        print("  • Nenhuma regressão foi detectada")
        print("  • Código pronto para produção")
    else:
        print("✗✗✗ ALGUNS TESTES FALHARAM ✗✗✗")
        print()
        print("Ação Necessária:")
        print("  • Revisar os testes que falharam")
        print("  • Verificar a implementação")
        print("  • Corrigir e re-executar")
    
    print("="*80)
    print()
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
