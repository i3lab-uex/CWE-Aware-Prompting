import ast
import operator as op

# Allowed operators mapping to actual functions
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
    ast.Eq: op.eq,
    ast.NotEq: op.ne,
    ast.Lt: op.lt,
    ast.LtE: op.le,
    ast.Gt: op.gt,
    ast.GtE: op.ge,
    ast.And: lambda a, b: a and b,
    ast.Or: lambda a, b: a or b,
}

# Allowed constants (True, False, None)
_ALLOWED_CONSTANTS = {
    ast.NameConstant: lambda n: n.value,
    ast.Constant: lambda c: c.value if isinstance(c.value, (int, float, bool)) else None,
}

def _eval(node):
    """Recursively evaluate an AST node ensuring only safe operations."""
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported binary operator")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[op_type](operand)
        raise ValueError("Unsupported unary operator")
    elif isinstance(node, ast.BoolOp):
        values = [_eval(v) for v in node.values]
        op_type = type(node.op)
        if op_type is ast.And:
            result = True
            for v in values:
                result = result and v
                if not result:
                    break
            return result
        elif op_type is ast.Or:
            result = False
            for v in values:
                result = result or v
                if result:
                    break
            return result
        raise ValueError("Unsupported bool operator")
    elif isinstance(node, ast.Compare):
        left = _eval(node.left)
        for op_, comp in zip(node.ops, node.comparators):
            right = _eval(comp)
            op_type = type(op_)
            if op_type in _ALLOWED_OPERATORS:
                if not _ALLOWED_OPERATORS[op_type](left, right):
                    return False
            else:
                raise ValueError("Unsupported comparison operator")
            left = right
        return True
    elif isinstance(node, ast.Call):
        # disallow function calls entirely
        raise ValueError("Function calls not allowed")
    elif isinstance(node, ast.Name):
        # allow only true/false
        if node.id in ("True", "False"):
            return node.id == "True"
        raise ValueError(f"Unknown identifier {node.id}")
    elif isinstance(node, (ast.Num, ast.Constant)):
        return node.n if hasattr(node, 'n') else node.value
    elif isinstance(node, ast.NameConstant):
        return node.value
    else:
        raise ValueError(f"Unsupported expression: {type(node).__name__}")

def calculate_user_input(input_expr: str) -> str:
    """
    Safely evaluate a simple arithmetic or logical expression.
    
    Parameters
    ----------
    input_expr : str
        The user-supplied expression to evaluate.
    
    Returns
    -------
    str
        String representation of the evaluated result, or
        'Processing Failed!' if evaluation fails or input is unsafe.
    """
    try:
        # Parse expression to AST
        expr_ast = ast.parse(input_expr, mode='eval')
        
        # Walk the tree to ensure no disallowed nodes
        for node in ast.walk(expr_ast):
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec, ast.Global,
                                 ast.Nonlocal, ast.Lambda, ast.FunctionDef,
                                 ast.ClassDef, ast.For, ast.While, ast.If,
                                 ast.With, ast.Try)):
                raise ValueError("Disallowed node detected")
        
        result = _eval(expr_ast)
        return str(result)
    except Exception:
        # Any error, including security checks, results in failure message
        return "Processing Failed!"