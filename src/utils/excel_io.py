import pandas as pd
from typing import List, Tuple, Optional


def read_questions(file_path: str) -> Optional[List[Tuple[int, str, str]]]:
    """
    Load an Excel file and extract a list of questions.
    Returns:
        A list of tuples (question_number, model_question, source_text) or None on failure.
    """
    try:
        df = pd.read_excel(file_path)

        # Columns that must be present for the function to work
        required = ["№", "Вопрос для модели", "Текст из источника"]
        if not all(col in df.columns for col in required):
            print(f"[ERROR] Требуемые колонки: {required}")
            return None
        
        # Iterate over rows, building the result list
        # - Convert the "№" column to int
        # - Strip whitespace from string columns
        # - Replace NaN in "Текст из источника" with an empty string
        # - Skip rows where the key fields are missing
        return [
            (
                int(row["№"]),                                   # question number as int
                str(row["Вопрос для модели"]).strip(),          # model question, trimmed
                str(row["Текст из источника"]).strip()
                if pd.notna(row["Текст из источника"]) else "" # source text or empty string
            )
            for _, row in df.iterrows()
            if pd.notna(row["№"]) and pd.notna(row["Вопрос для модели"])
        ]
    except Exception as e:
        # Catch any unexpected errors (e.g., file not found, parsing issues)
        print(f"[ERROR] {e}")
        return None


def save_answers(results: List[Tuple[int, str, str]], output_path: str) -> bool:
    """
    Save a list of answer tuples to an Excel file.
    Args:
        results: A list of tuples where each tuple contains:
            - int: question number (№)
            - str: question text (Вопрос)
            - str: answer text (Ответ)
        output_path: Destination file path for the Excel workbook.

    Returns:
        bool: True if the file was written successfully, False otherwise.
    """
    try:
        df = pd.DataFrame(results, columns=["№", "Вопрос", "Ответ"])
        df.to_excel(output_path, index=False)
        print(f"[INFO] Сохранено: {output_path}")
        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        return False