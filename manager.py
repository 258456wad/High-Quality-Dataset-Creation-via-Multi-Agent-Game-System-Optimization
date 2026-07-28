import json
import os
from pathlib import Path

from datasets import load_dataset
from langchain_deepseek import ChatDeepSeek
from langchain_huggingface import HuggingFaceEmbeddings

from generator_agent import GeneratorAgent
from planner_agent import PlannerAgent
from Similarity_And_Selection_Agent import SimilarityAndSelectionAgent


CODE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = Path(os.environ.get("PROJECT_ROOT", CODE_DIR.parent)).resolve()


def resolve_project_path(env_name, default_relative_path):
    value = os.environ.get(env_name)
    if value:
        return Path(value).expanduser().resolve()
    return (PROJECT_ROOT / default_relative_path).resolve()


DATA_DIR = resolve_project_path("DATA_DIR", "data")
OUTPUT_DIR = resolve_project_path("OUTPUT_DIR", "output_data")
CACHE_DIR = resolve_project_path("HF_DATASETS_CACHE", "temp_cache")
BGE_MODEL_PATH = resolve_project_path("BGE_MODEL_PATH", "bge-large-zh-v1.5")


def require_env(env_name):
    value = os.environ.get(env_name)
    if not value:
        raise RuntimeError(f"Environment variable {env_name} is required.")
    return value


def ensure_parent_dir(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def ask_int(prompt, valid_values=None):
    value = int(input(prompt).strip())
    if valid_values is not None and value not in valid_values:
        raise ValueError(f"Expected one of {sorted(valid_values)}, got {value}.")
    return value


def prepare_output_file(path):
    ensure_parent_dir(path)
    with open(path, "w", encoding="utf-8") as f:
        f.truncate(0)


def build_chat_client():
    api_key = require_env("DEEPSEEK_API_KEY")
    api_base = (
        os.environ.get("DEEPSEEK_API_BASE")
        or os.environ.get("DEEPSEEK_API_BASE_URL")
        or "https://api.deepseek.com"
    )

    return ChatDeepSeek(
        model=os.environ.get("DEEPSEEK_MODEL", "deepseek-chat"),
        api_key=api_key,
        api_base=api_base,
        temperature=0.1,
        timeout=120,
    )


def build_embedding_client():
    print("--- Loading local BGE embedding model. ---")
    return HuggingFaceEmbeddings(
        model_name=str(BGE_MODEL_PATH),
        model_kwargs={
            "device": os.environ.get("EMBEDDING_DEVICE", "cuda"),
        },
        encode_kwargs={
            "normalize_embeddings": True,
            "batch_size": int(os.environ.get("EMBEDDING_BATCH_SIZE", "8")),
        },
    )


def load_personas(persona_dataset_path):
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    raw_data = load_dataset(
        "json",
        data_files=str(persona_dataset_path),
        cache_dir=str(CACHE_DIR),
    )["train"]

    persona_dataset = []
    for i, item in enumerate(raw_data):
        item["_original_idx"] = i
        persona_dataset.append(item)
    return persona_dataset


def run_similarity_filter(samples, select_output_path, similarity_agent):
    if not samples:
        print("Warning: no raw samples were generated. Skipping deduplication.")
        return []

    print(f"--- Starting similarity filtering for {len(samples)} samples. ---")
    final_cleaned_data = similarity_agent.process(samples)

    with open(select_output_path, "w", encoding="utf-8") as f:
        for item in final_cleaned_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"--- Filtering completed. Selected samples: {len(final_cleaned_data)}. ---")
    return final_cleaned_data


