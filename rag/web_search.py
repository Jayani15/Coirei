import os
from tavily import TavilyClient

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)

def web_search(query):

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=3
    )

    context = ""

    sources = []

    for result in response["results"]:

        context += result["content"] + "\n\n"

        sources.append(result["url"])

    return context, sources