import ast
import operator as op
import math

# Allowed operators mapping
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed names from math module
_ALLOWED_NAMES = {k for k in dir(math) if not k.startswith("_")}
_ALLOWED_NAMES.update({"pi", "e"})  # ensure these are available

def _eval_node(node):
    """
    Recursively evaluate an AST node if it is safe.
    Raises ValueError on unsafe nodes.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](left, right)
        raise ValueError("Unsupported binary operator")
    if isinstance(node, ast.UnaryOp):
        operand = _eval_node(node.operand)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](operand)
        raise ValueError("Unsupported unary operator")
    if isinstance(node, ast.Call):
        # Ensure the function name is allowed
        if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_NAMES:
            raise ValueError("Disallowed function call")
        func = getattr(math, node.func.id)
        args = [_eval_node(arg) for arg in node.args]
        return func(*args)
    if isinstance(node, ast.Name):
        # Allow constants like pi or e
        if node.id in _ALLOWED_NAMES:
            return getattr(math, node.id)
        raise ValueError("Disallowed name")
    if isinstance(node, ast.Expr):
        return _eval_node(node.value)
    raise ValueError("Unsupported expression")

def safe_math_evaluator(expr_string: str) -> str:
    """
    Safely evaluate a mathematical expression from a string.
    
    Parameters
    ----------
    expr_string : str
        The input expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluation result or a warning message.
    
    Raises
    ------
    None (returns 'Unsafe Code Detected!' on error)
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr_string, mode="eval")
        # Walk the tree to ensure no unsafe nodes are present
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec)):
                raise ValueError("Import or exec detected")
        result = _eval_node(parsed.body)
        return str(result)
    except Exception:
        # Any exception means the expression is unsafe or evaluation failed
        return "Unsafe Code Detected!"