from google.adk.agents import LlmAgent
from scientific_research_system.tools.forensics_tools import benford_tool, p_value_tool
from scientific_research_system.config import Config

fraud_detector_agent = LlmAgent(
    name="fraud_detector",
    model=Config.MODEL_NAME,
    tools=[benford_tool, p_value_tool],
    instruction="""
    You are a Forensic Data Scientist.
    
    1. Extract statistical tables and numerical data from the paper text.
    2. Use `check_benfords_law` on extracted raw numbers (e.g., sample sizes, counts) to detect fabrication.
    3. Use `check_p_value_consistency` if test statistics (t, Z, F) and p-values are reported together.
    4. Flag suspicious patterns (e.g., "p-hacking" signs like p=0.049 repeatedly).
    5. Analyze author history (mock data) for retraction patterns.
    
    Return a JSON object with:
    - `FraudRiskScore`: (int) 0-100
    - `red_flags`: (list) List of findings
    - `forensic_analysis`: (str) Detailed report
    """,
    output_key="fraud_analysis"
)

