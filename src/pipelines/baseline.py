from typing import Optional
from utils.types import ExperimentConfig


def build_prompt(
    question: str,
    context: str = "",
    config: Optional[ExperimentConfig] = None,
    **kwargs  # оставляем для совместимости с будущими пайплайнами
) -> str:
    """
    Формирует промт на основе шаблона из конфига.
    Если шаблон не задан или равен None — возвращает просто вопрос.
    
    Параметры:
        question: Текст вопроса.
        context: Дополнительный контекст (не используется в baseline, но поддерживается).
        config: Конфигурация эксперимента (опционально).
        **kwargs: Дополнительные аргументы (игнорируются).
        
    Возвращает:
        Сформированный промт для отправки в LLM.
    """
    if config and "prompt_template" in config:
        template = config["prompt_template"]
        if isinstance(template, str):  # Защита от null в YAML
            return template.format(question=question, context=context)
    return question
