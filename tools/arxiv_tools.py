from langchain_community.tools import ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper
from langchain_core.tools import tool

@tool
def search_arxiv(query: str) -> str:
    """
    Searches arXiv for scientific papers based on the query.
    Returns abstracts and metadata of relevant papers.
    """
    arxiv_wrapper = ArxivAPIWrapper(top_k_results=5, doc_content_chars_max=2000)
    tool = ArxivQueryRun(api_wrapper=arxiv_wrapper)
    return tool.run(query)

