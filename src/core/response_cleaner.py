import re

def clean_model_response(text: str) -> str:
    """
    Delete <think>...</think> blocks and whitespaces
    """
    if not text:
        return ""
    cleaned = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
    return "\n".join(lines).strip()