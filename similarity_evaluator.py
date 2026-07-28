import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score


class SimilarityEvaluator:
    def __init__(self, client):
        self.client = client

    def _get_embeddings(self, texts):
        return np.array(self.client.embed_documents(texts))

    def pso_optimize_dbscan(self, embeddings):
        """
        Use a lightweight particle swarm optimization loop to search for the
        best DBSCAN eps value.
        """
        n_particles = 10
        iters = 15
        w, c1, c2 = 0.5, 1.5, 1.5

        particles_pos = np.random.uniform(0.1, 0.25, n_particles)
        particles_vel = np.zeros(n_particles)

        p_best_pos = np.copy(particles_pos)
        p_best_score = np.full(n_particles, -1.0)
        g_best_pos = 0.15
        g_best_score = -1.0

        for _ in range(iters):
            for i in range(n_particles):
                eps_val = particles_pos[i]
                eps_val = max(0.1, min(eps_val, 0.25))

                db = DBSCAN(eps=eps_val, min_samples=2, metric="cosine").fit(embeddings)
                n_clusters = len(set(db.labels_)) - (1 if -1 in db.labels_ else 0)

                if len(set(db.labels_)) > 1:
                    base_score = silhouette_score(embeddings, db.labels_, metric="cosine")
                    n_noise = list(db.labels_).count(-1)
                    coverage = (len(embeddings) - n_noise) / len(embeddings)
                    penalty = 1.0 if n_clusters > 5 else 0.5
                    score = base_score * penalty + (coverage * 0.5)

                    if score > p_best_score[i]:
                        p_best_score[i] = score
                        p_best_pos[i] = eps_val

                    if score > g_best_score:
                        g_best_score = score
                        g_best_pos = eps_val

            r1, r2 = np.random.rand(), np.random.rand()
            particles_vel = (
                w * particles_vel
                + c1 * r1 * (p_best_pos - particles_pos)
                + c2 * r2 * (g_best_pos - particles_pos)
            )
            particles_pos += particles_vel

        print(
            "--- PSO optimization completed: "
            f"best eps = {g_best_pos:.4f}, best silhouette score = {g_best_score:.4f} ---"
        )
        return g_best_pos

    def analyze(self, raw_data_list):
        """
        Run semantic embedding plus PSO-DBSCAN similarity assessment.
        """
        combined_texts = [
            f"Question: {item['prompt']}\nAnswer: {item['response']}"
            for item in raw_data_list
        ]
        embeddings = self._get_embeddings(combined_texts)

        optimal_eps = self.pso_optimize_dbscan(embeddings)
        db = DBSCAN(eps=optimal_eps, min_samples=2, metric="cosine").fit(embeddings)

        return {
            "labels": db.labels_,
            "embeddings": embeddings,
            "eps": optimal_eps,
        }
