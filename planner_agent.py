import json
from personal_filter import *
from langchain_core.messages import HumanMessage
from datasets import load_dataset
import re

class PlannerAgent:
    def __init__(self, client, personal_filter, persona_filter_path):
        self.client = client
        self.model = "deepseek-chat"
        # self.model="qwen3-235b"
        self.personal_filter = personal_filter
        self.persona_filter_path = persona_filter_path

    def plan(self, user_raw_input, output_path, persona_dataset):
        """
        极简规划：只输出 template, sample_size, output_path
        """
        print(f"[Planner Agent] 正在解析用户指令...")
        # --- 新增判断逻辑 ---
        # 1.初筛角色库
        # 给每一行数据增加一个原始索引字段
        persona_filter_dataset = []
        if self.personal_filter is None or self.personal_filter.strip() == "":
            # 不进行检索，直接赋值
            persona_filter_dataset= persona_dataset
            os.makedirs(os.path.dirname(self.persona_filter_path), exist_ok=True)
            with open(self.persona_filter_path, "w", encoding="utf-8") as f:
                for p in persona_filter_dataset:
                    f.write(json.dumps(p, ensure_ascii=False) + "\n")
            # print(f"\n✅ 已保存：{out_path}")
            print(f"初筛共筛选出 {len(persona_filter_dataset)} 个角色")
        else:
            # 1.1 自动翻译得到 中英文关键词
            cn_key, en_key = get_bilingual_keywords(self.personal_filter, self.client)

            # 1.2 读取角色库
            # all_personas = load_personas(persona_dataset)

            # 1.3 同时用中英文检索
            final_roles = filter_by_both_keywords(persona_dataset, cn_key, en_key)

            # 1.4 保存
            save_result(final_roles, self.persona_filter_path)
            raw_data = load_dataset("json", data_files=self.persona_filter_path)['train']
            # persona_dataset = [item for item in raw_data]
            for i, item in enumerate(raw_data):
                item['_original_idx'] = i  # 记录它在原始文件里的行号
                persona_filter_dataset.append(item)

        # print(f"初筛后的角色库保存在：{self.persona_filter_path}")
        actual_count = len(persona_filter_dataset)


        # 2.分析用户需求并且产生提示词等指令
        # 关键修改：要求模型根据用户的“语气”和“要求”去重构提示词
        prompt = f"""
        你是一个顶级 AI 指令架构师。你的任务是将用户模糊的数据合成需求，转化为一个高度结构化的 JSON 配置指令。
        
        ### 当前环境信息:
        - 筛选后的可用角色总数 (actual_count): {actual_count}
        
        ### 用户原始需求:
        "{user_raw_input}"

        ### 输出 JSON 字段定义与要求:
        1. "template": (核心字段) 
           - 你需要将用户的需求重构为一段“基于人设的提问触发指令”。
           - **核心目标**：要求 LLM 代入 {{persona}} 身份，根据其职业背景提出一个**专业、具体且具有挑战性的真实问题**。
           - **占位符要求**：必须包含 `{{persona}}` 占位符。
           - **指令引导语建议**：
            - “请你代入以下角色：{{persona}}。基于你的职业背景和日常工作，请设计一个你真实会遇到的、极具专业深度的挑战性问题。”
            - “请直接输出问题内容，不要包含‘我的问题是’、‘好的，我提出了以下问题’等废话。”
            - “严禁输出解释性内容，只需要输出那个‘被提问’的指令本身。”
           - **扩写与强化**：如果用户要求“专业”，你必须在模板中显式加入“使用行业黑话/专业术语”、“严禁解释性废话”、“保持专业深度”等引导词。
           - **单样本导向**：注意！模板应写成针对“单个角色”的指令，不要在模板里写“请生成 X 条”，因为系统会循环调用它。
           - 要求模型在涉及专业术语时，必须采用中文的格式，严禁直接输出大段外语。

        2. "sample_size": 
           - 提取用户要求的样本总数。
           - 如果用户用汉字表明数量，也需要提取。
           - **关键逻辑**：
             - 如果用户提到“全部”、“所有”、“尽可能多”、“输出能搜到的所有”等，**你必须输出数字 {actual_count}**。
             - 如果用户提到具体的数字（如“100”或“一百”），请转化为整数。
             - 如果用户未指明数量，默认输出 5。
           - **注意：此字段必须为整数(int)，严禁输出字符串。**

        3. "output_path": 
           - 严格保持为 "{output_path}"，不得修改。

        4. "domain_expert": 
           - 根据需求识别该任务所属的专业领域（如：量化金融、法律合规、代码审计等），以便后续 Agent 注入专家知识。

        ### 约束条件:
        - 严禁复读用户的原始需求。
        - 确保生成的 `template` 逻辑严密，能够激发 {{persona}} 的职业特质。
        - 只输出 JSON 格式，不包含任何开场白或结尾说明。
        - 占位符融合：确保 {{persona}} 前后的衔接自然。
        - 标点清洗：要求生成的模板语法严密，严禁出现标点符号堆砌。
        """
        #
        messages = [
            HumanMessage(content=prompt)
        ]

        response = self.client.invoke(
            input=messages,
            # 保留 JSON 输出格式（和原来功能一样）
            extra_body={"response_format": {"type": "json_object"}}
        )

        # 获取结果（和原来 completion.choices[0].message.content 一样）
        result = response.content
        # response = self.client.chat.completions.create(
        #     model=self.model,  # 确保这里是 deepseek-chat
        #     messages=[{"role": "user", "content": prompt}],
        #     # 注意：DeepSeek 支持 json_object，但提示词里必须包含 "json" 字符
        #     response_format={"type": "json_object"}
        # )


        # 【关键修复】解析JSON（新版写法！！）
        # 提取```json 和 ```之间的内容（或直接提取{...}块）
        json_match = re.search(r'```json\s*({[\s\S]*?})\s*```', result)
        if json_match:
            json_str = json_match.group(1)
        else:
            # 兼容没有```json标记的情况，直接提取第一个{...}块
            json_match = re.search(r'({[\s\S]*})', result)
            if json_match:
                json_str = json_match.group(1)
            else:
                raise ValueError("未找到有效JSON内容")
        instruction_config = json.loads(json_str)  # 这里改对了！

        return instruction_config, persona_filter_dataset