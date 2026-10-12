import re

# Regular expression that matches a set of potentially dangerous keywords or patterns.
# The pattern is case‑insensitive and uses word boundaries to avoid false positives
# in legitimate identifiers.
DANGEROUS_PATTERNS = re.compile(
    r"""
    (?:
        import\b          |  # importing modules
        exec\b            |  # executing code
        eval\b            |  # evaluating code
        open\b            |  # opening files
        __import__\b      |  # dynamic import
        os\b              |  # os module usage
        sys\b             |  # sys module usage
        subprocess\b      |  # subprocess usage
        shell\b           |  # shell execution patterns
        class\b           |  # defining classes
        def\b             |  # defining functions
        lambda\b          |  # lambda expressions
        \.\b              |  # attribute access (can be abused)
        ;                 |  # semicolon injection
        \{|\}             |  # braces that might start a block
        \<\>              |  # angle brackets for HTML tags
        \bfrom\b          |  # from imports
        \bwith\b          |  # with statements
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)

def process_user_input(user_query: str) -> str:
    """
    Safely evaluate a user supplied Python expression.

    Parameters
    ----------
    user_query : str
        A string containing a Python expression that will be evaluated.

    Returns
    -------
    str
        The result of the evaluation converted to a string, or 'Error!' if the
        evaluation fails or if potentially malicious input is detected.
    """
    # Quick check for disallowed patterns
    if DANGEROUS_PATTERNS.search(user_query):
        return "Error!"

    # Strip surrounding whitespace
    expr = user_query.strip()

    # Reject empty input
    if not expr:
        return "Error!"

    try:
        # Compile the expression in eval mode to ensure it is a single expression
        code = compile(expr, "<user_input>", "eval")

        # Execute the compiled code with no builtins or globals.
        # This prevents access to modules, functions, and objects that could be used
        # maliciously. Only literals, arithmetic operations, and other safe
        # constructs are allowed.
        result = eval(code, {"__builtins__": None}, {})
    except Exception:
        return "Error!"

    # Convert the result to string for a consistent return type
    return str(result)