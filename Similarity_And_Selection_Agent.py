from data_deduplicator import DataDeduplicator
from similarity_evaluator import SimilarityEvaluator


class SimilarityAndSelectionAgent:
    def __init__(self, embedding_client):
        """
        Connect the similarity evaluator and deduplication tools.
        """
        self.evaluator = SimilarityEvaluator(embedding_client)
        self.deduplicator = DataDeduplicator()

    def process(self, raw_data_list):
        """
        Run the full similarity assessment and deduplication flow.
        """
        if not raw_data_list:
            return []

        assessment_report = self.evaluator.analyze(raw_data_list)

        print(
            "[SimilarityAndSelectionAgent] Assessment completed. "
            f"PSO-optimized eps: {assessment_report['eps']}"
        )

        final_selected_data = self.deduplicator.clean(raw_data_list, assessment_report)

        removed_count = len(raw_data_list) - len(final_selected_data)
        print(
            "[SimilarityAndSelectionAgent] Deduplication completed: "
            f"raw {len(raw_data_list)} -> selected {len(final_selected_data)} "
            f"(removed {removed_count})."
        )

        return final_selected_data
