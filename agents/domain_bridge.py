from google.adk.agents import LlmAgent
from scientific_research_system.tools.ontology_tools import canonicalize_tool
from scientific_research_system.config import Config

domain_bridge_agent = LlmAgent(
    name="domain_bridge",
    model=Config.MODEL_NAME,
    tools=[canonicalize_tool],
    instruction="""
    You are a Lateral Innovation Expert.
    
    1. Take the specific research problem or topic (from context or input).
    2. Canonicalize it using `canonicalize_problem`.
    3. Search for *solution patterns* in completely different fields (e.g., if Biology, look in Physics/Finance).
    4. Propose a transferability plan: how to apply the foreign solution to the current problem.
    
    Return a JSON object with:
    - `source_domain`: (str) The original field
    - `target_solutions`: (list) Solutions from other fields
    - `transfer_feasibility_score`: (int) 0-100
    """,
    output_key="innovation_bridge"
)

