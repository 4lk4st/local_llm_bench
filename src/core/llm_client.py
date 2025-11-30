import requests
from typing import Optional


def call_ollama(
    prompt: str,
    model: str = "qwen3:0.6b",
    system_prompt: str = "",
    temperature: float = 0.7,
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
    system_prompt : str, optional
        Optional system prompt to guide the model's behavior.
    temperature : float, optional
        Sampling temperature, default is 0.7.
    timeout : int, optional
        Request timeout in seconds, default is 60.

    Returns
    -------
    Optional[str]
        The generated response text, or None if an error occurs.
    """
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature},
    }
    if system_prompt.strip():
        payload["system"] = system_prompt
        
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"[ERROR] Ollama: {e}")
        return None
