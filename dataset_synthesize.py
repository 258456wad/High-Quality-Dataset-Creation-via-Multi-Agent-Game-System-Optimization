import argparse
import os
import json
from sympy.codegen.ast import none
import re
import numpy as np
from langchain_deepseek import ChatDeepSeek
from langchain_core.messages import HumanMessage, SystemMessage
from tenacity import retry, stop_after_attempt, wait_exponential

from prompt_templates import (
    instruction_template,
    knowledge_template,
    npc_template,
    math_template,
    finance_template,
    instruction_template_cn,# cn代表中文
    knowledge_template_cn,
    npc_template_cn,
    math_template_cn,
    finance_template_cn,
    stock_analysis_cn,
    trading_strategy_cn,
    stock_knowledge_cn,
    risk_assessment_cn,
    market_insight_cn,
    universal_gen_v2_cn
)
from datasets import load_dataset
from tqdm import tqdm

# 清洗掉think
def super_clean(text):
    if not text:
        return ""
    # 1. 核心清洗：移除 <think> ... </think> 及其内部所有内容
    # re.DOTALL 确保能匹配跨行的思考过程
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL | re.IGNORECASE)

    # 2. 辅助清洗：移除 Markdown 的代码块标签（如果模型自作聪明加了的话）
    text = re.sub(r'```[a-zA-Z]*\n?', '', text)
    text = text.replace('```', '')

    # 3. 移除多余的空行和首尾空格
    return text.strip()

# 修改为：
# client = OpenAI(
#     api_key="sk-81c79590bb1243a6bfddbd5d87a96ff0", # 建议运行完后妥善保管 Key
#     base_url="https://api.deepseek.com"
# )

# def get_response(user_prompt):
#     completion = client.chat.completions.create(
#         model="gpt-4o",
#         temperature=0.7,
#         messages=[
#             {"role": "system", "content":  f"{system_prompt}"},
#             {"role": "user", "content": f"{user_prompt}"}
#         ]
#     )
#     return completion.choices[0].message.content
# 加上这个装饰器
@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=10))
def get_response(client, user_prompt,system_prompt):
    # completion = client.chat.completions.create(
    #     model="deepseek-chat",  # 这里从 gpt-4o 改为 deepseek-chat
    #     temperature=0.7,
    #     messages=[
    #         {"role": "system", "content":  f"{system_prompt}"},
    #         {"role": "user", "content": f"{user_prompt}"}
    #     ]
    # )
    # return completion.choices[0].message.content
    # 构造消息（和原来逻辑完全一样，只是格式适配 LangChain）
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]

    # 调用方式改成 ChatDeepSeek 支持的格式
    completion = client.invoke(messages)

    return completion.content.strip()



# 翻译成中文
def translate_to_chinese(client, text: str) -> str:
    """Translate a given English text to Simplified Chinese."""
    # completion = client.chat.completions.create(
    #     model="deepseek-chat",
    #     temperature=0.3,
    #     messages=[
    #         {"role": "system", "content": "You are a professional translator specializing in translating English text to fluent Simplified Chinese."},
    #         {"role": "user", "content": f"Translate the following text to Simplified Chinese, preserving meaning and style, and do not add any extra commentary:\n\n{text}"}
    #     ]
    # )
    # return completion.choices[0].message.content.strip()
    # 完全保留你原来的提示词逻辑
    """智能翻译：英文→中文，中文直接返回"""
    # 判断是否包含中文字符
    def has_chinese(s):
        return re.search(r'[\u4e00-\u9fff]', s)

    # 如果已经是中文，直接返回，不翻译！
    if has_chinese(text):
        return text.strip()

    # 如果是英文，才走翻译流程
    messages = [
        SystemMessage(
            content="You are a professional translator specializing in translating English text to fluent Simplified Chinese."
        ),
        HumanMessage(
            content=f"Translate the following text to Simplified Chinese, preserving meaning and style, and do not add any extra commentary:\n\n{text}"
        )
    ]
    completion = client.invoke(messages)
    return completion.content.strip()


# 防止template是自定义的指令不能被使用，所以引入函数检测template是否是中文
def is_contains_chinese(objs):
    return re.search(r'[\u4e00-\u9fff]', objs)

