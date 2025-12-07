# src/core/llm_client.py

import requests
from typing import Optional


def call_ollama(
    prompt: str,
    model: str = "qwen3:0.6b",
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    timeout: int = 60,
) -> Optional[str]:
    """
    Send a request to the locally hosted Ollama API to generate a completion.

    Parameters
    ----------
    prompt : str
        The user prompt to feed to the model.
    model : str, optional
        Model identifier, default is "qwen3:0.6b".
    temperature : float, optional
        Sampling temperature. If not provided, Ollama uses its default.
    top_p : float, optional
        Nucleus sampling parameter. If not provided, Ollama uses its default.
    timeout : int, optional
        Request timeout in seconds, default is 60.

    Returns
    -------
    Optional[str]
        The generated response text, or None if an error occurs.
    """
    url = "http://localhost:11434/api/generate"
    
    # Формируем payload
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    # Добавляем параметры модели только если они заданы
    if temperature is not None or top_p is not None:
        payload["options"] = {}
        if temperature is not None:
            payload["options"]["temperature"] = temperature
        if top_p is not None:
            payload["options"]["top_p"] = top_p

    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"[ERROR] Ollama: {e}")
        return None