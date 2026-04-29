import pytest
import tempfile
import os
from readers import read_csv_files, validate_row


class TestReaders:
    """Тесты для модуля readers.py"""

    def test_read_single_csv(self):
        """Тест чтения одного CSV файла"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("title,ctr,retention_rate,views\n")
            f.write("Video1,20.5,35,1000\n")
            f.write("Video2,10.0,80,500\n")
            temp_file = f.name

        try:
            data = read_csv_files([temp_file])
            assert len(data) == 2
            assert data[0]['title'] == 'Video1'
            assert data[0]['ctr'] == '20.5'
            assert data[1]['retention_rate'] == '80'
        finally:
            os.unlink(temp_file)

    def test_read_multiple_csvs(self):
        """Тест чтения нескольких CSV файлов"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f1:
            f1.write("title,ctr,retention_rate\n")
            f1.write("Video1,20,30\n")
            temp_file1 = f1.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f2:
            f2.write("title,ctr,retention_rate\n")
            f2.write("Video2,25,35\n")
            temp_file2 = f2.name

        try:
            data = read_csv_files([temp_file1, temp_file2])
            assert len(data) == 2
            assert data[0]['title'] == 'Video1'
            assert data[1]['title'] == 'Video2'
        finally:
            os.unlink(temp_file1)
            os.unlink(temp_file2)

    def test_file_not_found(self):
        """Тест обработки несуществующего файла"""
        with pytest.raises(FileNotFoundError, match="Файл не найден"):
            read_csv_files(['nonexistent.csv'])

    def test_missing_required_columns(self):
        """Тест отсутствия обязательных колонок"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("title,views,likes\n")
            f.write("Video1,1000,100\n")
            temp_file = f.name

        try:
            with pytest.raises(ValueError, match="не содержит обязательные колонки"):
                read_csv_files([temp_file])
        finally:
            os.unlink(temp_file)

    def test_validate_row_valid(self):
        """Тест валидации корректной строки"""
        row = {'title': 'Test Video', 'ctr': '20.5', 'retention_rate': '45.0'}
        assert validate_row(row) is True

    def test_validate_row_invalid(self):
        """Тест валидации некорректной строки"""
        row = {'title': '', 'ctr': 'invalid', 'retention_rate': '45'}
        assert validate_row(row) is False