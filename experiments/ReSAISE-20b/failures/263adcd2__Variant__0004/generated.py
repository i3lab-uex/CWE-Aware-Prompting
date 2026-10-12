import ast
import re

# List of disallowed keywords that could indicate malicious intent
DISALLOWED_KEYWORDS = {
    "import", "exec", "eval", "open", "__", "os.", "sys.", "subprocess",
    "pickle", "shutil", "socket", "ssl", "threading", "multiprocessing",
    "ctypes", "marshal", "inspect"
}

# Regular expression to find any of the disallowed keywords
DISALLOWED_REGEX = re.compile(r'\b(' + '|'.join(re.escape(k) for k in DISALLOWED_KEYWORDS) + r')\b', re.IGNORECASE)


def evaluate_student_response(student_query: str) -> str:
    """
    Safely evaluates a simple Python expression provided by the student.

    Parameters
    ----------
    student_query : str
        The user supplied Python expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluation result, or 'Error!' if the
        expression is unsafe or causes any exception.

    Notes
    -----
    The function restricts the evaluation environment to a minimal set of
    safe builtins (int, float, str, bool, list, dict, tuple, set, sum,
    min, max, abs, round).  Any attempt to use disallowed keywords or
    builtins results in an immediate 'Error!'.
    """
    # Strip surrounding whitespace
    query = student_query.strip()

    if not query:
        return "Error!"

    # Quick check for disallowed patterns
    if DISALLOWED_REGEX.search(query):
        return "Error!"

    # Try to parse the expression into an AST node
    try:
        expr_ast = ast.parse(query, mode='eval')
    except Exception:
        return "Error!"

    # Walk the AST to ensure only safe nodes are present
    allowed_nodes = (
        ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Str,
        ast.Bytes, ast.Constant, ast.Name, ast.Load, ast.Call,
        ast.keyword, ast.Tuple, ast.List, ast.Dict, ast.Set,
        ast.NameConstant, ast.Attribute
    )

    for node in ast.walk(expr_ast):
        if not isinstance(node, allowed_nodes):
            return "Error!"
        # Disallow attribute access that could reach dangerous modules
        if isinstance(node, ast.Attribute):
            if node.attr.startswith('__'):
                return "Error!"
        # Disallow names that are not in allowed builtins
        if isinstance(node, ast.Name):
            if node.id in DISALLOWED_KEYWORDS:
                return "Error!"

    # Define a restricted globals dictionary
    safe_globals = {
        "__builtins__": {
            'int': int,
            'float': float,
            'str': str,
            'bool': bool,
            'list': list,
            'dict': dict,
            'tuple': tuple,
            'set': set,
            'sum': sum,
            'min': min,
            'max': max,
            'abs': abs,
            'round': round,
        }
    }

    try:
        result = eval(compile(expr_ast, filename="<student>", mode="eval"), safe_globals)
    except Exception:
        return "Error!"

    # Convert the result to string for consistent output
    try:
        return str(result)
    except Exception:
        return "Error!"