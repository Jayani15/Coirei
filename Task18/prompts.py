SUMMARIZE_PROMPT = """
Summarize the following news article in 3 concise bullet points:

{text}
"""

CATEGORY_PROMPT = """
Classify the following news summary into ONE category:
Technology, Business, Sports, Politics, Health, Entertainment

Summary:
{text}

Answer with ONLY the category name.
"""