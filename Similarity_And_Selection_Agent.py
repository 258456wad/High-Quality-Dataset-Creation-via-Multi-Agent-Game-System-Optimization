from similarity_evaluator import SimilarityEvaluator
from data_deduplicator import DataDeduplicator
import numpy as np
class SimilarityAndSelectionAgent:
    def __init__(self, embedding_client):
        self.evaluator = SimilarityEvaluator(embedding_client)
        self.deduplicator = DataDeduplicator()
    def process(self, raw_data_list):
        if not raw_data_list:
            return []
        assessment_report = self.evaluator.analyze(raw_data_list)
        final_selected_data = self.deduplicator.clean(raw_data_list, assessment_report)
        removed_count = len(raw_data_list) - len(final_selected_data)
        return final_selected_data
