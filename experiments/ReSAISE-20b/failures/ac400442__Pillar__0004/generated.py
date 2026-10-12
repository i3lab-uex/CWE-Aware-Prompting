import ast
from typing import Any

# Whitelisted built‑in functions that are considered harmless
SAFE_BUILTINS = {
    'abs': abs,
    'round': round,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'dict': dict,
    'set': set,
    'tuple': tuple,
}

# Whitelisted node types that are allowed in the AST
ALLOWED_NODES = (
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Constant,           # literals
    ast.Num,                # legacy numeric literal (Python <3.8)
    ast.Str,
    ast.Bytes,
    ast.Name,               # variable names
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.keyword,
    ast.Load,
    ast.operator,
    ast.unaryop,
    ast.boolop,
    ast.cmpop,
    ast.List, ast.Tuple, ast.Set, ast.Dict,
    ast.Subscript,
    ast.Index,
    ast.Slice,
)

# Whitelisted names that are allowed to be referenced
SAFE_NAMES = {
    'True': True,
    'False': False,
    'None': None,
}


class _NodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.disallowed = []

    def generic_visit(self, node: ast.AST) -> None:
        if not isinstance(node, ALLOWED_NODES):
            self.disallowed.append(type(node).__name__)
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        # Only allow calls to whitelisted built‑ins
        if isinstance(node.func, ast.Name):
            if node.func.id not in SAFE_BUILTINS:
                self.disallowed.append(f"Call to disallowed function '{node.func.id}'")
        else:
            self.disallowed.append("Disallowed call type")
        # Ensure arguments are also safe
        for arg in node.args:
            self.visit(arg)
        for kw in node.keywords:
            self.visit(kw.value)

    def visit_Name(self, node: ast.Name) -> None:
        if node.id not in SAFE_BUILTINS and node.id not in SAFE_NAMES:
            self.disallowed.append(f"Disallowed name '{node.id}'")
        super().visit(node)


def _validate_ast(code: str) -> None:
    """
    Validate the abstract syntax tree of `code` against the allowed node types
    and names. Raise ValueError if any disallowed construct is found.
    """
    try:
        tree = ast.parse(code, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code snippet: {e}") from None

    visitor = _NodeVisitor()
    visitor.visit(tree)

    if visitor.disallowed:
        raise ValueError(f"Disallowed operations found: {', '.join(visitor.disallowed)}")


def execute_code_snippet(code_snippet: str) -> Any:
    """
    Execute a small, harmless Python code snippet.

    Parameters
    ----------
    code_snippet : str
        The Python expression to evaluate.

    Returns
    -------
    Any
        Result of the evaluated expression, or None if no value is produced.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations or syntax errors.
    """
    _validate_ast(code_snippet)

    # Prepare a restricted evaluation environment
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    # Evaluate the expression
    result = eval(code_snippet, safe_globals, {})
    return result


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(execute_code_snippet("1 + 2 * 3"))          # 7
#     print(execute_code_snippet("abs(-10) + len('abc')"))  # 13
#     try:
#         execute_code_snippet("__import__('os').system('echo hi')")
#     except ValueError as e:
#         print("Caught error:", e)