"""
Модуль для взаимодействия с локальной LLM через Ollama API.
"""

import requests
import json
import re
from typing import Optional, Dict, Any
from constants import OLLAMA_API_URL, DEFAULT_MODEL_NAME


def clean_model_response(text: str) -> str:
    """
    Очищает ответ модели от служебных блоков, например <think>...</think>.

    Аргументы:
        text (str): Сырой ответ модели.

    Возвращает:
        str: Очищенный текст без <think>-блоков и лишних пробелов.

    Пример:
        >>> clean_model_response("Привет! <think>Думаю...</think> Как дела?")
        "Привет! Как дела?"
    """
    # Удаляем все вхождения <think>...</think> (регистронезависимо, с переносами строк)
    pattern = r"<think>.*?</think>"
    cleaned = re.sub(pattern, "", text, flags=re.DOTALL | re.IGNORECASE)

    # Удаляем лишние пробелы и пустые строки
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    return "\n".join(lines).strip()

def generate_response(
    prompt: str,
    model: str = DEFAULT_MODEL_NAME,
    system_prompt: str = "",
    timeout: int = 60
) -> Optional[str]:
    """
    Отправляет запрос к модели Ollama и возвращает текст ответа.

    Аргументы:
        prompt (str): Текстовый запрос для модели.
        model (str): Название модели (по умолчанию "qwen3:0.6b").
        system_prompt (str): Системный промпт (заготовка, пока не используется).
        timeout (int): Таймаут запроса в секундах.

    Возвращает:
        Optional[str]: Текст ответа модели или None в случае ошибки.

    Пример:
        >>> generate_response("Почему небо голубое?")
        "Небо кажется голубым из-за рассеяния Рэлея..."
    """
    try:
        payload: Dict[str, Any] = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        # Заготовка под системный промпт (в будущем можно добавить "system": system_prompt)
        if system_prompt.strip():
            payload["system"] = system_prompt

        response = requests.post(OLLAMA_API_URL, json=payload, timeout=timeout)
        response.raise_for_status()

        result: Dict[str, Any] = response.json()
        raw_response = result.get("response", "").strip()

        # Очищаем ответ от <think>-блоков
        cleaned_response = clean_model_response(raw_response)

        return cleaned_response

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Ошибка при запросе к модели: {e}")
        return None
    except (KeyError, json.JSONDecodeError) as e:
        print(f"[ERROR] Ошибка обработки ответа модели: {e}")
        return None