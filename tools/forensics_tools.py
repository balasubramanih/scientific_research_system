import math
from google.adk.tools.function_tool import FunctionTool

def check_benfords_law(numbers: list[float]):
    """
    Checks if a list of numbers follows Benford's Law (first digit distribution).
    Returns a risk score (0-100) indicating deviation.
    """
    if not numbers:
        return {"risk_score": 0, "message": "No data provided."}
        
    # Extract first digits
    first_digits = []
    for n in numbers:
        try:
            s = str(float(n)).replace('.', '').lstrip('0')
            if s:
                first_digits.append(int(s[0]))
        except ValueError:
            continue
            
    if not first_digits:
         return {"risk_score": 0, "message": "No valid numbers found."}

    total = len(first_digits)
    counts = {d: first_digits.count(d) for d in range(1, 10)}
    
    # Theoretical Benford probabilities
    benford_probs = {d: math.log10(1 + 1/d) for d in range(1, 10)}
    
    # Calculate Chi-square like deviation
    deviation_sum = 0
    for d in range(1, 10):
        observed = counts[d] / total
        expected = benford_probs[d]
        deviation_sum += abs(observed - expected)
        
    # Normalize deviation to a score (simplified)
    # Max possible deviation sum is around 1.0-ish roughly. 
    # Let's say > 0.3 is suspicious.
    risk_score = min(100, int(deviation_sum * 200))
    
    return {
        "risk_score": risk_score,
        "distribution": counts,
        "message": "High deviation detected" if risk_score > 50 else "Natural distribution"
    }

def check_p_value_consistency(stat: float, p_val: float, sample_size: int = 100):
    """
    Checks consistency between a test statistic (Z/t) and P-value.
    Assumes two-tailed Z-test for simplicity if not specified.
    """
    try:
        import scipy.stats as stats
        
        # Calculate expected p-value from stat (assuming Z-test for simplicity)
        # Two-tailed
        expected_p = 2 * (1 - stats.norm.cdf(abs(stat)))
        
        difference = abs(expected_p - p_val)
        
        # Allow some floating point or rounding margin (e.g., reported p < 0.05)
        consistent = difference < 0.05
        
        return {
            "consistent": consistent,
            "reported_p": p_val,
            "calculated_p": round(expected_p, 4),
            "difference": difference
        }
        
    except ImportError:
        return {"error": "scipy not installed, cannot calculate exact p-values."}
    except Exception as e:
        return {"error": str(e)}

# ADK Tools
benford_tool = FunctionTool(
    func=check_benfords_law
)

p_value_tool = FunctionTool(
    func=check_p_value_consistency
)

