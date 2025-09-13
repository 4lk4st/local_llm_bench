"""
Модуль для работы с Excel-файлами: чтение вопросов и запись ответов.
"""

import pandas as pd
from typing import List, Tuple, Optional
from openpyxl import load_workbook
from openpyxl.styles import Font
from constants import INPUT_EXCEL_FILENAME, OUTPUT_EXCEL_FILENAME

def read_questions_from_excel(file_path: str = INPUT_EXCEL_FILENAME) -> Optional[List[Tuple[int, str]]]:
    """
    Читает вопросы из Excel-файла.

    Аргументы:
        file_path (str): Путь к файлу с вопросами.

    Возвращает:
        Optional[List[Tuple[int, str]]]: Список кортежей (номер, вопрос) или None при ошибке.

    Пример:
        >>> read_questions_from_excel("questions.xlsx")
        [(1, "Почему небо голубое?"), (2, "Как работает фотосинтез?")]
    """
    try:
        df = pd.read_excel(file_path)
        if "№" not in df.columns or "Вопрос для модели" not in df.columns:
            print(f"[ERROR] В файле {file_path} отсутствуют обязательные колонки: '№', 'Вопрос для модели'")
            return None

        # Преобразуем в список кортежей, игнорируя NaN
        questions = [
            (int(row["№"]), str(row["Вопрос для модели"]).strip())
            for _, row in df.iterrows()
            if pd.notna(row["№"]) and pd.notna(row["Вопрос для модели"])
        ]
        return questions

    except Exception as e:
        print(f"[ERROR] Ошибка при чтении файла {file_path}: {e}")
        return None


def write_answers_to_excel(
    data: List[Tuple[int, str, str]],
    output_file: str = OUTPUT_EXCEL_FILENAME
) -> bool:
    """
    Записывает ответы модели в Excel-файл и форматирует его.

    Аргументы:
        data (List[Tuple[int, str, str]]): Список кортежей (номер, вопрос, ответ).
        output_file (str): Имя выходного файла.

    Возвращает:
        bool: True при успешной записи, False в случае ошибки.

    Пример:
        >>> write_answers_to_excel([(1, "Почему небо голубое?", "Из-за рассеяния...")])
        True
    """
    try:
        # Создаем DataFrame
        df = pd.DataFrame(data, columns=["№", "Вопрос, заданный модели", "Ответ модели"])

        # Записываем в Excel
        df.to_excel(output_file, index=False, engine="openpyxl")

        # Форматируем файл: ширина колонок и жирный заголовок
        workbook = load_workbook(output_file)
        worksheet = workbook.active

        # Жирный шрифт для заголовков
        bold_font = Font(bold=True)
        for cell in worksheet[1]:
            cell.font = bold_font

        # Автоподбор ширины колонок
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 100)  # ограничение ширины
            worksheet.column_dimensions[column_letter].width = adjusted_width

        workbook.save(output_file)
        print(f"[INFO] Ответы успешно записаны в {output_file}")
        return True

    except Exception as e:
        print(f"[ERROR] Ошибка при записи в файл {output_file}: {e}")
        return False