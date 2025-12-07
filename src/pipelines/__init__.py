from .baseline import build_prompt as baseline_prompt

# Словарь доступных пайплайнов
PIPELINES = {
    "baseline": baseline_prompt,
    # При необходимости можно добавить другие пайплайны, например "rag": rag_prompt
}