import numpy as np

from dataset_synthesize import main_all


class GeneratorAgent:
    def __init__(self, client, persona_dataset):
        """
        persona_dataset: persona records used for future weighting or sampling.
        """
        self.client = client
        self.persona_pool = persona_dataset
        self.weights = np.ones(len(persona_dataset))
        self.used_indices = set()
        self.now_pool = list(persona_dataset)

    def execute_task(self, template, sample_size, output_path, system_prompt):
        """
        Main execution entry point for the generation agent.
        """
        print("\n[Generator Agent] Planning the generation task.")
        if len(self.now_pool) < sample_size:
            print(
                f"Warning: not enough available personas. "
                f"Remaining: {len(self.now_pool)}, requested: {sample_size}."
            )
            sample_size = len(self.now_pool)

        current_indices_in_now_pool = np.random.choice(
            len(self.now_pool), size=sample_size, replace=False
        )

        sub_persona_dataset = [self.now_pool[i] for i in current_indices_in_now_pool]
        current_original_indices = [item["_original_idx"] for item in sub_persona_dataset]

        indices_set = set(current_indices_in_now_pool)
        self.now_pool = [
            item for idx, item in enumerate(self.now_pool) if idx not in indices_set
        ]
        self.used_indices.update(current_original_indices)

        total_used = len(self.persona_pool) - len(self.now_pool)
        print(
            f"This round used {len(sub_persona_dataset)} personas. "
            f"Available personas remaining: {len(self.now_pool)}."
        )
        print(
            f"Total consumed personas: {total_used}; "
            f"unique consumed persona IDs: {len(self.used_indices)}."
        )

        main_all(
            client=self.client,
            template=template,
            sample_size=sample_size,
            output_path=output_path,
            persona_dataset=sub_persona_dataset,
            system_prompt=system_prompt,
        )

        return output_path
