class DataDeduplicator:
    def __init__(self, top_k_per_cluster=3):
        """
                top_k_per_cluster: 每个相似簇保留的数据条数
                """
        self.top_k_per_cluster = top_k_per_cluster

    def clean(self, raw_data_list, assessment_report):
        labels = assessment_report['labels']
        cleaned_data = []
        noise_count = 0  # 新增：离群点计数器

        # 1. 按簇归类索引
        cluster_map = {}
        for idx, label in enumerate(labels):
            if label == -1:  # 离群点直接保留
                cleaned_data.append(raw_data_list[idx])
                noise_count += 1  # 统计离群点
            else:
                if label not in cluster_map:
                    cluster_map[label] = []
                cluster_map[label].append(raw_data_list[idx])
        # 打印离群点统计
        # print(f"--- 离群点(唯一数据)共有 {noise_count} 条，已全部保留 ---")
        # 2. 遍历每个簇
        for label, items in cluster_map.items():
            n = len(items)  # 这就是你关心的簇内数据条数

            if n > 1:
                # 按照 response 长度从大到小排序，确保“差生”排在最后
                items.sort(key=lambda x: len(x.get('response', '')), reverse=True)
                keep_n = max(1, int(n * (1-assessment_report["eps"])))
                # 保留数据
                survivors = items[:keep_n]
                cleaned_data.extend(survivors)
                # print(f"簇 {label} 共有 {n} 条数据，保留 {keep_n} 条。")
            else:
                # 如果只有 1 条，n-1 就变成 0 了，所以这种特殊情况要全留
                cleaned_data.extend(items)

        return cleaned_data
    # def clean(self, raw_data_list, assessment_report):
    #     labels = assessment_report['labels']
    #     cleaned_data = []
    #     cluster_count_map = {}
    #
    #     for idx, label in enumerate(labels):
    #         # 情况 A: 离群点 (Label == -1)，直接保留
    #         if label == -1:
    #             cleaned_data.append(raw_data_list[idx])
    #         else:
    #             # 情况 B: 属于某个相似簇 (Label >= 0)
    #             if label not in cluster_count_map:
    #                 cluster_count_map[label] = 0
    #
    #                 # 如果该簇已保留的数量还没达到阈值，则继续添加
    #             if cluster_count_map[label] < self.top_k_per_cluster:
    #                 cleaned_data.append(raw_data_list[idx])
    #                 cluster_count_map[label] += 1
    #             else:
    #                 # 超过阈值的部分才会被真正剔除
    #                 pass
    #             # # 策略：每个簇只保留第一条出现的（或长度最长的）
    #             # if label not in cluster_map:
    #             #     cluster_map[label] = raw_data_list[idx]
    #             #     cleaned_data.append(raw_data_list[idx])
    #             # else:
    #             #     # 如果当前这条比簇内已有的更长，则更新（可选优化）
    #             #     if len(raw_data_list[idx]['response']) > len(cluster_map[label]['response']):
    #             #         # 注意：这里仅作演示逻辑，实际去重通常只需保留一个代表
    #             #         pass
    #
    #     return cleaned_data