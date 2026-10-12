import ast
import operator as op
import math

# Mapping of AST operators to actual functions
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
}

# Allowed unary operators
UNARY_OPERATORS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed names from the math module
ALLOWED_NAMES = {name for name in dir(math) if not name.startswith("_")}
# Add built-in constants
ALLOWED_NAMES.update({"pi", "e"})

def _eval(node):
    """
    Recursively evaluate an AST node safely.
    Raises ValueError on any disallowed construct.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numbers (Python 3.8+ use Constant)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    if isinstance(node, ast.Num):  # For older Python versions
        return node.n

    # Binary operations
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        oper_func = OPERATORS.get(type(node.op))
        if oper_func is None:
            raise ValueError("Unsupported binary operator")
        return oper_func(left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        oper_func = UNARY_OPERATORS.get(type(node.op))
        if oper_func is None:
            raise ValueError("Unsupported unary operator")
        return oper_func(operand)

    # Function calls (only allowed math functions)
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function names allowed")
        func_name = node.func.id
        if func_name not in ALLOWED_NAMES:
            raise ValueError("Disallowed function")
        func = getattr(math, func_name)
        args = [_eval(arg) for arg in node.args]
        return func(*args)

    # Names (constants)
    if isinstance(node, ast.Name):
        if node.id not in ALLOWED_NAMES:
            raise ValueError("Disallowed name")
        return getattr(math, node.id)

    # Disallow any other nodes
    raise ValueError("Unsupported expression")

def safely_execute_expression(expression_code: str) -> str:
    """
    Safely evaluate a mathematical expression supplied by the user.
    
    Parameters
    ----------
    expression_code : str
        The Python expression to evaluate.

    Returns
    -------
    str
        Result of the evaluation or 'Unsafe Code Detected!' if any
        disallowed construct is found or an exception occurs.
    """
    try:
        # Parse the expression into an AST
        parsed = ast.parse(expression_code, mode='eval')

        # Walk the tree to ensure no disallowed nodes exist
        for node in ast.walk(parsed):
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.Exec,
                                 ast.With, ast.For, ast.While, ast.FunctionDef,
                                 ast.ClassDef, ast.Lambda)):
                return "Unsafe Code Detected!"

        result = _eval(parsed)
        return str(result)
    except Exception:
        # Any parsing or evaluation error is treated as unsafe
        return "Unsafe Code Detected!"