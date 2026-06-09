import json
import re
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_deepseek import ChatDeepSeek
import os
# ======================
# 你的 AI 客户端（不变）
# ======================

# ======================
# 你原来的翻译函数（完全保留）
# ======================
def clean_translation_output(raw_response: str) -> str:
    # 第一步：判断是否包含 think 标签
    if "<think" in raw_response.lower():
        # 有 think → 只删除 ... 整块
        cleaned = re.sub(r'<think.*?</think>', '', raw_response, flags=re.DOTALL | re.IGNORECASE)
        # 清理空白，返回结果
        return cleaned.strip()
    # 第二步：没有 think → 直接原封不动返回，不做任何处理
    return raw_response.strip()

def translate_to_chinese(text: str, client) -> str:
    """英文 → 中文"""
    if re.search(r'[\u4e00-\u9fff]', text):
        return text.strip()

    messages = [
        SystemMessage(content="You are a professional translator. Translate English to fluent Simplified Chinese only."),
        HumanMessage(content=f"Translate the following text to Simplified Chinese, preserving meaning and style, and do not add any extra commentary:\n\n{text}")
    ]
    completion = client.invoke(messages)
    cleaned_content = clean_translation_output(completion.content)
    return cleaned_content.strip()


def translate_to_english(text: str, client) -> str:
    """中文 → 英文（专门给关键词翻译用）"""
    messages = [
        SystemMessage(content="Translate Chinese to fluent, professional English. Only output the translation."),
        HumanMessage(content=f"Translate to English:\n{text}")
    ]
    completion = client.invoke(messages)
    cleaned_content = clean_translation_output(completion.content)
    cleaned_content = cleaned_content.lower()
    return cleaned_content.strip()

# ======================
# 核心：输入任意词 → 自动得到 中英文两个关键词
# ======================
def get_bilingual_keywords(user_input, client):
    """
    输入任意词 → 返回 [中文关键词，英文关键词]
    """
    user_input = user_input.strip()
    is_chinese = re.search(r'[\u4e00-\u9fff]', user_input) is not None

    if is_chinese:
        # 中文 → 翻译出英文
        cn_key = user_input
        en_key = translate_to_english(user_input, client)
    else:
        # 英文 → 翻译出中文
        en_key = user_input.lower()
        cn_key = translate_to_chinese(user_input, client)

    # print(f"翻译完成：中文 = {cn_key}，英文 = {en_key}")
    return [cn_key.strip(), en_key.strip()]

# ======================
# 读取 & 过滤
# ======================
# def load_personas(file_path="data/persona.jsonl"):
#     data = []
#     with open(file_path, "r", encoding="utf-8") as f:
#         for line in f:
#             data.append(json.loads(line.strip()))
#     return data

def filter_by_both_keywords(personas, cn_key, en_key):
    """同时用中英文检索"""
    result = []
    for p in personas:
        text = p["input persona"]
        text_lower = text.lower()

        # 只要命中一个就保留
        if cn_key in text or en_key in text_lower:
            result.append(p)
    return result

def save_result(personas, out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        for p in personas:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    # print(f"\n✅ 已保存：{out_path}")
    print(f"初筛共筛选出 {len(personas)} 个角色")

# # ======================
# # 主程序
# # ======================
# if __name__ == "__main__":
#     print("🔍 请输入任意关键词（中文/英文均可）：")
#     user_input = input("> ")
#
#     # 1. 自动翻译得到 中英文关键词
#     cn_key, en_key = get_bilingual_keywords(user_input)
#
#     # 2. 读取角色库
#     all_personas = load_personas()
#
#     # 3. 同时用中英文检索
#     final_roles = filter_by_both_keywords(all_personas, cn_key, en_key)
#
#     # 4. 保存
#     save_result(final_roles)
#
#     # 5. 展示结果
#     print("\n📌 匹配到的角色：")
#     for i, p in enumerate(final_roles, 1):
#         print(f"{i}. {p['input persona']}")