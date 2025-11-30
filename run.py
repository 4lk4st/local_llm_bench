import os
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


def load_config(config_path: str) -> dict:
    """
    Load a YAML configuration file.

    Args:
        config_path: Path to the YAML config file.

    Returns:
        A dictionary with the configuration data.

    Raises:
        FileNotFoundError: If the config file does not exist.
        yaml.YAMLError: If the file cannot be parsed as valid YAML.
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
    """Create the output directory and copy the config file for reproducibility."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    shutil.copy2(config_path, f"{output_dir}/config.yaml")


def main():
    """Run the QA pipeline using the provided configuration."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to the YAML config")
    args = parser.parse_args()
    
    config = load_config(args.config)
    ensure_output_dir(config["output_dir"], args.config)
    
    # Read questions from the input file
    questions = read_questions(config["input_file"])
    if not questions:
        return
    
    # Choose the appropriate prompt‑building pipeline
    prompt_builder = PIPELINES[config["pipeline"]]
    
    results = []
    for q_id, question, context in questions:
        # Build the prompt (baseline pipeline ignores the context)
        prompt = prompt_builder(
            question=question,
            context=context if config["use_context"] else "",
            config=config
        )
        
        # Call the model via Ollama
        raw_response = call_ollama(
            prompt=prompt,
            model=config["model"],
            system_prompt=config["system_prompt"],
            temperature=config["temperature"]
        ) or "[NO_RESPONSE]"

        response = clean_model_response(raw_response)
        
        results.append((q_id, question, response))
        print(f"[{q_id}] {question[:50]}... → {response[:60]}...")
    
    # Save the answers to an Excel file
    output_file = f"{config['output_dir']}/answers.xlsx"
    save_answers(results, output_file)


if __name__ == "__main__":
    main()