"""
Константы проекта — для удобного управления настройками.
"""

# Имя выходного файла с ответами модели
OUTPUT_EXCEL_FILENAME: str = "answers_v3.xlsx"

# Имя входного файла с вопросами
INPUT_EXCEL_FILENAME: str = "questions.xlsx"

# Имя выходного файла с оценкой ответов модели
OUTPUT_EVALUATION_FILENAME: str = "results.xlsx"

# URL и параметры API Ollama
OLLAMA_API_URL: str = "http://localhost:11434/api/generate"
DEFAULT_MODEL_NAME: str = "qwen3:0.6b"
