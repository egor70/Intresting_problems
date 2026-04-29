import pytest
from reports import clickbait_report, get_report, REPORTS_REGISTRY


class TestReports:
    """Тесты для модуля reports.py"""

    def test_clickbait_filtering(self):
        """Тест фильтрации кликбейтных видео"""
        data = [
            {'title': 'Video A', 'ctr': '25.0', 'retention_rate': '22'},
            {'title': 'Video B', 'ctr': '10.0', 'retention_rate': '80'},
            {'title': 'Video C', 'ctr': '18.5', 'retention_rate': '35'},
            {'title': 'Video D', 'ctr': '16.0', 'retention_rate': '45'},  # retention太高
            {'title': 'Video E', 'ctr': '15.0', 'retention_rate': '38'},  # ctr = 15 (не подходит)
            {'title': 'Video F', 'ctr': '20.0', 'retention_rate': '39'},
        ]

        result = clickbait_report(data)
        titles = [row['title'] for row in result]

        assert 'Video A' in titles
        assert 'Video C' in titles
        assert 'Video F' in titles
        assert 'Video B' not in titles
        assert 'Video D' not in titles
        assert 'Video E' not in titles

    def test_clickbait_sorting(self):
        """Тест сортировки по убыванию CTR"""
        data = [
            {'title': 'Video A', 'ctr': '30.0', 'retention_rate': '20'},
            {'title': 'Video B', 'ctr': '20.0', 'retention_rate': '25'},
            {'title': 'Video C', 'ctr': '25.0', 'retention_rate': '30'},
        ]

        result = clickbait_report(data)

        assert len(result) == 3
        assert result[0]['ctr'] == 30.0
        assert result[1]['ctr'] == 25.0
        assert result[2]['ctr'] == 20.0

    def test_clickbait_empty_result(self):
        """Тест когда нет подходящих видео"""
        data = [
            {'title': 'Video A', 'ctr': '10.0', 'retention_rate': '80'},
            {'title': 'Video B', 'ctr': '20.0', 'retention_rate': '50'},
        ]

        result = clickbait_report(data)
        assert result == []

    def test_clickbait_invalid_data(self):
        """Тест обработки некорректных данных"""
        data = [
            {'title': 'Valid', 'ctr': '20.0', 'retention_rate': '30'},
            {'title': 'Bad CTR', 'ctr': 'not_number', 'retention_rate': '30'},
            {'title': 'Bad Retention', 'ctr': '20.0', 'retention_rate': 'invalid'},
            {'title': '', 'ctr': '20.0', 'retention_rate': '30'},  # пустой заголовок
        ]

        result = clickbait_report(data)
        assert len(result) == 1
        assert result[0]['title'] == 'Valid'

    def test_get_report_exists(self):
        """Тест получения существующего отчёта"""
        func = get_report('clickbait')
        assert callable(func)

    def test_get_report_not_exists(self):
        """Тест получения несуществующего отчёта"""
        with pytest.raises(ValueError, match="Неизвестный отчёт"):
            get_report('unknown_report')

    def test_registry_contains_clickbait(self):
        """Тест что clickbait зарегистрирован"""
        assert 'clickbait' in REPORTS_REGISTRY
        assert callable(REPORTS_REGISTRY['clickbait'])