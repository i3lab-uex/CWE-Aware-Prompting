import ast
import builtins
import types
from typing import Any, Optional


# ------------------------------------------------------------
# 1. Whitelist of allowed AST node types
# ------------------------------------------------------------
ALLOWED_NODES = {
    # Expressions
    ast.Module,
    ast.Expr,
    ast.Load,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # numeric literals (Python <3.8)
    ast.Constant,     # literals in Python 3.8+
    ast.Str,
    ast.Bytes,
    ast.NameConstant,

    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift,
    ast.BitOr, ast.BitXor, ast.BitAnd, ast.Invert,
    ast.UAdd, ast.USub,

    # Comparisons
    ast.Compare,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Is, ast.IsNot, ast.In, ast.NotIn,

    # Bool ops
    ast.BoolOp,
    ast.And, ast.Or,
    ast.Not,

    # Function definition & calls
    ast.FunctionDef,
    ast.arguments,
    ast.arg,
    ast.Return,
    ast.Call,
    ast.Name,

    # Containers
    ast.List, ast.Tuple, ast.Dict, ast.Set,
    ast.Subscript,

    # Others
    ast.Assign,
    ast.AugAssign,
    ast.For, ast.While, ast.If, ast.With,
    ast.Pass, ast.Break, ast.Continue,

    # Allow attribute access but restrict to safe names
    ast.Attribute,
}

# ------------------------------------------------------------
# 2. Helper: walk AST and ensure only allowed nodes
# ------------------------------------------------------------
def _check_ast(node: ast.AST) -> None:
    if type(node) not in ALLOWED_NODES:
        raise ValueError(f"Forbidden construct: {type(node).__name__}")
    for child in ast.iter_child_nodes(node):
        _check_ast(child)


# ------------------------------------------------------------
# 3. Helper: filter safe builtins
# ------------------------------------------------------------
SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'dict': dict,
    'set': set,
    'tuple': tuple,
}

# ------------------------------------------------------------
# 4. Execution environment
# ------------------------------------------------------------
def execute_python_code(snippet_code: str) -> Optional[Any]:
    """
    Execute a user‑supplied Python snippet in a sandboxed environment.
    Only a small subset of language constructs is allowed.

    Parameters
    ----------
    snippet_code : str
        The Python code to execute.

    Returns
    -------
    Optional[Any]
        Result of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the code contains forbidden operations or syntax errors.
    """
    # Parse the snippet to an AST
    try:
        parsed = ast.parse(snippet_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from None

    # Walk the AST and validate
    _check_ast(parsed)

    # Prepare a minimal execution context
    exec_globals: dict = {
        '__builtins__': SAFE_BUILTINS,
    }
    exec_locals: dict = {}

    # Determine if the snippet is a single expression
    if (
        len(parsed.body) == 1
        and isinstance(parsed.body[0], ast.Expr)
    ):
        # Evaluate the expression
        expr_code = compile(parsed, filename="<sandbox>", mode="eval")
        try:
            result = eval(expr_code, exec_globals, exec_locals)
            return result
        except Exception as exc:
            raise ValueError(f"Execution error: {exc}") from None
    else:
        # Execute statements
        exec_code = compile(parsed, filename="<sandbox>", mode="exec")
        try:
            exec(exec_code, exec_globals, exec_locals)
        except Exception as exc:
            raise ValueError(f"Execution error: {exc}") from None
        return None

# ------------------------------------------------------------
# 5. Example usage (commented out)
# ------------------------------------------------------------
# if __name__ == "__main__":
#     print(execute_python_code("2 + 3"))          # outputs: 5
#     execute_python_code("""
#         def add(a, b):
#             return a + b
#         print(add(4, 5))
#     """)                                       # prints: 9