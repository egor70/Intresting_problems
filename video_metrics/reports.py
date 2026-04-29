"""
Модуль для генерации отчётов.
"""

from typing import List, Dict, Any, Callable
from tabulate import tabulate


def clickbait_report(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Отчёт о кликбейтных видео.

    Условия:
        - CTR > 15%
        - Удержание (retention_rate) < 40%

    Сортировка: по убыванию CTR.

    Args:
        data: Список словарей с данными видео

    Returns:
        Отфильтрованный и отсортированный список
    """
    filtered = []

    for row in data:
        try:
            ctr = float(row.get('ctr', 0))
            retention = float(row.get('retention_rate', 0))
            title = row.get('title', '').strip()

            if title and ctr > 15 and retention < 40:
                # Создаём копию с числовыми значениями для сортировки
                filtered.append({
                    'title': title,
                    'ctr': ctr,
                    'retention_rate': retention
                })
        except (ValueError, TypeError):
            # Пропускаем некорректные строки
            continue

    # Сортировка по убыванию CTR
    filtered.sort(key=lambda x: x['ctr'], reverse=True)

    return filtered


# Реестр доступных отчётов
# Для добавления нового отчёта нужно:
# 1. Создать функцию с сигнатурой (data) -> filtered_data
# 2. Добавить её в этот словарь с уникальным ключом
REPORTS_REGISTRY: Dict[str, Callable] = {
    'clickbait': clickbait_report,
    # 'trending': trending_report,  # пример добавления нового отчёта
    # 'viral': viral_report,        # пример добавления нового отчёта
}


def get_report(report_name: str) -> Callable:
    """
    Возвращает функцию-обработчик для указанного отчёта.

    Args:
        report_name: Название отчёта

    Returns:
        Функция обработки отчёта

    Raises:
        ValueError: Если отчёт с таким именем не зарегистрирован
    """
    if report_name not in REPORTS_REGISTRY:
        available_reports = ', '.join(REPORTS_REGISTRY.keys())
        raise ValueError(
            f"Неизвестный отчёт: '{report_name}'. "
            f"Доступные отчёты: {available_reports}"
        )
    return REPORTS_REGISTRY[report_name]


def print_report(report_name: str, data: List[Dict[str, Any]]) -> None:
    """
    Генерирует и выводит отчёт в консоль.

    Args:
        report_name: Название отчёта
        data: Сырые данные для анализа
    """
    report_func = get_report(report_name)
    filtered_data = report_func(data)

    if not filtered_data:
        print("Нет данных, соответствующих критериям отчёта.")
        return

    # Подготовка данных для tabulate
    table_data = [
        [row['title'], f"{row['ctr']:.1f}", f"{row['retention_rate']:.1f}"]
        for row in filtered_data
    ]

    headers = ['Название видео', 'CTR (%)', 'Удержание (%)']

    # Вывод таблицы
    print(tabulate(table_data, headers=headers, tablefmt='grid'))

    # Дополнительная статистика
    print(f"\nВсего найдено: {len(filtered_data)} видео")
    avg_ctr = sum(row['ctr'] for row in filtered_data) / len(filtered_data)
    print(f"Средний CTR: {avg_ctr:.1f}%")