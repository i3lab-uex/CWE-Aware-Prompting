import ast
import operator as op
import math

# Allowed operators and their corresponding functions
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

# Whitelist of allowed names from the math module
_ALLOWED_NAMES = {name: getattr(math, name) for name in dir(math) if not name.startswith('_')}

def _eval(node):
    """
    Recursively evaluate an AST node.
    Only nodes that are in the allowed set will be processed.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](left, right)
        raise ValueError("Unsupported binary operator")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        oper_type = type(node.op)
        if oper_type in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[oper_type](operand)
        raise ValueError("Unsupported unary operator")
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls allowed")
        func_name = node.func.id
        if func_name not in _ALLOWED_NAMES:
            raise ValueError(f"Function '{func_name}' is not allowed")
        func = _ALLOWED_NAMES[func_name]
        args = [_eval(arg) for arg in node.args]
        return func(*args)
    elif isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise ValueError(f"Name '{node.id}' is not allowed")
    else:
        raise ValueError(f"Unsupported expression type: {type(node).__name__}")

def secure_expression_evaluator(expr_input: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.
    
    Parameters
    ----------
    expr_input : str
        The user-provided expression to evaluate.
    
    Returns
    -------
    str
        The string representation of the evaluated result, or 
        'Unsafe Code Detected!' if the input is unsafe or evaluation fails.
    """
    try:
        # Parse expression into an AST
        parsed = ast.parse(expr_input, mode='eval')
        
        # Walk the tree to ensure no disallowed nodes are present
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec,
                                 ast.FunctionDef, ast.ClassDef, ast.Lambda,
                                 ast.Global, ast.Nonlocal, ast.With)):
                raise ValueError("Disallowed node type detected")
        
        result = _eval(parsed)
        return str(result)
    except Exception:
        # Any error (parsing, disallowed content, runtime) leads to warning
        return "Unsafe Code Detected!"