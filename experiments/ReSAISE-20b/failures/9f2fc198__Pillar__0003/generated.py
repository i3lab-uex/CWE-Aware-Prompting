import ast
import math
import operator as op

# Allowed operators mapping
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

# Allowed names (constants and math functions)
_ALLOWED_NAMES = {
    k: getattr(math, k) for k in dir(math) if not k.startswith("_")
}
_ALLOWED_NAMES.update({"pi": math.pi, "e": math.e})


def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    elif isinstance(node, ast.Num):  # <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    elif isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        oper = _ALLOWED_OPERATORS.get(type(node.op))
        if oper is None:
            raise ValueError("Unsupported binary operator")
        return oper(left, right)
    elif isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        oper = _ALLOWED_OPERATORS.get(type(node.op))
        if oper is None:
            raise ValueError("Unsupported unary operator")
        return oper(operand)
    elif isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Name '{node.id}' not allowed")
    elif isinstance(node, ast.Call):
        # Allow calls to math functions
        if isinstance(node.func, ast.Name) and node.func.id in _ALLOWED_NAMES:
            func = _ALLOWED_NAMES[node.func.id]
            args = [_eval_node(arg) for arg in node.args]
            return func(*args)
        raise ValueError("Unsupported function call")
    else:
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def secure_expression_evaluator(expr_input: str) -> str:
    """
    Safely evaluate a mathematical expression string.

    Parameters
    ----------
    expr_input : str
        User supplied mathematical expression.

    Returns
    -------
    str
        Result of the evaluation or 'Unsafe Code Detected!' on failure.
    """
    # Quick blacklist for obvious dangerous patterns
    bad_patterns = [
        r"\bimport\b",
        r"\beval\b",
        r"\bexec\b",
        r"__import__",
        r"\bopen\b",
        r"\bsys\b",
        r"\bsubprocess\b",
        r"\bexecfile\b",
        r"\bfopen\b",
    ]
    for pat in bad_patterns:
        if ast.literal_eval(f"r'{pat}'") and re.search(pat, expr_input):
            return "Unsafe Code Detected!"

    try:
        parsed = ast.parse(expr_input, mode="eval")
    except Exception:
        return "Unsafe Code Detected!"

    # Validate nodes
    for node in ast.walk(parsed):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.Module, ast.FunctionDef,
                             ast.ClassDef, ast.Lambda, ast.Assign)):
            return "Unsafe Code Detected!"

    try:
        result = _eval_node(parsed)
        return str(result)
    except Exception:
        return "Unsafe Code Detected!"