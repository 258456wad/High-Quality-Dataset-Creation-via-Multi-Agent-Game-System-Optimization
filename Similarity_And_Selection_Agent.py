from similarity_evaluator import SimilarityEvaluator
from data_deduplicator import DataDeduplicator
import numpy as np


# def plot_clusters(embeddings, labels, eps):
#     """
#     使用 PCA 将高维 Embedding 降维并可视化聚类结果
#     """
#     # 1. 降维：将 1024 维降至 2 维
#     pca = PCA(n_components=2)
#     reduced_data = pca.fit_transform(embeddings)
#
#     # 2. 设置绘图
#     plt.figure(figsize=(10, 7))
#     unique_labels = set(labels)
#
#     # 为不同的簇分配颜色
#     colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
#
#     for k, col in zip(unique_labels, colors):
#         if k == -1:
#             # 噪声点（离群点）用黑色表示
#             col = [0, 0, 0, 1]
#             label_name = "Noise (Outliers)"
#         else:
#             label_name = f"Cluster {k}"
#
#         class_member_mask = (labels == k)
#         xy = reduced_data[class_member_mask]
#
#         plt.scatter(xy[:, 0], xy[:, 1], c=[col], label=label_name,
#                     edgecolors='k', s=50, alpha=0.7)
#
#     plt.title(f'DBSCAN Clustering (PSO Optimized eps: {eps:.4f})')
#     plt.xlabel('PCA Component 1')
#     plt.ylabel('PCA Component 2')
#     plt.legend(loc='best', bbox_to_anchor=(1, 1), fontsize='small', ncol=2)
#     plt.grid(True, linestyle='--', alpha=0.5)
#     plt.show()

class SimilarityAndSelectionAgent:
    def __init__(self, embedding_client):
        """
        初始化智能体，接入评估和去重两个独立工具
        """
        self.evaluator = SimilarityEvaluator(embedding_client)
        self.deduplicator = DataDeduplicator()



    def process(self, raw_data_list):
        """
        完整的评估与去重流
        """
        if not raw_data_list:
            return []

        # print(f"[Similarity_And_Selection_Agent] 开始处理 {len(raw_data_list)} 条原始样本...")

        # 1. 接入相似度评估工具 (数学计算层)
        # 获取包含 MinHash、Embedding 和 DBSCAN 标签的报告
        assessment_report = self.evaluator.analyze(raw_data_list)

        print(f"[Similarity_And_Selection_Agent] 评估完成。PSO 寻优 eps 为: {assessment_report['eps']}")

        # 2. 接入去重工具 (逻辑清洗层)
        # 根据评估出的 labels 进行物理筛选
        final_selected_data = self.deduplicator.clean(raw_data_list, assessment_report)

        # 3. 输出统计
        removed_count = len(raw_data_list) - len(final_selected_data)
        print(f"[Similarity_And_Selection_Agent] 去重任务完成: 原始 {len(raw_data_list)} -> 剩余 {len(final_selected_data)} (去重 {removed_count} 条)")


        # # 传入报告中的向量和标签进行绘图
        # plot_clusters(
        #     embeddings=assessment_report['embeddings'],
        #     labels=assessment_report['labels'],
        #     eps=assessment_report['eps']
        # )
        return final_selected_data