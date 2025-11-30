from google.adk.agents import LlmAgent
from scientific_research_system.tools.citation_tools import fetch_citation_tool, detect_anomaly_tool
from scientific_research_system.config import Config

citation_auditor_agent = LlmAgent(
    name="citation_auditor",
    model=Config.MODEL_NAME,
    tools=[fetch_citation_tool, detect_anomaly_tool],
    instruction="""
    You are a Citation Integrity Specialist.
    
    Your goal is to analyze the citation list for temporal anomalies (citations post-dating the paper) and hallucination patterns.
    
    1. Use `fetch_citation_metadata` to get citations for the paper (assume paper_id is 'current_paper').
    2. Use `detect_temporal_anomaly` with the paper's publication date (assume today's date or '2023-10-01' if not specified).
    3. Calculate a Citation Integrity Score (0-100) based on the percentage of valid citations.
    
    Return a JSON object with:
    - `score`: (int) 0-100
    - `flagged_citations`: (list) List of suspicious citations
    - `audit_report`: (str) Brief analysis of findings
    """,
    output_key="citation_audit"
)

