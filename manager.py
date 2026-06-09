from datasets import load_dataset
import os
from planner_agent import PlannerAgent
from generator_agent import GeneratorAgent
from Similarity_And_Selection_Agent import SimilarityAndSelectionAgent
from langchain_deepseek import ChatDeepSeek
from langchain_huggingface import HuggingFaceEmbeddings
from huggingface_hub import InferenceClient
import json

def main():
    # 0. 用户输入一段话
    user_input = "我想要输出5000条高质量合成化的数据集，而且是基于人设的，比较专业的"
    personal_filter_need = 0    # 1代表需要，0代表不用
    user_need = 1  # 1代表需要，0代表不用
    # user_input = input("请输入您的数据集构建需求：")
    # personal_filter_need=int(input("请输入是否需要用关键词进行初步筛选（1代表需要，0代表不用）："))
    # 初始化为一个空状态
    personal_filter = None
    if personal_filter_need == 1:
        personal_filter = input("请输入您想要的风格（筛选关键词）：")
    else:
        print("--- 跳过初步筛选，将使用全量角色库进行生成 ---")
    # user_need = int(input("请输入是否需要进行多轮反馈生成（1代表需要，0代表不用）："))
    # 0.o 初始化基础配置
    # system_prompt = '''You are a helpful assistant.'''
    # 专家类型提示词
    system_prompt = '''你是一名专业的数据合成专家。你的任务是模拟特定人设的思维方式，生成具有逻辑深度和专业挑战性的指令。请确保输出内容的严谨性，避免口水话。'''
    # 源数据集路径
    persona_dataset_path = "data/persona.jsonl"  # 记得修改输入的路径
    # 初筛角色数据集路径
    persona_filter_path = "data/persona_filter_5000.jsonl"  # 记得修改输入的路径
    # 数据生成后输出文件路径(未反馈去重)
    output_path = "output_data/manager_fankui_5000.jsonl"  # 记得修改输出的路径
    # 去重后输出文件路径
    select_output_path = "output_data/select_output_manager_fankui_5000.jsonl"  # 记得修改输出的路径

    # print(f"数据源: {persona_dataset_path}")
    # print(f"输出位置: {output_path}")
    # 2.1 在启动所有任务前，先清空目标文件（如果文件存在）
    if os.path.exists(output_path):
        with open(output_path, 'w', encoding='utf-8') as f:
            f.truncate(0)  # 清空文件内容
        # print(f"--- 已初始化：清空旧数据 {output_path} ---")
    else:
        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if os.path.exists(select_output_path):
        with open(select_output_path, 'w', encoding='utf-8') as f:
            f.truncate(0)  # 清空文件内容
        # print(f"--- 已初始化：清空旧数据 {select_output_path} ---")
    else:
        # 确保目录存在
        os.makedirs(os.path.dirname(select_output_path), exist_ok=True)

    # 【关键改动】在这里读文件，把路径变成真正的 List 对象
    # 这样 persona_data 就是一个包含 20 万个字典的列表了
    raw_data = load_dataset("json", data_files=persona_dataset_path, cache_dir="temp_cache")['train']
    # persona_dataset = [item for item in raw_data]
    # 给每一行数据增加一个原始索引字段
    persona_dataset = []
    for i, item in enumerate(raw_data):
        item['_original_idx'] = i  # 记录它在原始文件里的行号
        persona_dataset.append(item)

    # client = OpenAI(api_key="sk-81c79590bb1243a6bfddbd5d87a96ff0", base_url="https://api.deepseek.com")
    # 本机电脑api
    api_key = os.environ.get("DEEPSEEK_API_KEY", "sk-81c79590bb1243a6bfddbd5d87a96ff0")
    api_base = os.environ.get("DEEPSEEK_API_BASE") or os.environ.get("DEEPSEEK_API_BASE_URL")
    client = ChatDeepSeek(
        model="deepseek-chat",
        api_key=api_key,
        api_base="https://api.deepseek.com",
        temperature=0.1,
        timeout=120
    )



    # # 中证环境api
    # api_key=os.environ.get("DEEPSEEK_API_KEY","sk-92771ee89bb145879c210aa4030e3a99")
    # api_base=os.environ.get("DEEPSEEK_API_BASE") or os.environ.get("DEEPSEEK_API_BASE_URL")
    # client = ChatDeepSeek(
    #     model="qwen3-235b",
    #     api_key=api_key,
    #     api_base="http://10.131.100.60:1025/v1",
    #     temperature=0.1
    # )

    # # 初始化指令配置区 [cite: 1, 2, 4]
    # instruction_config = {
    #     "template": "universal_gen_v2_cn",
    #     "sample_size": 10,
    #     "output_path": output_path
    # }


    # 1.需求规划智能体
    planner = PlannerAgent(client, personal_filter, persona_filter_path)
    # 这一步就把你那一段话变成了 config 字典
    instruction_config, persona_filter_dataset = planner.plan(user_input, output_path, persona_dataset)

    # print(instruction_config)


    if user_need==1: # 如果用户需要反馈，就反馈生成
        gold_standard_pool = []  # 最终高质量池子
        used_persona_indices = set()  # 记录已经用过的人设索引，防止重复抽取

        # 初始化智能体
        agent = GeneratorAgent(client, persona_filter_dataset)

        # ==========================================
        # 3.接入相似度评估与去重智能体
        # ==========================================
        # 跑向量，向量模型，本地部署
        # 1. 定义超级长的本地模型路径
        model_path = "bge-large-zh-v1.5"
        # 2. 直接加载模型到 GPU (1650 Ti)
        print("--- 正在加载本地 BGE 模型至显卡... ---")
        embed_client = HuggingFaceEmbeddings(
            model_name=model_path,
            model_kwargs={
                "device": "cuda"  # ✔ GPU
                # "device": "npu"  # 中证的
            },
            encode_kwargs={
                "normalize_embeddings": True,
                "batch_size": 8  # ✔ 防止爆显存
            }
        )
        similarity_agent = SimilarityAndSelectionAgent(embed_client)
        times = 0  # 计数用的
        # 2. 闭环合成循环
        while len(gold_standard_pool) < instruction_config['sample_size']:
            times += 1  # 更新计数循环
            # A. 检查初筛库是否还有剩余人设
            remaining_indices=agent.now_pool
            # remaining_indices = [i for i in range(len(persona_filter_dataset)) if i not in used_persona_indices]

            if not remaining_indices:
                print("--- 【注意】初筛数据库已耗尽，无法继续生成更多数据 ---")
                break

            # B. 计算本轮需要补齐的差额 (Batch Size)
            needed_now = instruction_config['sample_size'] - len(gold_standard_pool)
            # 这一轮尝试抽取人设的数量，建议稍微多抽一点（比如 Needed * 1.2），因为去重会有损耗
            # 但不能超过初筛库剩余总量
            current_batch_size = min(needed_now, len(remaining_indices))

            print(f"--- 反馈循环进度: {len(gold_standard_pool)}/{instruction_config['sample_size']} | 第{times}轮抽取 {current_batch_size} 条人设进行生成 ---")

            # C. 循环生成（这一步只存当前轮次的结果，不覆盖 output_path）
            # 这里建议修改 GeneratorAgent.execute_task 让它返回 List 而不是只写文件
            # 如果不方便改源码，我们可以通过读取 output_path 的增量来获取
            # 2.2 向智能体传递指令并执行任务 [cite: 14]
            # 【修复代码】每轮生成前，必须物理清空 output_path
            if os.path.exists(output_path):
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.truncate(0)
            agent.execute_task(
                template=instruction_config['template'],
                sample_size=current_batch_size,  # 本轮只生成这么多
                output_path=output_path,
                system_prompt=system_prompt
            )
            print(f"[Generator Agent] 第{times}轮执行完毕，结果已保存至: {output_path}")

            # 读取刚刚生成的 JSONL 数据
            # D. 读取本轮生成的数据并进行评估去重
            current_raw_samples = []
            if os.path.exists(output_path):
                with open(output_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        current_raw_samples.append(json.loads(line.strip()))

            if not current_raw_samples:
                print("警告：本轮未生成数据。")
                continue

            # E. 相似度去重（传入已有的池子 + 本轮新数据，进行全局去重）
            # 建议 similarity_agent.process 支持接收 (新数据, 已有数据池)
            # 如果不支持，就合并后处理
            if current_raw_samples:
                combined_for_filter = gold_standard_pool + current_raw_samples
                print(f"--- Similarity And Selection Agent启动相似度过滤：当前样本数 {len(combined_for_filter )} ---")
                cleaned_data = similarity_agent.process(combined_for_filter)
                # 更新池子
                if cleaned_data is not None:
                    gold_standard_pool = cleaned_data
                    if gold_standard_pool:
                        with open(select_output_path, 'w', encoding='utf-8') as f:
                            for item in gold_standard_pool:
                                f.write(json.dumps(item, ensure_ascii=False) + '\n')
                else:
                    print("⚠️ 警告：去重智能体返回 None，维持原池子进入下一轮重试。")

            print(f"--- 第{times}轮过滤后，高质量池子总数达到: {len(gold_standard_pool)} 条 ---")

        # 3. 最终保存
        print(f"--- 任务结束，最终产出 {len(gold_standard_pool)} 条高质量数据 ---")
        if gold_standard_pool:
            # with open(select_output_path, 'w', encoding='utf-8') as f:
            #     for item in gold_standard_pool:
            #         f.write(json.dumps(item, ensure_ascii=False) + '\n')
            print(f"--- 过滤完成：剩余高质量样本 {len(gold_standard_pool)} 条 ---")
        else:
            print("警告：没有生成任何原始样本，跳过去重环节。")
        return 0

    # ==========================================
    # 第二部分.不需要反馈
    # ==========================================
    else: # 如果不需要反馈就直接生成
        # 2. 数据生成智能体

        # 初始化智能体
        agent = GeneratorAgent(client, persona_filter_dataset)

        # 2.2 向智能体传递指令并执行任务 [cite: 14]
        print(f"--- 系统指令，启动任务：{instruction_config} ---")
        output_path = agent.execute_task(
            template=instruction_config['template'],
            sample_size=instruction_config['sample_size'],
            output_path=output_path,
            system_prompt=system_prompt
        )
        print(f"[Generator Agent] 第一轮执行完毕，结果已保存至: {output_path}")

        # ==========================================
        # 3.接入相似度评估与去重智能体
        # ==========================================
        # 跑向量，向量模型，本地部署
        # 1. 定义超级长的本地模型路径
        model_path = "bge-large-zh-v1.5"
        # 2. 直接加载模型到 GPU (1650 Ti)
        print("--- 正在加载本地 BGE 模型至显卡... ---")
        embed_client = HuggingFaceEmbeddings(
            model_name=model_path,
            model_kwargs={
                "device": "cuda"  # ✔ GPU
                # "device": "npu"  # 中证的
            },
            encode_kwargs={
                "normalize_embeddings": True,
                "batch_size": 8  # ✔ 防止爆显存
            }
        )
        similarity_agent = SimilarityAndSelectionAgent(embed_client)
        # 读取刚刚生成的 JSONL 数据
        raw_samples = []

        with open(output_path, 'r', encoding='utf-8') as f:
            for line in f:
                raw_samples.append(json.loads(line.strip()))

        if raw_samples:
            print(f"--- 启动相似度过滤：当前样本数 {len(raw_samples)} ---")

            # 2. 执行评估与去重流水线
            # process 内部会调用评估工具 (MinHash/Embedding/PSO-DBSCAN) 和去重工具
            final_cleaned_data = similarity_agent.process(raw_samples)

            # 3. 将去重后的高质量数据覆盖写回文件（或保存到新路径）
            with open(select_output_path, 'w', encoding='utf-8') as f:
                for item in final_cleaned_data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')

            print(f"--- 过滤完成：剩余高质量样本 {len(final_cleaned_data)} 条 ---")
            # print(f"高质量数据集输出{final_cleaned_data}")
        else:
            print("警告：没有生成任何原始样本，跳过去重环节。")

        # print(f"恭喜！{instruction_config.get('domain_expert', '金融')} 领域的高质量数据集已构建完成。")

        return 0





if __name__ == "__main__":
    main()