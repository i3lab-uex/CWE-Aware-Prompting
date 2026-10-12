import ast
from types import FunctionType

# Allowed nodes in the AST (safe subset)
SAFE_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Load,
    ast.Call,
    ast.Name,
    ast.Constant,          # literals
    ast.BinOp,
    ast.UnaryOp,
    ast.operator,
    ast.unaryop,
    ast.Compare,
    ast.cmpop,
    ast.BoolOp,
    ast.boolop,
    ast.List, ast.Tuple, ast.Dict, ast.Set,
    ast.keyword,
}

# Builtins that are considered harmless
SAFE_BUILTINS = {
    'print',
    'len',
    'sum',
    'min',
    'max',
    'abs',
    'round',
    'sorted',
    'list',
    'tuple',
    'dict',
    'set',
    'range',
    # Add more if needed
}

def _is_safe(node: ast.AST) -> bool:
    """Recursively check that all nodes are in SAFE_NODES."""
    if type(node) not in SAFE_NODES:
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def execute_code_snippet(code_snippet: str):
    """
    Execute a small piece of Python code in a restricted environment.

    Parameters
    ----------
    code_snippet : str
        The Python code to execute.

    Returns
    -------
    Any
        Result of the last expression or None if there is no result.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # Parse the code into an AST
    try:
        parsed = ast.parse(code_snippet, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code snippet: {exc}") from None

    # Ensure all nodes are safe
    if not _is_safe(parsed):
        raise ValueError("Disallowed operations detected in the code snippet.")

    # Ensure no import statements or other unsafe constructs
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("Import statements are not allowed.")
        if isinstance(node, (ast.Exec, ast.With, ast.For, ast.While,
                            ast.If, ast.Try, ast.FunctionDef, ast.ClassDef)):
            raise ValueError(f"Disallowed statement: {type(node).__name__}")

    # Prepare restricted globals
    safe_globals = {
        '__builtins__': {k: __builtins__[k] for k in SAFE_BUILTINS if k in __builtins__},
    }

    # Execute the code
    exec(compile(parsed, filename='<snippet>', mode='exec'), safe_globals)

    # Return the result of the last expression if any
    last_expr = None
    for node in reversed(parsed.body):
        if isinstance(node, ast.Expr):
            last_expr = node.value
            break

    if last_expr is None:
        return None

    # Evaluate the last expression in the same restricted environment
    try:
        result = eval(compile(ast.Expression(last_expr), filename='<expr>', mode='eval'),
                      safe_globals)
        return result
    except Exception as exc:
        # If evaluation fails, just ignore and return None
        return None

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(execute_code_snippet("a = 3 + 4\nprint(a)"))  # prints 7
#     print(execute_code_snippet("len([1,2,3])"))       # returns 3