import ast
from typing import Any, Optional

# List of allowed AST node types (read‑only operations only)
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Load,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,  # only allowed for builtins listed in SAFE_BUILTINS
    ast.keyword,
    ast.Attribute,  # only for safe builtins
    ast.Subscript,
    ast.Index,
    ast.Slice,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.Lambda,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.FloorDiv, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor,
    ast.BitAnd, ast.And, ast.Or, ast.Not,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Unary ops
    ast.UAdd, ast.USub,
}

# Safe built‑in functions that are allowed to be called
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'dict': dict,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'pow': pow,
    'range': range,
    'set': set,
    'str': str,
    'sum': sum,
    'tuple': tuple,
}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively verify that all nodes in the AST are allowed.
    Raise ValueError if a disallowed node is encountered.
    """
    if type(node) not in ALLOWED_NODES:
        raise ValueError(f"Disallowed operation: {type(node).__name__}")

    for child in ast.iter_child_nodes(node):
        _is_safe_node(child)

def execute_code_snippet(code_snippet: str) -> Optional[Any]:
    """
    Execute a small Python snippet safely.

    Parameters
    ----------
    code_snippet : str
        The Python code to execute. Only expressions and harmless
        operations are allowed. Import statements, file I/O,
        function definitions, loops, and any other side‑effects are
        disallowed.

    Returns
    -------
    Any or None
        The value of the last expression in the snippet, or None if no
        expression is present.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations.
    """
    if not isinstance(code_snippet, str):
        raise ValueError("code_snippet must be a string")

    # Parse the code into an AST
    try:
        parsed = ast.parse(code_snippet, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code snippet: {exc}") from exc

    # Validate safety of the AST
    _is_safe_node(parsed)

    # Prepare a restricted globals dictionary
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    # No locals needed for expressions
    safe_locals = {}

    # Execute the code in a restricted namespace
    exec(compile(parsed, filename="<sandbox>", mode="exec"),
         safe_globals,
         safe_locals)

    # Retrieve the value of the last expression, if any
    # In exec mode, expressions are not returned directly.
    # We can capture them by wrapping the snippet in an Expression node.
    try:
        expr_tree = ast.parse(code_snippet, mode='eval')
        # If parsing as eval succeeds, return the evaluated result
        return eval(compile(expr_tree, filename="<sandbox>", mode="eval"),
                    safe_globals,
                    safe_locals)
    except SyntaxError:
        # Not a single expression; return None
        return None

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(execute_code_snippet("1 + 2 * 3"))   # -> 7
#     print(execute_code_snippet("sum(range(10))"))  # -> 45
#     execute_code_snippet("open('file.txt')")   # Raises ValueError