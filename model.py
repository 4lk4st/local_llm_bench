"""
Модуль для взаимодействия с локальной LLM через Ollama API.
"""

import requests
import json
import re
from typing import Optional, Dict, Any
from constants import OLLAMA_API_URL, DEFAULT_MODEL_NAME


SYSTEM_PROMPT = """
### ТВОЯ РОЛЬ ###
Ты - профессиональный консультант по вопросам управления многоквартирными домами в Российской Федерации.
Ты хорошо знаешь жилищное законодательство и готов помочь людям ответить на любой их вопрос в этой области.

### КОНТЕКСТ ЗАДАЧИ ###
1. В настоящее время в Российской Федерации много новых людей пробуют себя в сфере управления многоквартирными
домами. И не все из них хорошо изучили Жилищный кодекс.
2. К тебе за консультацией обратился председатель товарищества собственников жилья (ТСЖ) многоквартирного дома с вопросом,
который будет указан ниже.

### ДОПОЛНИТЕЛЬНЫЙ КОНТЕКСТ ###
Ниже приведён релевантный фрагмент из нормативного документа или источника, который ты ОБЯЗАН использовать при подготовке ответа.
Если в контексте нет информации для ответа — сообщи об этом вежливо.

### ТВОЯ ЗАДАЧА ###
Дай чёткий, точный и полный ответ на вопрос, опираясь ТОЛЬКО на приведённый контекст. Не придумывай информацию.

### ПРАВИЛА ФОРМАТИРОВАНИЯ ОТВЕТА ###
1. Ответ только на русском языке.
2. В ответе нельзя использовать символы разметки markdown, такие как * и #.
"""

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
    question: str,
    context: str,
    model: str = DEFAULT_MODEL_NAME,
    system_prompt: str = SYSTEM_PROMPT,
    timeout: int = 60
) -> Optional[str]:
    """
    Отправляет запрос к модели Ollama и возвращает текст ответа, усиленный контекстом (RAG).

    Аргументы:
        question (str): Текстовый запрос для модели.
        context (str): Контекст из источника, на который должна опираться модель.
        model (str): Название модели (по умолчанию "qwen3:0.6b").
        system_prompt (str): Системный промпт.
        timeout (int): Таймаут запроса в секундах.

    Возвращает:
        Optional[str]: Текст ответа модели или None в случае ошибки.

    Пример:
        >>> generate_response("Можно ли проводить собрание онлайн?", "Согласно ЖК РФ ст. 47.1, собрание может проводиться дистанционно...")
        "Да, согласно статье 47.1 Жилищного кодекса РФ, собрание собственников может проводиться в дистанционной форме."
    """
    try:
        # Формируем полный промпт: контекст + вопрос
        full_prompt = f"""
            Контекст из источника:
            {context}

            Вопрос:
            {question}

            Пожалуйста, ответьте на вопрос, опираясь строго на приведённый контекст.
        """.strip()

        payload: Dict[str, Any] = {
            "model": model,
            "prompt": full_prompt,
            "stream": False
        }

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