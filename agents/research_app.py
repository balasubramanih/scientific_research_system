from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.tools.function_tool import FunctionTool
from scientific_research_system.tools.arxiv_tools import search_arxiv
from scientific_research_system.tools.search_tools import web_search
from scientific_research_system.config import Config

# Import new agents
from scientific_research_system.agents.citation_auditor import citation_auditor_agent
from scientific_research_system.agents.reproducibility_agent import reproducibility_agent
from scientific_research_system.agents.domain_bridge import domain_bridge_agent
from scientific_research_system.agents.negative_results import negative_results_agent
from scientific_research_system.agents.fraud_detector import fraud_detector_agent

# Wrap tools manually
def arxiv_search_func(query: str):
    return search_arxiv.run(query)

def web_search_func(query: str):
    return web_search.run(query)

def create_research_system(execution_mode: str = "sequential"):
    """
    Creates the autonomous research system using Google ADK.
    
    Args:
        execution_mode (str): "parallel" for faster execution, "sequential" for rate-limited environments.
    
    Structure:
    1. Query Formulation
    2. Literature Mining (Parallel/Sequential)
    3. Quality Control (Parallel/Sequential)
    4. Knowledge Graph Construction
    5. Gap Analysis
    6. Innovation Stage (Parallel/Sequential)
    7. Hypothesis Generation
    8. Writing
    9. Evaluation
    """
    
    # Determine Agent Class based on mode
    StageAgent = ParallelAgent if execution_mode == "parallel" else SequentialAgent
    
    # 1. Query Formulation Agent
    query_agent = LlmAgent(
        name="query_formulation",
        model=Config.MODEL_NAME,
        instruction="""
        You are a research expert. 
        Generate 3 specific, academic search queries for the given research topic.
        Focus on finding recent reviews, key methodologies, and core concepts.
        Return the queries as a comma-separated list string.
        """,
        output_key="queries"
    )

    # 2. Mining Agents (Parallel)
    
    # Arxiv Agent
    arxiv_agent = LlmAgent(
        name="arxiv_mining",
        model=Config.MODEL_NAME,
        tools=[FunctionTool(arxiv_search_func)],
        instruction="""
        You are a specialist in academic paper mining.
        The research queries are: {queries}
        
        For each query, use the `arxiv_search_func` tool to find relevant papers.
        Summarize the key findings, methods, and abstracts from the papers you find.
        Return a consolidated summary of arXiv papers.
        """,
        output_key="arxiv_results"
    )

    # Web Search Agent
    web_agent = LlmAgent(
        name="web_mining",
        model=Config.MODEL_NAME,
        tools=[FunctionTool(web_search_func)],
        instruction="""
        You are a specialist in web research.
        The research queries are: {queries}
        
        For each query, use the `web_search_func` tool to find relevant articles, blog posts, or simplified explanations.
        Summarize the key information found on the web.
        Return a consolidated summary of web resources.
        """,
        output_key="web_results"
    )

    mining_stage = StageAgent(
        name="literature_mining",
        sub_agents=[arxiv_agent, web_agent]
    )

    # 3. Quality Control Stage (Parallel/Sequential)
    quality_control_stage = StageAgent(
        name="quality_control_stage",
        sub_agents=[citation_auditor_agent, fraud_detector_agent, reproducibility_agent]
    )

    # 4. Knowledge Graph Agent
    kg_agent = LlmAgent(
        name="knowledge_graph",
        model=Config.MODEL_NAME,
        instruction="""
        You are a Knowledge Graph specialist.
        
        Analyze the gathered information:
        ArXiv Findings: {arxiv_results}
        Web Findings: {web_results}
        
        Extract key concepts, authors, and findings.
        Return a JSON object with 'entities' (list of strings) and 'relationships' (list of strings describing connections).
        """,
        output_key="knowledge_graph"
    )

    # 5. Gap Analysis Agent
    gap_agent = LlmAgent(
        name="gap_analysis",
        model=Config.MODEL_NAME,
        instruction="""
        You are a Senior Researcher.
        
        Analyze the existing literature and the knowledge graph concepts.
        Knowledge Graph: {knowledge_graph}
        Literature Context: {arxiv_results}
        
        Identify 3 major research gaps, contradictions, or underexplored areas.
        Return a list of gaps.
        """,
        output_key="gaps"
    )

    # 6. Innovation Stage (Parallel/Sequential)
    innovation_stage = StageAgent(
        name="innovation_stage",
        sub_agents=[domain_bridge_agent, negative_results_agent]
    )

    # 7. Hypothesis Generation Agent
    hypothesis_agent = LlmAgent(
        name="hypothesis_generation",
        model=Config.MODEL_NAME,
        instruction="""
        You are a Creative Scientist.
        
        Based on the identified gaps: {gaps}
        And insights from the Innovation Stage (if available in the conversation history):
        
        Propose 3 novel research hypotheses and experimental designs.
        Be specific about methodology.
        """,
        output_key="hypotheses"
    )

    # 8. Writer Agent
    writer_agent = LlmAgent(
        name="writing",
        model=Config.MODEL_NAME,
        instruction="""
        You are a Scientific Writer.
        
        Write a comprehensive literature review section.
        Incorporating:
        1. Findings from literature: {arxiv_results}
        2. Identified Gaps: {gaps}
        3. Proposed Hypotheses: {hypotheses}
        4. Quality Control Audits (if available)
        5. Innovation Insights (if available)
        
        Cite sources where possible (referring to the provided findings).
        Format in Markdown.
        """,
        output_key="draft"
    )

    # 9. Evaluation Agent
    eval_agent = LlmAgent(
        name="evaluation",
        model=Config.MODEL_NAME,
        instruction="""
        You are a Research Review Board.
        
        Evaluate the provided research draft and hypotheses.
        Draft: {draft}
        Hypotheses: {hypotheses}
        
        Review the specific Quality Control and Innovation metrics included in the draft.
        
        Rate them on:
        - Novelty (1-10)
        - Feasibility (1-10)
        - Clarity (1-10)
        - Integrity Score (Average of Citation/Fraud/Reproducibility audits)
        - Cross-Domain Potential
        
        Provide a brief critique.
        Appended the evaluation to the end of the draft text.
        """,
        output_key="final_report"
    )

    # Main Workflow
    workflow = SequentialAgent(
        name="research_workflow",
        sub_agents=[
            query_agent,
            mining_stage,
            quality_control_stage,
            kg_agent,
            gap_agent,
            innovation_stage,
            hypothesis_agent,
            writer_agent,
            eval_agent
        ]
    )
    
    return workflow
