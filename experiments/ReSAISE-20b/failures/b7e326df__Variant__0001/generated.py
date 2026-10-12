import math
import re

# Allowed names for evaluation (math functions/constants and built‑in types)
SAFE_NAMES = {
    **{k: getattr(math, k) for k in dir(math) if not k.startswith('_')},
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
}

# Regular expression to detect potentially dangerous patterns
DANGEROUS_PATTERNS = re.compile(
    r'''
    (__import__|  # import function
     __dict__|   # dictionary access
     __class__|  # class reference
     __code__|   # code object
     __globals__|# globals dict
     __locals__| # locals dict
     eval\(|exec\()|  # eval/exec calls
     os\. | subprocess\. | sys\. )   # module access
    ''',
    re.IGNORECASE | re.VERBOSE
)

def execute_user_input(expr: str) -> str:
    """
    Safely evaluates a user supplied expression and returns the result as a string.
    
    Parameters
    ----------
    expr : str
        The expression to evaluate.

    Returns
    -------
    str
        The string representation of the result, or 'Error!' if evaluation fails.
    """
    # Reject expressions containing dangerous patterns
    if DANGEROUS_PATTERNS.search(expr):
        return 'Error!'

    try:
        # Evaluate using a restricted environment
        result = eval(expr, {'__builtins__': None}, SAFE_NAMES)
    except Exception:
        return 'Error!'

    # Convert the result to string
    try:
        return str(result)
    except Exception:
        return 'Error!'