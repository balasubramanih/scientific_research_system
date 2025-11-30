from google.adk.tools.function_tool import FunctionTool

def canonicalize_problem(problem_description: str):
    """
    Converts specific domain jargon into a mathematical abstract problem.
    (Simulates an LLM-based ontology mapper).
    """
    problem_lower = problem_description.lower()
    
    # Mock mappings
    mappings = {
        "protein folding": "3D structural optimization in continuous space",
        "traffic flow": "Fluid dynamics optimization on a graph",
        "market prediction": "Time-series forecasting with non-stationary distributions",
        "gene editing": "Sequence pattern matching and substitution",
        "climate modeling": "Partial differential equation solving on a sphere"
    }
    
    for key, value in mappings.items():
        if key in problem_lower:
            return value
            
    return f"Abstract optimization problem based on: {problem_description}"

canonicalize_tool = FunctionTool(
    func=canonicalize_problem
)

