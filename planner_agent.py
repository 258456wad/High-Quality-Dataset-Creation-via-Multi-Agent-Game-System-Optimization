import json
import os
import re

from datasets import load_dataset
from langchain_core.messages import HumanMessage

from personal_filter import (
    filter_by_both_keywords,
    get_bilingual_keywords,
    save_result,
)


class PlannerAgent:
    def __init__(self, client, personal_filter, persona_filter_path):
        self.client = client
        self.model = "deepseek-chat"
        self.personal_filter = personal_filter
        self.persona_filter_path = persona_filter_path

    def plan(self, user_raw_input, output_path, persona_dataset):
        """
        Convert a natural-language dataset request into a structured task config.
        """
        print("[Planner Agent] Parsing the user instruction.")

        persona_filter_dataset = []
        if self.personal_filter is None or self.personal_filter.strip() == "":
            persona_filter_dataset = persona_dataset
            os.makedirs(os.path.dirname(self.persona_filter_path), exist_ok=True)
            with open(self.persona_filter_path, "w", encoding="utf-8") as f:
                for persona in persona_filter_dataset:
                    f.write(json.dumps(persona, ensure_ascii=False) + "\n")
            print(f"Initial filtering selected {len(persona_filter_dataset)} personas.")
        else:
            cn_key, en_key = get_bilingual_keywords(self.personal_filter, self.client)
            final_roles = filter_by_both_keywords(persona_dataset, cn_key, en_key)
            save_result(final_roles, self.persona_filter_path)

            raw_data = load_dataset("json", data_files=self.persona_filter_path)["train"]
            for i, item in enumerate(raw_data):
                item["_original_idx"] = i
                persona_filter_dataset.append(item)

        actual_count = len(persona_filter_dataset)

        prompt = f"""
You are a top-tier AI instruction architect. Convert the user's rough dataset
synthesis request into one highly structured JSON configuration.

### Current Environment
- Available personas after filtering (actual_count): {actual_count}

### Raw User Request
"{user_raw_input}"

### Required JSON Fields
1. "template":
   - Rewrite the user's request into a persona-grounded question-generation prompt.
   - Core goal: ask the LLM to adopt the {{persona}} identity and raise a professional, specific, challenging real-world question based on that persona's occupational background.
   - Placeholder requirement: the template must contain the literal placeholder `{{persona}}`.
   - Suggested guidance:
     - "Assume the following role: {{persona}}. Based on your professional background and daily work, design one realistic, highly specialized, and challenging question you would genuinely encounter."
     - "Output only the question content. Do not include filler such as 'my question is' or 'here is the question'."
     - "Do not output explanatory content. Only output the question itself."
   - If the user asks for professional depth, explicitly require industry terminology, no filler, and domain-level rigor.
   - The template must target one persona at a time. Do not ask the model to generate X samples because the system handles repeated calls.
   - When domain terminology is involved, prefer clear professional English rather than long untranslated foreign passages.

2. "sample_size":
   - Extract the total number of requested samples.
   - If the user writes the number in words, convert it to an integer.
   - If the user asks for all available samples, as many as possible, or every searchable sample, output {actual_count}.
   - If the user gives a specific number, convert it to an integer.
   - If the user does not specify a quantity, default to 5.
   - This field must be an integer, not a string.

3. "output_path":
   - Keep this value exactly as "{output_path}".

4. "domain_expert":
   - Identify the professional domain of the task, such as quantitative finance, legal compliance, code auditing, or risk management.

### Constraints
- Do not repeat the raw user request.
- Ensure the generated `template` is logically precise and activates the persona's professional traits.
- Output JSON only, with no preface or closing explanation.
- Ensure the {{persona}} placeholder is integrated naturally.
- Keep punctuation clean and avoid repeated punctuation marks.
"""

        messages = [HumanMessage(content=prompt)]

        response = self.client.invoke(
            input=messages,
            extra_body={"response_format": {"type": "json_object"}},
        )

        result = response.content
        json_match = re.search(r"```json\s*({[\s\S]*?})\s*```", result)
        if json_match:
            json_str = json_match.group(1)
        else:
            json_match = re.search(r"({[\s\S]*})", result)
            if json_match:
                json_str = json_match.group(1)
            else:
                raise ValueError("No valid JSON object found in planner response.")

        instruction_config = json.loads(json_str)
        return instruction_config, persona_filter_dataset
