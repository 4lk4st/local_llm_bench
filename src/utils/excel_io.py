import pandas as pd
from typing import List, Tuple, Optional


def read_questions(file_path: str) -> Optional[List[Tuple[int, str, str, str]]]:
    """
    Загружает Excel файл и извлекает список вопросов.
    Возвращает:
        Список кортежей (номер_вопроса, вопрос_для_модели, текст_из_источника, правильный_ответ)
        либо None в случае ошибки.
    """
    try:
        # Читаем файл с помощью pandas
        df = pd.read_excel(file_path)

        # Обязательные колонки, без которых функция не сможет работать
        required = ["№", "Вопрос для модели", "Текст из источника", "Правильный ответ"]
        if not all(col in df.columns for col in required):
            print(f"[ERROR] Требуемые колонки: {required}")
            return None

        # Проходим по строкам таблицы и формируем результат
        return [
            (
                int(row["№"]),                                  # номер вопроса как int
                str(row["Вопрос для модели"]).strip(),          # вопрос для модели, без пробелов
                str(row["Текст из источника"]).strip()
                if pd.notna(row["Текст из источника"]) else "", # текст из источника или пустая строка
                str(row["Правильный ответ"]).strip()
                if pd.notna(row["Правильный ответ"]) else ""    # правильный ответ или пустая строка
            )
            for _, row in df.iterrows()
            if pd.notna(row["№"]) and pd.notna(row["Вопрос для модели"])
        ]
    except Exception as e:
        # Любая непредвиденная ошибка (файл не найден, проблемы парсинга и т.п.)
        print(f"[ERROR] {e}")
        return None


def save_answers(
    results: List[Tuple[int, str, str, str, str, Optional[int]]],
    output_path: str,
) -> bool:
    """
    Сохраняет результаты эксперимента в Excel.

    Столбцы:
        - №               – номер вопроса
        - Вопрос          – исходный текст вопроса
        - Промт           – запрос, отправленный модели
        - Полный ответ    – ответ модели без очистки (может содержать рассуждения)
        - Итоговый ответ  – очищенный ответ (без рассуждений)
        - Оценка качества – числовая оценка от 1 до 100 (или пусто, если оценка не проводилась)

    Возвращает:
        True при успешной записи, False при ошибке.
    """
    try:
        df = pd.DataFrame(
            results,
            columns=["№", "Вопрос", "Промт", "Полный ответ", "Итоговый ответ", "Оценка качества"],
        )
        df.to_excel(output_path, index=False)
        print(f"[INFO] Сохранено: {output_path}")
        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        return False