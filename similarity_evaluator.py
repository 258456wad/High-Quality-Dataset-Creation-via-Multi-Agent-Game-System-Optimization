import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score


class SimilarityEvaluator:
    def __init__(self, client):
        self.client = client  # 用于调用 Embedding API

    # def _get_minhash(self, text):
    #     m = MinHash(num_perm=128)
    #     # 1-gram 处理
    #     for word in list(text):
    #         m.update(word.encode('utf8'))
    #     return m

    def _get_embeddings(self, texts):
        # 修正：直接调用你测试成功的 embed_documents 方法
        # 这一步会解决之前的 AttributeError 报错
        return np.array(self.client.embed_documents(texts))

    def pso_optimize_dbscan(self, embeddings):
        """
        基于原生粒子群算法(PSO)寻找最优 eps 参数。
        通过模拟粒子在解空间内的惯性、个体最优和全局最优更新，寻找使轮廓系数最高的聚类半径。
        """
        # 1. 初始化 PSO 参数
        n_particles = 10  # 粒子数量
        iters = 15  # 迭代次数
        w, c1, c2 = 0.5, 1.5, 1.5  # 惯性权重、个体学习因子、社会学习因子

        # 2. 随机初始化粒子的位置(eps)和速度
        # eps 搜索范围设定在 0.05 到 0.5 之间，步长更精细，
        particles_pos = np.random.uniform(0.1, 0.25, n_particles) # 聚类半径eps，初始分配的位置
        particles_vel = np.zeros(n_particles)

        # 记录个体最优位置和全局最优位置
        p_best_pos = np.copy(particles_pos)
        p_best_score = np.full(n_particles, -1.0)
        g_best_pos = 0.15  # 初始全局最优候选
        g_best_score = -1.0

        # 3. 开始迭代寻优
        for t in range(iters):
            for i in range(n_particles):
                # 【强制约束 1】大幅缩小 eps 搜索上限，强制进入“精细去重”模式
                # 余弦距离 0.05-0.15 之间通常是金融问答语义极其接近的区间
                eps_val = particles_pos[i]

                # 边界约束：确保 eps 在合理范围内，相似度，防止粒子每次迭代跑太远或太近
                eps_val = max(0.1, min(eps_val, 0.25))

                # 执行聚类评估
                db = DBSCAN(eps=eps_val, min_samples=2, metric='cosine').fit(embeddings)
                n_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)
                # 只有当聚类数大于1时，轮廓系数才有意义
                if len(set(db.labels_)) > 1:
                    # 显存/内存保护：如果数据量极大，建议在此处进行采样计算
                    base_score = silhouette_score(embeddings, db.labels_, metric='cosine')
                    # 【强制约束 2】惩罚单一簇，奖励多簇。让算法倾向于分出 10-30 个簇
                    # 这样可以确保 n-1 策略能删掉几十条数据
                    # 计算被聚类的点（非噪声点）占总数的比例
                    n_noise = list(db.labels_).count(-1)
                    coverage = (len(embeddings) - n_noise) / len(embeddings)
                    penalty = 1.0 if n_clusters > 5 else 0.5
                    # 调整 score：既要聚类质量（base_score），也要覆盖率（coverage）
                    score = base_score * penalty+ (coverage * 0.5) # 这里是权重
                    # score = silhouette_score(embeddings, db.labels_, metric='cosine')

                    # 更新个体最优
                    if score > p_best_score[i]:
                        p_best_score[i] = score
                        p_best_pos[i] = eps_val

                    # 更新全局最优
                    if score > g_best_score:
                        g_best_score = score
                        g_best_pos = eps_val

            # 4. 更新粒子的速度和位置（PSO 核心公式）
            r1, r2 = np.random.rand(), np.random.rand()
            particles_vel = (w * particles_vel +
                             c1 * r1 * (p_best_pos - particles_pos) +
                             c2 * r2 * (g_best_pos - particles_pos))
            particles_pos += particles_vel

        # 轮廓系数越接近 1：说明簇内点非常近（紧凑），且离其他簇非常远（分离度高）。这是一个完美的聚类
        print(f"--- PSO 寻优完成：最优 eps = {g_best_pos:.4f}, 最高轮廓系数 = {g_best_score:.4f} ---")
        return g_best_pos
    # def pso_optimize_dbscan(self, embeddings):
    #     """
    #     利用粒子群算法思想寻找最优的 eps 参数
    #     这里简化为启发式搜索，实际可接入 PySwarms 库
    #     """
    #     best_eps = 0.5
    #     best_score = -1
    #     # 模拟粒子群在 0.1 到 0.9 之间寻找使轮廓系数最高的 eps
    #     for eps_candidate in np.linspace(0.1, 0.9, 10):
    #         db = DBSCAN(eps=eps_candidate, min_samples=2, metric='cosine').fit(embeddings)
    #         if len(set(db.labels_)) > 1:
    #             score = silhouette_score(embeddings, db.labels_, metric='cosine')
    #             if score > best_score:
    #                 best_score = score
    #                 best_eps = eps_candidate
    #     return best_eps

    def analyze(self, raw_data_list):
        """
        综合评估入口：MinHash + Embedding + PSO-DBSCAN
        """
        # texts = [item['response'] for item in raw_data_list]
        # 【关键改动】只提取 response 字段，排除 prompt 干扰
        # responses = [item['response'] for item in raw_data_list]
        combined_texts = [
            f"问题：{item['prompt']}\n回答：{item['response']}"
            for item in raw_data_list
        ]

        # 1. 语义向量化
        embeddings = self._get_embeddings(combined_texts)

        # 2. PSO 寻优并执行 DBSCAN 聚类
        optimal_eps = self.pso_optimize_dbscan(embeddings)
        db = DBSCAN(eps=optimal_eps, min_samples=2, metric='cosine').fit(embeddings)

        # 3. 返回聚类结果报告
        return {
            "labels": db.labels_,
            "embeddings": embeddings,
            "eps": optimal_eps
        }