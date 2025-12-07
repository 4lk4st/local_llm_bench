# src/pipelines/simple_rag.py

def build_prompt(question: str, context: str = "", config=None, **kwargs) -> str:
    """
    Возвращает промт, содержащий контекст и вопрос пользователя.
    При наличии `config.prompt_template` используется шаблон из конфигурации,
    в противном случае – простой фиксированный формат.

    Parameters
    ----------
    question: str
        Текст вопроса.
    context: str, optional
        Текст из источника, который будет включён в промт.
    config: ExperimentConfig | None
        Позволяет задать пользовательский шаблон, например:
        "Ответь, используя следующий контекст:\n{context}\nВопрос: {question}"

    Returns
    -------
    str
        Сформированный промт.
    """
    # Если пользователь задал собственный шаблон – применим его.
    if config and getattr(config, "prompt_template", None):
        return config.prompt_template.format(question=question, context=context)

    # Иначе – используем стандартный фиксированный вариант.
    return f"Текст, в котором есть ответ на вопрос:\n{context}\nВопрос:\n{question}"