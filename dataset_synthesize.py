import json
import re
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage
from tenacity import retry, stop_after_attempt, wait_exponential
from tqdm import tqdm

from prompt_templates import (
    finance_template,
    finance_template_cn,
    instruction_template,
    instruction_template_cn,
    knowledge_template,
    knowledge_template_cn,
    market_insight_cn,
    math_template,
    math_template_cn,
    npc_template,
    npc_template_cn,
    risk_assessment_cn,
    stock_analysis_cn,
    stock_knowledge_cn,
    trading_strategy_cn,
    universal_gen_v2_cn,
)


TEMPLATES = {
    "instruction": instruction_template,
    "knowledge": knowledge_template,
    "npc": npc_template,
    "math": math_template,
    "finance": finance_template,
    "instruction_cn": instruction_template_cn,
    "knowledge_cn": knowledge_template_cn,
    "npc_cn": npc_template_cn,
    "math_cn": math_template_cn,
    "finance_cn": finance_template_cn,
    "stock_analysis_cn": stock_analysis_cn,
    "trading_strategy_cn": trading_strategy_cn,
    "stock_knowledge_cn": stock_knowledge_cn,
    "risk_assessment_cn": risk_assessment_cn,
    "market_insight_cn": market_insight_cn,
    "universal_gen_v2_cn": universal_gen_v2_cn,
}


def super_clean(text):
    if not text:
        return ""

    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"```[a-zA-Z]*\n?", "", text)
    text = text.replace("```", "")
    return text.strip()


@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_response(client, user_prompt, system_prompt):
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]
    completion = client.invoke(messages)
    return completion.content.strip()


def translate_to_chinese(client, text: str) -> str:
    """Translate English text to Simplified Chinese when needed."""

    def has_chinese(value):
        return re.search(r"[\u4e00-\u9fff]", value)

    if has_chinese(text):
        return text.strip()

    messages = [
        SystemMessage(
            content=(
                "You are a professional translator specializing in translating "
                "English text to fluent Simplified Chinese."
            )
        ),
        HumanMessage(
            content=(
                "Translate the following text to Simplified Chinese, preserving "
                "meaning and style. Do not add extra commentary:\n\n"
                f"{text}"
            )
        ),
    ]
    completion = client.invoke(messages)
    return completion.content.strip()


def contains_chinese(text):
    return re.search(r"[\u4e00-\u9fff]", text) is not None


def clean_synthesized_content(text):
    """
    Normalize model output by removing hidden reasoning blocks, markdown fences,
    duplicate punctuation, and common assistant prefixes.
    """
    if not text:
        return ""

    text = super_clean(text)
    text = re.sub(r"[\.\,\;\!\?]{2,}", ".", text)
    text = "".join(ch for ch in text if ch.isprintable() or ch in ["\n", "\r", "\t"])
    text = text.strip()

    patterns_to_remove = [
        r"^Sure[,\s]+",
        r"^Here is .*?:",
        r"^Based on your request[,\s]+.*?:",
        r"^As .*?,\s*",
    ]
    for pattern in patterns_to_remove:
        text = re.sub(pattern, "", text, flags=re.MULTILINE | re.IGNORECASE)

    text = text.replace("..", ".").replace(",,", ",")
    return text.strip()


def clean_persona_field(text):
    """
    Normalize persona text so template formatting stays stable.
    """
    if not text:
        return "."
    return text.strip().rstrip(".").rstrip(",").rstrip(";") + "."


def select_template(template_name_or_text):
    if template_name_or_text in TEMPLATES:
        return TEMPLATES[template_name_or_text]

    if template_name_or_text is not None and len(str(template_name_or_text).strip()) > 0:
        return template_name_or_text

    raise ValueError(
        "Invalid template type. Choose a known template name or provide a custom template string."
    )


def main(client, args, persona_dataset, system_prompt):
    template = select_template(args.template)

    if args.sample_size > 0:
        persona_dataset = persona_dataset[: args.sample_size]

    output_path = Path(args.output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    persona_cache = {}
    with open(output_path, "a", encoding="utf-8") as out:
        for item in tqdm(persona_dataset, desc="Generating data"):
            persona = item["input persona"].strip()

            if contains_chinese(template):
                if persona not in persona_cache:
                    persona_cache[persona] = translate_to_chinese(client, persona)
                persona = persona_cache[persona]

            cleaned_persona = clean_persona_field(persona)
            question_generation_prompt = template.format(persona=cleaned_persona)

            raw_question = get_response(
                client,
                question_generation_prompt,
                system_prompt,
            )
            extracted_question = clean_synthesized_content(raw_question)

            answer_system_prompt = (
                "Answer the following question with professional depth, rigorous "
                "reasoning, and expertise that fits the persona context."
            )
            raw_answer = get_response(client, extracted_question, answer_system_prompt)
            cleaned_answer = clean_synthesized_content(raw_answer)

            output_record = {
                "prompt": extracted_question,
                "response": cleaned_answer,
            }
            out.write(json.dumps(output_record, ensure_ascii=False) + "\n")


def main_all(client, template, sample_size, output_path, persona_dataset, system_prompt):
    """
    Adapter used by GeneratorAgent to call the synthesis flow without CLI parsing.
    """

    class Args:
        def __init__(self, template, sample_size, output_path):
            self.template = template
            self.sample_size = sample_size
            self.output_path = output_path

    args = Args(template, sample_size, output_path)
    main(client, args, persona_dataset, system_prompt)
