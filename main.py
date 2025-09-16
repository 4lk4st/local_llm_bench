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
    1. Чтение вопросов и контекстов из Excel.
    2. Для каждого вопроса — запрос к модели с использованием контекста (RAG-имитация).
    3. Сохранение только вопросов и ответов в новый Excel-файл (контекст НЕ сохраняется).
    """
    print("[INFO] Начинаем обработку вопросов...")

    # Шаг 1: Чтение вопросов и контекстов
    questions_with_context = read_questions_from_excel()
    if not questions_with_context:
        print("[ERROR] Не удалось прочитать вопросы. Завершение работы.")
        return

    print(f"[INFO] Прочитано {len(questions_with_context)} вопросов с контекстами.")

    # Шаг 2: Получение ответов — используем контекст для генерации, но не сохраняем его в результат
    results: List[Tuple[int, str, str]] = []  # №, вопрос, ответ (контекст не сохраняем)
    for i, (q_num, question, context) in enumerate(questions_with_context, start=1):
        print(f"[INFO] Обработка вопроса {i}/{len(questions_with_context)}: {question[:50]}...")
        answer = generate_response(question=question, context=context)
        if answer is None:
            answer = "[ОШИБКА: модель не ответила]"
        results.append((q_num, question, answer))  # Только номер, вопрос, ответ

    # Шаг 3: Запись в Excel — как в оригинале, 3 колонки
    success = write_answers_to_excel(results, OUTPUT_EXCEL_FILENAME)
    if success:
        print("[SUCCESS] Все ответы успешно сохранены!")
    else:
        print("[ERROR] Не удалось сохранить ответы в файл.")


if __name__ == "__main__":
    main()