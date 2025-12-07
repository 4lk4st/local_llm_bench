from typing import TypedDict, Optional

class ExperimentConfig(TypedDict):
    """Строгая типизация для конфигурационного файла эксперимента."""
    name: str
    model: str
    pipeline: str
    input_path: str
    output_dir: str
    prompt_template: str
    # Необязательные поля
    parameters: Optional[dict]