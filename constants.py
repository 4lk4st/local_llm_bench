"""
Константы проекта — для удобного управления настройками.
"""

# Имя выходного файла с ответами модели
OUTPUT_EXCEL_FILENAME: str = "answers_v1.xlsx"

# Путь к входному файлу с вопросами
INPUT_EXCEL_FILENAME: str = "questions.xlsx"

# URL и параметры API Ollama
OLLAMA_API_URL: str = "http://localhost:11434/api/generate"
DEFAULT_MODEL_NAME: str = "qwen3:0.6b"