# 专门清洗一遍数据，防止出现一些乱七八糟的格式错误
def clean_synthesized_content(text):
    """
    终极数据清洗：彻底解决标点重复、缺少句号、格式混乱问题
    """
    if not text:
        return ""


    # 1. 先统一：把所有连续的句号/逗号 变成 一个句号
    text = re.sub(r'[。！？；\.,;]{2,}', '。', text)

    # 2. 修复：角色背景：XXX任务指令 → 自动补句号
    text = re.sub(r'(角色背景：.*?[^。])(任务指令：)', r'\1。\2', text, flags=re.DOTALL)

    # 3. 再全局清理：所有重复标点 → 只留一个
    text = re.sub(r'([。，！？；])\1+', r'\1', text)

    # 4. 清除乱码
    text = "".join(ch for ch in text if ch.isprintable())

    # 5. 清除多余空格
    text = text.strip()

    # 6. 移除AI前缀废话
    patterns_to_remove = [
        r"^好的[，。]这是为您生成的.*[:：]",
        r"^根据您的要求[，。].*[:：]",
        r"^作为.*[，。]我为您生成了.*[:：]"
    ]
    for pattern in patterns_to_remove:
        text = re.sub(pattern, "", text, flags=re.MULTILINE)

    # 7.双句号替换成单句号
    text = text.replace("。。", "。")
    text = text.replace("，，", "，")

    # 8. 过滤非法或不可见乱码
    text = "".join(ch for ch in text if ch.isprintable() or ch in ['\n', '\r', '\t'])

    return text

def clean_persona_field(text):
    """
    标准化 persona：去掉末尾杂乱标点，统一加上中文句号。
    """
    if not text:
        return "。"
    # 1. 去掉首尾空格
    # 2. rstrip 去掉末尾所有的句号（中文和英文）、逗号、分号等
    # 3. 最后统一加上一个中文句号
    return text.strip().rstrip("。").rstrip(".").rstrip("，").rstrip(",") + "。"


