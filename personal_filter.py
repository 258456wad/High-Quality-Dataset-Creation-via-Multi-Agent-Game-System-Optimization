import json
import re

from langchain_core.messages import HumanMessage, SystemMessage


def clean_translation_output(raw_response: str) -> str:
    if "<think" in raw_response.lower():
        cleaned = re.sub(
            r"<think.*?</think>",
            "",
            raw_response,
            flags=re.DOTALL | re.IGNORECASE,
        )
        return cleaned.strip()
    return raw_response.strip()


def translate_to_chinese(text: str, client) -> str:
    """Translate English text to Simplified Chinese."""
    if re.search(r"[\u4e00-\u9fff]", text):
        return text.strip()

    messages = [
        SystemMessage(
            content=(
                "You are a professional translator. "
                "Translate English to fluent Simplified Chinese only."
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
    cleaned_content = clean_translation_output(completion.content)
    return cleaned_content.strip()


def translate_to_english(text: str, client) -> str:
    """Translate Chinese text to English for keyword matching."""
    messages = [
        SystemMessage(
            content=(
                "Translate Chinese to fluent, professional English. "
                "Only output the translation."
            )
        ),
        HumanMessage(content=f"Translate to English:\n{text}"),
    ]
    completion = client.invoke(messages)
    cleaned_content = clean_translation_output(completion.content)
    return cleaned_content.lower().strip()


def get_bilingual_keywords(user_input, client):
    """
    Return a pair of keywords: [Chinese keyword, English keyword].
    """
    user_input = user_input.strip()
    is_chinese = re.search(r"[\u4e00-\u9fff]", user_input) is not None

    if is_chinese:
        cn_key = user_input
        en_key = translate_to_english(user_input, client)
    else:
        en_key = user_input.lower()
        cn_key = translate_to_chinese(user_input, client)

    return [cn_key.strip(), en_key.strip()]


def filter_by_both_keywords(personas, cn_key, en_key):
    """Keep personas that match either the Chinese or English keyword."""
    result = []
    for persona in personas:
        text = persona["input persona"]
        text_lower = text.lower()

        if cn_key in text or en_key in text_lower:
            result.append(persona)
    return result


def save_result(personas, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        for persona in personas:
            f.write(json.dumps(persona, ensure_ascii=False) + "\n")
    print(f"Initial filtering selected {len(personas)} personas.")
