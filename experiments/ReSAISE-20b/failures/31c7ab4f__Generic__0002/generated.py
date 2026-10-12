import ast
from typing import Any

def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluates a simple arithmetic expression provided as a string.

    Only the following constructs are allowed:
        - Literals (int, float)
        - Binary operations: +, -, *, /, //, %, **, <<, >>, &
        - Unary operations: +, -
        - Parentheses for grouping

    Any other constructs (function calls, attribute access, imports,
    etc.) will cause the function to return 'Unsafe Code Detected!'.

    Parameters
    ----------
    code_string : str
        The expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluated result, or an error
        message if the input is unsafe or evaluation fails.
    """
    # Define a set of allowed AST node types
    ALLOWED_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python >=3.8
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
        ast.LShift,
        ast.RShift,
        ast.BitAnd,
        ast.BitOr,
        ast.BitXor,
        ast.UAdd,
        ast.USub,
        ast.Paren,        # Not a real node; parentheses are handled by grouping
    }

    def _is_safe(node: ast.AST) -> bool:
        """
        Recursively check that the AST contains only allowed nodes.
        """
        if type(node) not in ALLOWED_NODES:
            return False
        for child in ast.iter_child_nodes(node):
            if not _is_safe(child):
                return False
        return True

    try:
        # Parse the expression (not a full module)
        parsed = ast.parse(code_string, mode='eval')
    except SyntaxError:
        return 'Unsafe Code Detected!'

    # Check safety of the parsed AST
    if not _is_safe(parsed):
        return 'Unsafe Code Detected!'

    try:
        # Evaluate the expression in a restricted environment
        result: Any = eval(compile(parsed, filename="<string>", mode="eval"),
                           {"__builtins__": None}, {})
    except Exception:
        return 'Unsafe Code Detected!'

    return str(result)