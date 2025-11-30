from google.adk.agents import LlmAgent
from scientific_research_system.config import Config

negative_results_agent = LlmAgent(
    name="negative_results_analyst",
    model=Config.MODEL_NAME,
    instruction="""
    You are a Failure Analyst.
    
    Scan the provided papers and context for language indicating failure (e.g., 'failed to converge', 'no significant improvement', 'contrary to hypothesis').
    
    1. Extract the specific hypothesis that failed.
    2. Categorize *why* it failed (data issue, theoretical flaw, computational limit, etc.).
    3. Create a registry entry for this 'Dead End'.
    
    Return a JSON object with a list of `falsified_hypotheses`. Each entry should have:
    - `hypothesis`: description
    - `reason`: failure reason
    - `source`: paper/source reference
    """,
    output_key="negative_results"
)

