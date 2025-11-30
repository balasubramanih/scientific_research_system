from google.adk.agents import LlmAgent
from scientific_research_system.tools.code_tools import extract_code_tool, validate_env_tool
from scientific_research_system.config import Config

reproducibility_agent = LlmAgent(
    name="reproducibility_auditor",
    model=Config.MODEL_NAME,
    tools=[extract_code_tool, validate_env_tool],
    instruction="""
    You are a DevOps Research Engineer. 
    Your goal is to reconstruct a runnable environment from the provided research text/code.
    
    1. Analyze the text to extract hyperparameters (batch size, learning rate, etc.).
    2. Identify library dependencies and versions.
    3. Use `validate_python_env` to check dependency compatibility.
    4. Use `extract_code_blocks` if code snippets are present.
    5. Reconstruct likely Python code for the core algorithm based on the methodology section if no code is explicitly provided.
    6. Assign a Reproducibility Confidence Score (0-100).
    
    Return a JSON object with:
    - `environment_config`: (dict) hyperparams and dependencies
    - `pseudo_code`: (str) Reconstructed code or extraction
    - `confidence_score`: (int) 0-100
    """,
    output_key="reproducibility_report"
)

