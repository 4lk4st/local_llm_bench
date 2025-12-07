import os
import re
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

# Загружаем переменные окружения из .env
load_dotenv()

# Константы для оценки
BOTHUB_API_KEY = os.getenv("BOTHUB_API_KEY")
BOTHUB_BASE_URL = "https://bothub.chat/api/v2/openai/v1"
BOTHUB_MODEL = "qwen3-max"

EVALUATION_PROMPT_TEMPLATE = (
    "Сравни два текста по смысловой близости."
    "Первый — ответ модели: «{model_response}»."
    "Второй — эталонный ответ: «{ground_truth}»."
    "Оцени схожесть по шкале от 1 до 100, где 100 — полное совпадение по смыслу."
    "Верни только целое число."
)

# Глобальный клиент (инициализируется один раз при первом вызове)
_client = None

def _get_client() -> OpenAI:
    global _client
    if _client is None:
        if not BOTHUB_API_KEY:
            raise ValueError("BOTHUB_API_KEY не найден в .env файле.")
        _client = OpenAI(api_key=BOTHUB_API_KEY, base_url=BOTHUB_BASE_URL)
    return _client

def evaluate_response_quality(model_response: str, ground_truth: str) -> Optional[int]:
    """
    Оценивает качество ответа модели по сравнению с эталонным.
    
    Возвращает целое число от 1 до 100 или None в случае ошибки.
    """
    if not BOTHUB_API_KEY:
        # Если ключ не задан, просто пропускаем оценку
        return None

    try:
        prompt = EVALUATION_PROMPT_TEMPLATE.format(
            model_response=model_response.strip(),
            ground_truth=ground_truth.strip()
        )

        client = _get_client()
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=BOTHUB_MODEL,
        )

        if not chat_completion.choices:
            return None

        response_text = chat_completion.choices[0].message.content
        if response_text is None:
            return None

        # Извлекаем первое целое число из ответа
        match = re.search(r'\b(\d{1,3})\b', response_text)
        if match:
            score = int(match.group(1))
            return max(1, min(100, score))  # Ограничиваем диапазон 1-100
        return None

    except Exception as e:
        print(f"⚠️ Ошибка при оценке качества: {e}")
        return None