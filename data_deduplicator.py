class DataDeduplicator:
    def __init__(self, top_k_per_cluster=3):
        """
        top_k_per_cluster: number of records retained from each similarity cluster.
        """
        self.top_k_per_cluster = top_k_per_cluster

    def clean(self, raw_data_list, assessment_report):
        labels = assessment_report["labels"]
        cleaned_data = []
        noise_count = 0

        cluster_map = {}
        for idx, label in enumerate(labels):
            if label == -1:
                cleaned_data.append(raw_data_list[idx])
                noise_count += 1
            else:
                if label not in cluster_map:
                    cluster_map[label] = []
                cluster_map[label].append(raw_data_list[idx])

        for label, items in cluster_map.items():
            n = len(items)

            if n > 1:
                items.sort(key=lambda x: len(x.get("response", "")), reverse=True)
                keep_n = max(1, int(n * (1 - assessment_report["eps"])))
                survivors = items[:keep_n]
                cleaned_data.extend(survivors)
            else:
                cleaned_data.extend(items)

        return cleaned_data
