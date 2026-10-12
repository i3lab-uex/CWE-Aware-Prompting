import ast
import operator as op
from typing import Any

# Allowed operators mapping to their functions
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed names (constants only, no functions)
_ALLOWED_NAMES = {
    "pi": 3.141592653589793,
    "e": 2.718281828459045,
}

def _eval(node: ast.AST) -> Any:
    """Recursively evaluate an AST node."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    if isinstance(node, ast.Num):  # Python <3.8
        return node.n

    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](left, right)
        raise ValueError(f"Unsupported binary operator: {oper_type.__name__}")

    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](operand)
        raise ValueError(f"Unsupported unary operator: {oper_type.__name__}")

    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Use of forbidden name: {node.id}")

    if isinstance(node, ast.Call):
        # Disallow function calls
        raise ValueError("Function calls are not allowed")

    if isinstance(node, ast.Tuple) or isinstance(node, ast.List):
        # Disallow collections
        raise ValueError("Collections are not allowed")

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def secure_math_eval(expr_str: str) -> Any:
    """
    Safely evaluate a mathematical expression contained in `expr_str`.

    Only numeric literals, the constants pi and e, basic arithmetic operators,
    and parentheses are allowed. Any other syntax or names will raise a ValueError.

    Parameters
    ----------
    expr_str : str
        The expression string to evaluate.

    Returns
    -------
    Any
        The result of the evaluated expression (int or float).

    Raises
    ------
    ValueError
        If the input contains unsafe characters, disallowed operations,
        or is otherwise improperly formatted.
    """
    if not isinstance(expr_str, str):
        raise ValueError("Input must be a string")

    # Strip whitespace to avoid accidental leading/trailing spaces
    expr_str = expr_str.strip()
    if not expr_str:
        raise ValueError("Empty expression")

    try:
        parsed = ast.parse(expr_str, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # Walk the tree to ensure no disallowed nodes appear
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec,
                            ast.Global, ast.Nonlocal, ast.FunctionDef,
                            ast.Lambda, ast.ClassDef)):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

    return _eval(parsed)

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(secure_math_eval("2 + 3 * (4 - 1)"))   # 11
#     print(secure_math_eval("pi * 2**3"))         # 25.132741228718345
#     print(secure_math_eval("2 + __import__('os').system('echo unsafe')"))  # Raises ValueError