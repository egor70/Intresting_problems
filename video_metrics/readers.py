"""
Модуль для чтения CSV файлов с данными о видео.
"""

import csv
from typing import List, Dict, Any


def read_csv_files(file_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Читает один или несколько CSV файлов и объединяет данные.

    Args:
        file_paths: Список путей к CSV файлам

    Returns:
        Список словарей с данными из всех файлов

    Raises:
        FileNotFoundError: Если файл не найден
        ValueError: Если файл имеет неправильный формат
    """
    all_rows = []
    required_columns = {'title', 'ctr', 'retention_rate'}

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)

                # Проверка наличия обязательных колонок
                if reader.fieldnames:
                    missing_columns = required_columns - set(reader.fieldnames)
                    if missing_columns:
                        raise ValueError(
                            f"Файл {file_path} не содержит обязательные колонки: "
                            f"{', '.join(missing_columns)}"
                        )

                # Чтение строк
                for row_num, row in enumerate(reader, start=2):
                    # Пропускаем пустые строки
                    if not any(row.values()):
                        continue
                    all_rows.append(row)

        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        except csv.Error as e:
            raise ValueError(f"Ошибка при чтении CSV файла {file_path}: {e}")

    return all_rows


def validate_row(row: Dict[str, Any]) -> bool:
    """
    Проверяет, содержит ли строка валидные данные.

    Args:
        row: Словарь с данными строки

    Returns:
        True если данные валидны, иначе False
    """
    try:
        float(row.get('ctr', ''))
        float(row.get('retention_rate', ''))
        return bool(row.get('title', '').strip())
    except (ValueError, TypeError):
        return False