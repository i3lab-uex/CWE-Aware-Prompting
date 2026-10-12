import ast
from typing import Any, Optional

# ----------------------------------------------------
# Safe execution of a single Python expression
# ----------------------------------------------------

class _SafeExpressionVisitor(ast.NodeVisitor):
    """
    Visitor that verifies a Python AST contains only
    harmless nodes.  Raises ValueError on disallowed usage.
    """
    # Disallowed node types
    _disallowed = (
        ast.Import,
        ast.ImportFrom,
        ast.Call,          # no function calls
        ast.Attribute,     # prevent attribute access like os.system
        ast.Subscript,     # disallow indexing (e.g., __import__('os'))
        ast.Lambda,
        ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp,
        ast.Yield, ast.YieldFrom,
        ast.AsyncFunctionDef, ast.FunctionDef, ast.ClassDef,
        ast.For, ast.While, ast.With, ast.AsyncWith,
        ast.Try, ast.ExceptHandler,
        ast.Global, ast.Nonlocal,
    )

    # Allowed literal and expression nodes
    _allowed = (
        ast.Module, ast.Expr,
        ast.Constant, ast.Num, ast.Str, ast.Bytes,  # constants
        ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
        ast.NameConstant,  # True, False, None
        ast.Tuple, ast.List, ast.Set, ast.Dict,
    )

    def visit(self, node: ast.AST) -> Any:
        if isinstance(node, self._disallowed):
            raise ValueError(f"Disallowed operation: {type(node).__name__}")
        # Allow only specific nodes
        if not isinstance(node, self._allowed):
            raise ValueError(f"Disallowed node: {type(node).__name__}")
        return super().visit(node)

def _is_safe_expr(code: str) -> None:
    """
    Parse *code* and verify it is a single expression without
    dangerous constructs.  Raises ValueError if unsafe.
    """
    try:
        tree = ast.parse(code, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None
    _SafeExpressionVisitor().visit(tree)

# ----------------------------------------------------
# Public API
# ----------------------------------------------------

def execute_code_snippet(code_snippet: str) -> Optional[Any]:
    """
    Execute a small Python code snippet safely.

    Parameters
    ----------
    code_snippet : str
        The Python expression to evaluate.  Only literal and arithmetic
        expressions are permitted; function calls, imports, or any other
        potentially harmful constructs will raise ValueError.

    Returns
    -------
    Any
        The result of evaluating the expression, or None if no value.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations or invalid syntax.
    """
    # Ensure the snippet is a single safe expression
    _is_safe_expr(code_snippet)

    # Restrict builtins to a minimal safe subset
    allowed_builtins = {
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sum': sum,
    }

    # Evaluate in a sandboxed environment
    try:
        result = eval(
            code_snippet,
            {'__builtins__': allowed_builtins},
            {}
        )
    except Exception as exc:
        # Wrap any runtime error in ValueError to keep API consistent
        raise ValueError(f"Execution error: {exc}") from None

    return result

# ----------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------
# if __name__ == "__main__":
#     print(execute_code_snippet("2 + 3 * (4 - 1)"))   # Should print 11
#     try:
#         execute_code_snippet("__import__('os').system('echo unsafe')")
#     except ValueError as e:
#         print(e)  # Should raise ValueError