def main():
    user_input = input("Enter your dataset construction request: ")
    personal_filter_need = ask_int(
        "Use keyword-based persona pre-filtering? Enter 1 for yes, 0 for no: ",
        valid_values={0, 1},
    )

    personal_filter = None
    if personal_filter_need == 1:
        personal_filter = input("Enter the desired style or filtering keyword: ")
    else:
        print("--- Skipping pre-filtering and using the full persona pool. ---")

    feedback_needed = ask_int(
        "Use multi-round feedback generation? Enter 1 for yes, 0 for no: ",
        valid_values={0, 1},
    )

    system_prompt = (
        "You are a professional data synthesis expert. Simulate each persona's "
        "thinking style and generate logically deep, domain-specific, challenging "
        "instructions. Keep the output rigorous and avoid filler."
    )

    persona_dataset_path = DATA_DIR / os.environ.get("PERSONA_FILE", "persona.jsonl")
    persona_filter_path = DATA_DIR / os.environ.get(
        "PERSONA_FILTER_FILE",
        "persona_filter_2000.jsonl",
    )
    output_path = OUTPUT_DIR / os.environ.get(
        "RAW_OUTPUT_FILE",
        "manager_feedback_2000.jsonl",
    )
    select_output_path = OUTPUT_DIR / os.environ.get(
        "SELECTED_OUTPUT_FILE",
        "selected_manager_feedback_2000.jsonl",
    )

    prepare_output_file(output_path)
    prepare_output_file(select_output_path)

    persona_dataset = load_personas(persona_dataset_path)
    client = build_chat_client()

    planner = PlannerAgent(client, personal_filter, str(persona_filter_path))
    instruction_config, persona_filter_dataset = planner.plan(
        user_input,
        str(output_path),
        persona_dataset,
    )

    if feedback_needed == 1:
        gold_standard_pool = []
        agent = GeneratorAgent(client, persona_filter_dataset)
        embed_client = build_embedding_client()
        similarity_agent = SimilarityAndSelectionAgent(embed_client)
        round_index = 0

        while len(gold_standard_pool) < instruction_config["sample_size"]:
            round_index += 1
            remaining_personas = agent.now_pool

            if not remaining_personas:
                print(
                    "--- Notice: the filtered persona pool is exhausted, "
                    "so no more data can be generated. ---"
                )
                break

            needed_now = instruction_config["sample_size"] - len(gold_standard_pool)
            current_batch_size = min(needed_now, len(remaining_personas))

            print(
                "--- Feedback loop progress: "
                f"{len(gold_standard_pool)}/{instruction_config['sample_size']} | "
                f"round {round_index}, sampling {current_batch_size} personas. ---"
            )

            prepare_output_file(output_path)
            agent.execute_task(
                template=instruction_config["template"],
                sample_size=current_batch_size,
                output_path=str(output_path),
                system_prompt=system_prompt,
            )
            print(
                f"[Generator Agent] Round {round_index} completed. "
                f"Results saved to: {output_path}"
            )

            current_raw_samples = []
            if output_path.exists():
                with open(output_path, "r", encoding="utf-8") as f:
                    for line in f:
                        current_raw_samples.append(json.loads(line.strip()))

            if not current_raw_samples:
                print("Warning: no samples were generated in this round.")
                continue

            combined_for_filter = gold_standard_pool + current_raw_samples
            cleaned_data = similarity_agent.process(combined_for_filter)

            if cleaned_data is not None:
                gold_standard_pool = cleaned_data
                if gold_standard_pool:
                    with open(select_output_path, "w", encoding="utf-8") as f:
                        for item in gold_standard_pool:
                            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            else:
                print(
                    "Warning: the deduplication agent returned None. "
                    "Keeping the previous pool for the next retry."
                )

            print(
                f"--- After round {round_index}, the high-quality pool contains "
                f"{len(gold_standard_pool)} samples. ---"
            )

        print(
            f"--- Task finished. Final high-quality samples: "
            f"{len(gold_standard_pool)}. ---"
        )
        return 0

    agent = GeneratorAgent(client, persona_filter_dataset)
    print(f"--- Starting task with instruction config: {instruction_config} ---")
    output_path = Path(
        agent.execute_task(
            template=instruction_config["template"],
            sample_size=instruction_config["sample_size"],
            output_path=str(output_path),
            system_prompt=system_prompt,
        )
    )
    print(f"[Generator Agent] First round completed. Results saved to: {output_path}")

    embed_client = build_embedding_client()
    similarity_agent = SimilarityAndSelectionAgent(embed_client)

    raw_samples = []
    with open(output_path, "r", encoding="utf-8") as f:
        for line in f:
            raw_samples.append(json.loads(line.strip()))

    run_similarity_filter(raw_samples, select_output_path, similarity_agent)
    return 0


if __name__ == "__main__":
    main()
