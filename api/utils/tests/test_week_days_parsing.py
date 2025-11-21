"""
Testes para correção da Issue #248: Display incorreto da informação de data e hora
https://github.com/unb-mds/2023-2-SuaGradeUnB/issues/248

Problema: Ao exibir as informações de horário de uma matéria com múltiplas aulas,
apenas uma aula é exibida. O bug foi causado pelo regex que não lidava corretamente
com espaços múltiplos (comuns em HTML/web scraping).

Correção: Trocar \s por \s+ no regex para aceitar um ou mais espaços.
"""

from rest_framework.test import APITestCase
from utils.web_scraping import DisciplineWebScraper


class WeekDaysParsingTest(APITestCase):
    """
    Testes para verificar o parsing correto de dias da semana e horários.
    Baseado na Issue #248 sobre display incorreto de horários.
    """

    def setUp(self):
        """Configuração inicial para cada teste"""
        self.scraper = DisciplineWebScraper(
            department="650",
            year="2023",
            period="2",
            session=self.client,
            cookie=""
        )

    def test_parse_single_weekday_with_time(self):
        """
        Testa o parsing de um único dia da semana com horário.
        
        Caso base: uma única aula na semana.
        """
        data = "Terça-feira 14:00 às 15:50"
        result = self.scraper.get_week_days(data)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Terça-feira 14:00 às 15:50")

    def test_parse_multiple_weekdays_terca_quinta(self):
        """
        Testa o parsing de múltiplos dias da semana (Terça e Quinta).
        
        Este é o caso da Issue #248: Paradigmas de Programação do professor Edson Alves
        deveria ter 2 aulas (Terça e Quinta) mas apenas Terça estava sendo exibida.
        """
        data = "35T23 Terça-feira 14:00 às 15:50 Quinta-feira 14:00 às 15:50"
        result = self.scraper.get_week_days(data)
        
        # Deve encontrar DOIS dias da semana com horários
        self.assertEqual(len(result), 2, 
                        f"Esperava 2 dias, mas encontrou {len(result)}: {result}")
        self.assertIn("Terça-feira 14:00 às 15:50", result)
        self.assertIn("Quinta-feira 14:00 às 15:50", result)

    def test_parse_segunda_quarta_sexta(self):
        """
        Testa o parsing de três dias da semana (Segunda, Quarta e Sexta).
        
        Caso comum: disciplinas com aulas três vezes por semana.
        """
        data = "246M34 Segunda-feira 10:00 às 11:50 Quarta-feira 10:00 às 11:50 Sexta-feira 10:00 às 11:50"
        result = self.scraper.get_week_days(data)
        
        self.assertEqual(len(result), 3,
                        f"Esperava 3 dias, mas encontrou {len(result)}: {result}")
        self.assertIn("Segunda-feira 10:00 às 11:50", result)
        self.assertIn("Quarta-feira 10:00 às 11:50", result)
        self.assertIn("Sexta-feira 10:00 às 11:50", result)

    def test_parse_all_weekdays(self):
        """
        Testa o parsing de todos os dias da semana possíveis.
        """
        data = ("Segunda-feira 08:00 às 09:50 Terça-feira 08:00 às 09:50 "
                "Quarta-feira 08:00 às 09:50 Quinta-feira 08:00 às 09:50 "
                "Sexta-feira 08:00 às 09:50 Sábado 08:00 às 09:50")
        result = self.scraper.get_week_days(data)
        
        self.assertEqual(len(result), 6,
                        f"Esperava 6 dias, mas encontrou {len(result)}: {result}")

    def test_parse_with_schedule_codes(self):
        """
        Testa o parsing quando há códigos de horário misturados com os dias.
        
        Verifica que o regex não confunde códigos de horário (35T23) com dias da semana.
        """
        data = "35T23 Terça-feira 14:00 às 15:50 Quinta-feira 14:00 às 15:50"
        result = self.scraper.get_week_days(data)
        
        # Não deve incluir o código de horário "35T23" nos resultados
        for day in result:
            self.assertNotIn("35T23", day)
            self.assertIn(":", day)  # Deve conter horário
            self.assertIn("às", day)  # Deve conter "às"

    def test_parse_quinta_feira_specifically(self):
        """
        Testa especificamente "Quinta-feira" que era o dia faltante na Issue #248.
        
        O regex original tinha problema com dias começando com 'Qu'.
        """
        data = "Quinta-feira 14:00 às 15:50"
        result = self.scraper.get_week_days(data)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Quinta-feira 14:00 às 15:50")

    def test_parse_sabado(self):
        """
        Testa o parsing de "Sábado" (sem hífen).
        """
        data = "Sábado 08:00 às 09:50"
        result = self.scraper.get_week_days(data)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], "Sábado 08:00 às 09:50")

    def test_parse_with_double_spaces(self):
        """
        Testa o parsing quando há espaços duplos (Issue #248 - caso real).
        
        Em HTML/web scraping é comum ter espaços extras. O regex deve ser
        robusto para lidar com isso usando \s+ em vez de \s.
        """
        data = "Terça-feira  14:00 às 15:50"
        result = self.scraper.get_week_days(data)
        
        self.assertEqual(len(result), 1,
                        f"Esperava 1 dia com espaços duplos, mas encontrou {len(result)}: {result}")
        self.assertIn("Terça-feira", result[0])

    def test_parse_multiple_days_with_extra_spaces(self):
        """
        Testa múltiplos dias quando há espaços extras entre elementos.
        
        Este é o cenário real da Issue #248: dados do scraping podem ter
        espaçamento inconsistente.
        """
        data = "35T23  Terça-feira  14:00 às  15:50  Quinta-feira  14:00  às  15:50"
        result = self.scraper.get_week_days(data)
        
        self.assertEqual(len(result), 2,
                        f"Esperava 2 dias com espaços extras, mas encontrou {len(result)}: {result}")
        # Verificar que ambos os dias foram capturados
        self.assertTrue(any("Terça" in r for r in result))
        self.assertTrue(any("Quinta" in r for r in result))

    def test_parse_with_multiple_spaces_between_time_components(self):
        """
        Testa parsing com múltiplos espaços em diferentes partes do horário.
        """
        data = "Segunda-feira   10:00   às   11:50"
        result = self.scraper.get_week_days(data)
        
        self.assertEqual(len(result), 1,
                        f"Esperava 1 resultado, mas encontrou {len(result)}: {result}")
        self.assertIn("Segunda-feira", result[0])
