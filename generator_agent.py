import os
import numpy as np
# 导入固定接口的 main_all
from dataset_synthesize import main_all

class GeneratorAgent:
    def __init__(self, client, persona_dataset):
        """
        初始化智能体
        persona_dataset: 传入的人设数据集对象（用于未来计算权重或采样）
        """
        self.client = client
        self.persona_pool = persona_dataset # 总库
        self.weights = np.ones(len(persona_dataset))
        self.used_indices = set() # 已经用过的索引
        self.now_pool=list(persona_dataset) # 初始化现有的库

    def execute_task(self, template, sample_size, output_path, system_prompt):
        """
        这个方法是智能体的执行入口
        """
        # print(f"\n[Generator Agent] 正在规划任务: {template} 目标数量: {sample_size}")
        print(f"\n[Generator Agent] 正在规划任务。")
        # 1. 检查现有库是否足够
        if len(self.now_pool) < sample_size:
            print(f"警告：可用人设不足！剩余 {len(self.now_pool)}，请求 {sample_size}")
            sample_size = len(self.now_pool)

        # 2. 从“现有库”的当前长度里随机抽取下标
        # 注意：这里我们只针对 now_pool 进行操作，提取下标
        current_indices_in_now_pool = np.random.choice(len(self.now_pool), size=sample_size, replace=False)

        # 3. 提取出本轮要用的“子集”数据，提取数据
        sub_persona_dataset = [self.now_pool[i] for i in current_indices_in_now_pool]
        current_original_indices = [item['_original_idx'] for item in sub_persona_dataset]

        # 4. 【核心动作】更新现有库：把选中的人设从 now_pool 中删掉
        # 使用 set 查找下标速度更快，删掉选中的数据
        indices_set = set(current_indices_in_now_pool)
        self.now_pool = [item for idx, item in enumerate(self.now_pool) if idx not in indices_set]
        self.used_indices.update(current_original_indices)

        # 5. 更新累计消耗记录（用于汇报）
        # 累计消耗 = 总库长度 - 剩余长度
        total_used = len(self.persona_pool) - len(self.now_pool)
        print(f"本轮消耗 {len(sub_persona_dataset)} 个角色。现有库剩余可用: {len(self.now_pool)}")
        print(f"当前累计已消耗角色总数: {total_used},对比看used计算的当前累计已消耗角色总数: {len(self.used_indices)}")
        # print(f"累计索引的角色ID：{self.used_indices}")

        # 6. 执行工具调用
        # 这里直接驱动你写好的 main_all
        main_all(
            client=self.client,
            template=template,
            sample_size=sample_size,
            output_path=output_path,
            persona_dataset=sub_persona_dataset,
            system_prompt=system_prompt
        )


        # print(f"[Generator Agent] 执行完毕，结果已保存至: {output_path}")
        return output_path