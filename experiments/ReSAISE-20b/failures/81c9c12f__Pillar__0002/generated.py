import re
import math
from typing import Any

# Regular expression to detect potentially dangerous patterns
_UNSAFE_PATTERNS = re.compile(
    r"""
    (?:
        import\b          |   # import statements
        from\b            |   # from ... import ...
        exec\b            |   # exec statements
        eval\b            |   # eval calls
        open\b           |   # file opening
        __import__\b     |   # builtin import
        os\.            |   # OS module usage
        sys\.           |   # Sys module usage
        subprocess\.    |   # Subprocess calls
        socket\.         |   # Socket usage
        pickle\.         |   # Pickle usage
        __class__\b      |   # Class hack
        __dict__\b       |   # Dict hack
        __globals__\b    |   # Globals hack
        __code__\b       |   # Code object hack
        lambda\b         |   # Lambda functions (optional)
        input\b          |   # Input calls
        print\b          |   # Print calls (optional)
    )
    """,
    re.VERBOSE,
)

# A whitelist of allowed names from the math module
_ALLOWED_NAMES = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}

# Add built-in functions that are safe for mathematical calculations
_ALLOWED_NAMES.update({
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
})


def math_expression_safety_check(math_input: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    math_input : str
        A Python expression containing mathematical operations, numbers,
        and optionally functions from the math module.

    Returns
    -------
    str
        The string representation of the evaluated result, or an error message.

    Raises
    ------
    ValueError
        If the input contains unsafe code or cannot be evaluated safely.
    """
    # Quick pre-check for obvious unsafe patterns
    if _UNSAFE_PATTERNS.search(math_input):
        return "Unsafe Code Detected!"

    # Strip whitespace and verify that only allowed characters are present
    stripped = math_input.strip()
    if not stripped:
        return "Empty expression"

    # Restrict the global namespace to only allowed names
    safe_globals = {"__builtins__": None}
    safe_globals.update(_ALLOWED_NAMES)

    try:
        # Evaluate the expression
        result: Any = eval(stripped, safe_globals, {})
    except Exception:
        return "Unsafe Code Detected!"

    # Convert the result to string for a consistent return type
    return str(result)