def main(client, args, persona_dataset, system_prompt):
    # Load the appropriate template
    if args.template == "instruction":
        template = instruction_template
    elif args.template == "knowledge":
        template = knowledge_template
    elif args.template == "npc":
        template = npc_template
    elif args.template == "math":
        template = math_template
    elif args.template == "finance":
        template = finance_template
    elif args.template == "instruction_cn":
        template = instruction_template_cn
    elif args.template == "knowledge_cn":
        template = knowledge_template_cn
    elif args.template == "npc_cn":
        template = npc_template_cn
    elif args.template == "math_cn":
        template = math_template_cn
    elif args.template == "finance_cn":
        template = finance_template_cn
    elif args.template == "stock_analysis_cn":
        template = stock_analysis_cn
    elif args.template == "trading_strategy_cn":
        template = trading_strategy_cn
    elif args.template == "stock_knowledge_cn":
        template = stock_knowledge_cn
    elif args.template == "risk_assessment_cn":
        template = risk_assessment_cn
    elif args.template == "market_insight_cn":
        template = market_insight_cn
    elif args.template == "universal_gen_v2_cn":
        template = universal_gen_v2_cn
        # 核心修改点：
    elif args.template is not None and len(str(args.template).strip()) > 0:
        # 如果 args.template 既不是上面的代号，也不是空的，就直接把它当做 Prompt 模板内容
        template = args.template
        # print(f"[System] 检测到自定义动态指令，正在使用 Planner 生成的模板内容...")
    else:
        raise ValueError("Invalid template type. Choose from 'instruction', 'knowledge', 'npc', 'math', 'finance', 'instruction_cn', 'knowledge_cn', 'npc_cn', 'math_cn', 'finance_cn', 'stock_analysis_cn', 'stock_knowledge_cn', 'trading_strategy_cn', 'risk_assessment_cn', 'market_insight_cn'.")

    # Load the dataset
    # 这里应该也可以改成其他的jsonl文件看看
    # persona_dataset = load_dataset("proj-persona/PersonaHub", data_files="persona.jsonl")['train']
    # 需要根据不同的情况修改jsonl输入的文件
    # print(f"接收到 Agent 派发的 {len(persona_dataset)} 个角色进行生成.")
    # persona_dataset = load_dataset("json", data_files=data_path)['train'] #改成本地文件
    if args.sample_size > 0:
        # 增加这一行：随机打乱，seed=42 是为了让你以后能复现同样的随机结果
        # persona_dataset = persona_dataset.shuffle(seed=42).select(range(args.sample_size))
        # 不再随机挑选，直接选择
        persona_dataset = persona_dataset[:args.sample_size]
    # print(f"Total number of input personas: {len(persona_dataset['input persona'])}")

    # If using a Chinese template, translate personas to Chinese first
    persona_cache = {}
    with open(args.output_path, "a", encoding='utf-8') as out:
        # --- 修改点 1: 直接遍历列表对象 ---
        for item in tqdm(persona_dataset, desc="正在生成数据"):
        # for persona in tqdm(persona_dataset['input persona']):
        #     persona = persona.strip()
        # --- 修改点 2: 从字典 item 中提取具体的人设文本 ---
            persona = item['input persona'].strip()
            if args.template.endswith("_cn"):
                # Avoid translating duplicates
                if persona not in persona_cache:
                    persona_cache[persona] = translate_to_chinese(client, persona)
                persona = persona_cache[persona]

            # 如果template有中文，也需要进行personal合成，这种方法专门用来针对自定义动态指令
            elif is_contains_chinese(template):
                if persona not in persona_cache:
                    persona_cache[persona] = translate_to_chinese(client, persona)
                persona = persona_cache[persona]

            cleaned_persona = clean_persona_field(persona)  # 这里的 cleaned_persona 是干净的词段
            # --- 第一步：根据人设生成【问题/指令】 ---
            # 建议在 template 中明确告诉模型：“请仅输出一个专业的问题，不要输出多余的解释”
            question_generation_prompt = template.format(persona=cleaned_persona)
            raw_question = get_response(client, question_generation_prompt, system_prompt)
            # 清洗提取出的问题
            extracted_question_1 = super_clean(raw_question)
            extracted_question = clean_synthesized_content(extracted_question_1)
            # --- 第二步：根据生成的【问题】生成【专业回答】 ---
            # 定义一个专门用于回答的系统提示词（或者直接在 user_prompt 里写）
            answer_system_prompt = f"请针对提出的问题{extracted_question}，给出专业、深度、符合身份背景的回答。"
            # 这里的 get_response 可以再次调用
            raw_answer = get_response(client, extracted_question, answer_system_prompt)
            # 清洗回答
            cleaned_answer = clean_synthesized_content(raw_answer)

            # user_prompt = template.format(persona=cleaned_persona)
            # cleaned_prompt = clean_synthesized_content(user_prompt)
            # gpt4o_out_text = get_response(client, cleaned_prompt, system_prompt)
            # # --- 关键改进点：写入前的清洗 ---
            # # cleaned_prompt = clean_synthesized_content(user_prompt)
            # cleaned_response = clean_synthesized_content(gpt4o_out_text)

            # o = {"prompt": cleaned_prompt, "response": cleaned_response, "persona": cleaned_persona}
            o = {"prompt": extracted_question, "response": cleaned_answer}

            out.write(json.dumps(o, ensure_ascii=False) + '\n')

    # print(f"Outputted the results to: {args.output_path}")


# 1. 新增一个 main_all 函数，作为外部调用的统一入口
def main_all(client, template, sample_size, output_path, persona_dataset, system_prompt):
    """
    这个函数模拟了命令行参数的输入，直接调用原本的 main 逻辑。
    """

    # 模拟一个 args 对象，使其具备原本 argparse 解析出来的属性
    class Args:
        def __init__(self, template, sample_size, output_path):
            self.template = template
            self.sample_size = sample_size
            self.output_path = output_path

    args = Args(template, sample_size, output_path)

    # 直接调用你原本代码中定义的 main(args) 函数
    # 这样你不需要改动 main 函数内部的任何逻辑
    main(client, args, persona_dataset, system_prompt)







