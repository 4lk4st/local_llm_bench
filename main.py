"""
Основной модуль — точка входа в программу.
Читает вопросы, получает ответы от модели, сохраняет в Excel.
"""

from typing import List, Tuple
from model import generate_response
from excel_handler import read_questions_from_excel, write_answers_to_excel
from constants import OUTPUT_EXCEL_FILENAME

def main() -> None:
    """
    Основная функция программы.

    Шаги:
    1. Чтение вопросов из Excel.
    2. Для каждого вопроса — запрос к модели.
    3. Сохранение ответов в новый Excel-файл.
    """
    print("[INFO] Начинаем обработку вопросов...")

    # Шаг 1: Чтение вопросов
    questions = read_questions_from_excel()
    if not questions:
        print("[ERROR] Не удалось прочитать вопросы. Завершение работы.")
        return

    print(f"[INFO] Прочитано {len(questions)} вопросов.")

    # Шаг 2: Получение ответов
    results: List[Tuple[int, str, str]] = []
    for i, (q_num, question) in enumerate(questions, start=1):
        print(f"[INFO] Обработка вопроса {i}/{len(questions)}: {question[:50]}...")
        answer = generate_response(question)
        if answer is None:
            answer = "[ОШИБКА: модель не ответила]"
        results.append((q_num, question, answer))

    # Шаг 3: Запись в Excel
    success = write_answers_to_excel(results, OUTPUT_EXCEL_FILENAME)
    if success:
        print("[SUCCESS] Все ответы успешно сохранены!")
    else:
        print("[ERROR] Не удалось сохранить ответы в файл.")

if __name__ == "__main__":
    main()