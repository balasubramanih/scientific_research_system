import re
from google.adk.tools.function_tool import FunctionTool

def extract_code_blocks(text: str):
    """
    Extracts Python code blocks from text using Regex.
    Looks for markdown style code blocks ```python ... ``` or just ``` ... ```.
    """
    # Regex for code blocks
    # Matches ```python code ``` or ``` code ```
    pattern = r"```(?:python)?(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    return [m.strip() for m in matches]

def validate_python_env(dependencies: list[str]):
    """
    Mocks validation of Python dependencies.
    Returns True if dependencies are compatible, False otherwise.
    """
    # Simple mock logic: Fail if conflicting libraries are present
    deps_str = " ".join(dependencies).lower()
    
    if "tensorflow" in deps_str and "pytorch" in deps_str:
        return {"valid": False, "error": "Potential conflict: TensorFlow and PyTorch in same environment."}
    
    if "numpy" in deps_str and "pandas" in deps_str:
        return {"valid": True, "message": "Standard data stack detected."}
        
    return {"valid": True, "message": "Dependencies appear compatible."}

# ADK Tools
extract_code_tool = FunctionTool(
    func=extract_code_blocks
)

validate_env_tool = FunctionTool(
    func=validate_python_env
)