# """
# 分割线，下面是单独使用的流程，不用的话直接注释掉--------------------------------------------------------------------------------------------
# """
# persona_dataset_path="data/persona_short_user.jsonl"# 记得修改输入的路径
# output_path="output_data/persona_short_user.jsonl"# 记得修改输出的路径
# sample_size=5
# print(f"数据源: {persona_dataset_path}")
# print(f"输出位置: {output_path}")
# # 2.1 在启动所有任务前，先清空目标文件（如果文件存在）
# if os.path.exists(output_path):
#     with open(output_path, 'w', encoding='utf-8') as f:
#         f.truncate(0)  # 清空文件内容
#     print(f"--- 已初始化：清空旧数据 {output_path} ---")
# else:
#     # 确保目录存在
#     os.makedirs(os.path.dirname(output_path), exist_ok=True)
#
# system_prompt = '''You are a helpful assistant.'''
# raw_data = load_dataset("json", data_files=persona_dataset_path)['train']
# persona_dataset = []
# for i, item in enumerate(raw_data):
#     item['_original_idx'] = i  # 记录它在原始文件里的行号
#     persona_dataset.append(item)
#
# # client = OpenAI(api_key="sk-81c79590bb1243a6bfddbd5d87a96ff0", base_url="https://api.deepseek.com")
# # 本机电脑api
# api_key=os.environ.get("DEEPSEEK_API_KEY","sk-81c79590bb1243a6bfddbd5d87a96ff0")
# api_base=os.environ.get("DEEPSEEK_API_BASE") or os.environ.get("DEEPSEEK_API_BASE_URL")
# client = ChatDeepSeek(
#     model="deepseek-chat",
#     api_key=api_key,
#     api_base="https://api.deepseek.com",
#     temperature=0.1
# )
# # 中证环境api
# # api_key=os.environ.get("DEEPSEEK_API_KEY","sk-92771ee89bb145879c210aa4030e3a99")
# # api_base=os.environ.get("DEEPSEEK_API_BASE") or os.environ.get("DEEPSEEK_API_BASE_URL")
# # client = ChatDeepSeek(
# #     model="qwen3-235b",
# #     api_key=api_key,
# #     api_base="http://10.131.100.60:1025/v1",
# #     temperature=0.1
# # )
#
# persona_pool = persona_dataset  # 总库
# weights = np.ones(len(persona_dataset))
# used_indices = set()  # 已经用过的索引
# now_pool = list(persona_dataset)  # 初始化现有的库
# # 1. 检查现有库是否足够
# if len(now_pool) < sample_size:
#     print(f"警告：可用人设不足！剩余 {len(now_pool)}，请求 {sample_size}")
#     sample_size = len(now_pool)
#
# # 2. 从“现有库”的当前长度里随机抽取下标
# # 注意：这里我们只针对 now_pool 进行操作，提取下标
# current_indices_in_now_pool = np.random.choice(len(now_pool), size=sample_size, replace=False)
#
# # 3. 提取出本轮要用的“子集”数据，提取数据
# sub_persona_dataset = [now_pool[i] for i in current_indices_in_now_pool]
# current_original_indices = [item['_original_idx'] for item in sub_persona_dataset]
#
# # 4. 【核心动作】更新现有库：把选中的人设从 now_pool 中删掉
# # 使用 set 查找下标速度更快，删掉选中的数据
# indices_set = set(current_indices_in_now_pool)
# now_pool = [item for idx, item in enumerate(now_pool) if idx not in indices_set]
# used_indices.update(current_original_indices)
#
# # 5. 更新累计消耗记录（用于汇报）
# # 累计消耗 = 总库长度 - 剩余长度
# total_used = len(persona_pool) - len(now_pool)
# print(f"本轮消耗 {len(sub_persona_dataset)} 个角色。现有库剩余可用: {len(now_pool)}")
# print(f"当前累计已消耗角色总数: {total_used},对比看used计算的当前累计已消耗角色总数: {len(used_indices)}")
# print(f"累计索引的角色ID：{used_indices}")
# main_all(
#             client=client,
#             template="universal_gen_v2_cn",
#             sample_size=sample_size,
#             output_path=output_path,
#             persona_dataset=sub_persona_dataset,
#             system_prompt=system_prompt
#         )


