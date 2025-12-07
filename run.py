import argparse
import yaml
import shutil
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).parent / "src"))

from utils.excel_io import read_questions, save_answers
from core.llm_client import call_ollama
from core.response_cleaner import clean_model_response
from pipelines import PIPELINES
from utils.quality_evaluator import evaluate_response_quality
from utils.types import ExperimentConfig
from typing import get_type_hints


def load_config(config_path: str) -> ExperimentConfig:
    """
    Загружает конфигурационный файл в формате YAML.

    Параметры:
        config_path: Путь к файлу конфигурации YAML.

    Возвращает:
        Словарь с данными конфигурации, соответствующий типу ExperimentConfig.

    Исключения:
        FileNotFoundError: Если указанный файл не найден.
        yaml.YAMLError: Если файл нельзя корректно распарсить как YAML.
        ValueError: Если не хватает обязательных ключей.
    """
    config_file = Path(config_path)
    if not config_file.is_file():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    try:
        with config_file.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}
    except yaml.YAMLError as exc:
        raise yaml.YAMLError(f"Error parsing YAML config: {exc}") from exc

    if not isinstance(config, dict):
        raise ValueError("Config file must contain a YAML mapping (dictionary) at the top level.")

    return config


def ensure_output_dir(output_dir: str, config_path: str):
    """Создаёт выходную директорию и копирует файл конфигурации для воспроизводимости."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    shutil.copy2(config_path, f"{output_dir}/config.yaml")


def main() -> None:
    """Запускает пайплайн, который задан в файле конфигурации."""
    # Считываем путь до файла конфигурации
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to the YAML config")
    args = parser.parse_args()
    
    # Загружаем файл конфигурации и создаём выходную директорию
    config = load_config(args.config)
    ensure_output_dir(config["output_dir"], args.config)
    
    # Загружаем вопросы
    questions = read_questions(config["input_path"])
    if not questions:
        return
    
    # Загружаем pipeline
    prompt_builder = PIPELINES[config["pipeline"]]
    
    # Считываем параметры для llm из файла конфигурации
    llm_params = config.get("parameters") or {}

    results = []
    for q_id, question, context, ground_truth in questions:
        # Формируем промт
        prompt = prompt_builder(
            question=question,
            context=context,
            config=config,
        )
        
        # Вызываем модель через ollama
        raw_response = call_ollama(
            prompt=prompt,
            model=config["model"],
            temperature=llm_params.get("temperature"),  # может быть None → игнорируется
            top_p=llm_params.get("top_p"),              # может быть None → игнорируется
        ) or "[NO_RESPONSE]"

        response = clean_model_response(raw_response)
        quality_score = evaluate_response_quality(response, ground_truth)
        
        
        results.append((q_id, question, prompt, raw_response, response, quality_score))
        print(f"[{q_id}] {question[:50]}... → {response[:60]}...")
    
    # Сохраняем ответ в excel-файл
    output_file = f"{config['output_dir']}/answers.xlsx"
    save_answers(results, output_file)

    # Выводим краткую информацию о метрике качества эксперимента
    valid_scores = [score for score in [r[5] for r in results] if score is not None]
    if valid_scores:
        avg_score = sum(valid_scores) / len(valid_scores)
        print(f"\n✅ Средний балл качества ответов: {avg_score:.1f}")


if __name__ == "__main__":
    main()

