prompt_dict = {

    "review": """
        # 审核暂时不接入 llm
        是 agent 的第一入口
    """,

    "long-term_history": """
        # 这个是长期历史记录的提示词
        是 agent 的第二入口
    """,

    "short-term_history": """
        # 这个是短期历史记录的提示词
        是 agent 的第三入口
    """,

    "is_character": """
        # 这个是判断是否是人物的提示词
        是 agent 的第二步
    """,

    "rag_compress": """
        # 这个是大量 rag 压缩的提示词
        是 agent 的第三步
    """,

    "summary_tool_information": """
        # 这个是总结信息的提示词
        是 agent 的第四步
    """,

    "is_fit_character": """
        # 这个是判断是否符合人物的提示词
        是 agent 的第五步
    """,

    "summary": """
        # 这个是汇总的提示词
        是 agent 的出口
    """
}

