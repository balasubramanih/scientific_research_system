from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

@tool
def web_search(query: str) -> str:
    """
    Performs a web search to find general scientific information, blog posts, or simplified explanations.
    Useful for broad context or finding recent developments not yet on arXiv.
    """
    search = DuckDuckGoSearchRun()
    return search.run(query)

