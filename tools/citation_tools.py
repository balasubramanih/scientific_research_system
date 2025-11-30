import datetime
from google.adk.tools.function_tool import FunctionTool

def fetch_citation_metadata(paper_id: str):
    """
    Mocks fetching citation metadata for a given paper ID.
    Returns a list of citations with publication dates.
    """
    # Mock data: Simulating a paper published in 2023
    # We include some citations that are "from the future" (time travel paradox)
    
    citations = [
        {"title": "Foundations of Multi-Agent Systems", "paper_id": "cit_001", "publication_date": "2022-01-15"},
        {"title": "Advanced Graph Neural Networks", "paper_id": "cit_002", "publication_date": "2023-05-20"},
        {"title": "Future of AI: 2025 Outlook", "paper_id": "cit_003", "publication_date": "2025-11-10"}, # Anomaly
        {"title": "Quantum Computing in 2024", "paper_id": "cit_004", "publication_date": "2024-02-28"}, # Anomaly
        {"title": "Legacy Algorithms", "paper_id": "cit_005", "publication_date": "2020-08-01"}
    ]
    return citations

def detect_temporal_anomaly(paper_date_str: str, citations: list[dict]):
    """
    Detects citations that were published after the source paper.
    paper_date_str format: YYYY-MM-DD
    """
    anomalies = []
    try:
        paper_date = datetime.datetime.strptime(paper_date_str, "%Y-%m-%d").date()
        
        for cit in citations:
            cit_date_str = cit.get("publication_date")
            if cit_date_str:
                cit_date = datetime.datetime.strptime(cit_date_str, "%Y-%m-%d").date()
                if cit_date > paper_date:
                    anomalies.append(cit)
                    
    except ValueError as e:
        return [f"Error parsing dates: {e}"]
        
    return anomalies

# ADK Tool Wrappers
# Note: FunctionTool in this ADK version infers name/description from the function itself (docstring/name).
fetch_citation_tool = FunctionTool(
    func=fetch_citation_metadata
)

detect_anomaly_tool = FunctionTool(
    func=detect_temporal_anomaly
)

