#!/usr/bin/env python3
"""
CLI утилита для анализа метрик YouTube видео.
"""

import argparse
import sys
from readers import read_csv_files
from reports import get_report, print_report


def parse_arguments():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(
        description='Анализ метрик YouTube видео',
        epilog='Пример: python cli.py --files stats1.csv stats2.csv --report clickbait'
    )
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='Пути к CSV файлам с данными (можно указать несколько)'
    )
    parser.add_argument(
        '--report',
        required=True,
        help='Название отчёта (например: clickbait)'
    )

    return parser.parse_args()


def main():
    """Главная функция."""
    args = parse_arguments()

    try:
        # Чтение данных из файлов
        data = read_csv_files(args.files)

        if not data:
            print("Предупреждение: Нет данных для анализа")
            return 0

        # Генерация и вывод отчёта
        print_report(args.report, data)
        return 0

    except FileNotFoundError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())