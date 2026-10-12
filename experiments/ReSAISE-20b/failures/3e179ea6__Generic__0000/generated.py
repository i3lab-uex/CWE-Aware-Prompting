import ast
import math
from typing import Any

# --------------------------------------------------------------------------- #
#   Safe evaluator for mathematical expressions written in Python syntax
# --------------------------------------------------------------------------- #

SAFE_FUNCTIONS = {
    # Basic math functions that are safe to expose
    "sin":   math.sin,
    "cos":   math.cos,
    "tan":   math.tan,
    "asin":  math.asin,
    "acos":  math.acos,
    "atan":  math.atan,
    "sinh":  math.sinh,
    "cosh":  math.cosh,
    "tanh":  math.tanh,
    "log":   math.log,          # natural log
    "log10": math.log10,
    "sqrt":  math.sqrt,
    "ceil":  math.ceil,
    "floor": math.floor,
    "fabs":  math.fabs,
    # Constants
    "pi":    math.pi,
    "e":     math.e,
}

# Allowed AST node types
ALLOWED_NODES = (
    ast.Expression,   # root of the parsed tree
    ast.BinOp,        # binary operators (+,-,*,/,//,% ,**)
    ast.UnaryOp,      # unary operators (+,-)
    ast.Num,          # Python <3.8 numeric literals
    ast.Constant,     # Python >=3.8 numeric literals
    ast.Call,         # function calls to safe functions
    ast.Name,         # names of allowed constants/functions
)

# Allowed binary operators
ALLOWED_BINOPS = (
    ast.Add, ast.Sub,
    ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow
)

# Allowed unary operators
ALLOWED_UNARYOPS = (
    ast.UAdd, ast.USub,
)

def _eval(node: ast.AST) -> Any:
    """
    Recursively evaluate an AST node. Only nodes that are explicitly allowed
    will be processed. Any other node results in a ValueError.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)

    # Numeric literals
    if isinstance(node, (ast.Num, ast.Constant)):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")

    # Binary operations
    if isinstance(node, ast.BinOp):
        if not isinstance(node.op, ALLOWED_BINOPS):
            raise ValueError("Unsupported binary operator")
        left = _eval(node.left)
        right = _eval(node.right)
        return _apply_binop(node.op, left, right)

    # Unary operations
    if isinstance(node, ast.UnaryOp):
        if not isinstance(node.op, ALLOWED_UNARYOPS):
            raise ValueError("Unsupported unary operator")
        operand = _eval(node.operand)
        return _apply_unaryop(node.op, operand)

    # Function calls
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function names are allowed")
        func_name = node.func.id
        if func_name not in SAFE_FUNCTIONS:
            raise ValueError(f"Function '{func_name}' is not allowed")
        args = [_eval(arg) for arg in node.args]
        # No keyword arguments are allowed
        if node.keywords:
            raise ValueError("Keyword arguments not allowed")
        return SAFE_FUNCTIONS[func_name](*args)

    # Names (constants)
    if isinstance(node, ast.Name):
        if node.id in SAFE_FUNCTIONS:
            return SAFE_FUNCTIONS[node.id]
        raise ValueError(f"Name '{node.id}' is not allowed")

    raise ValueError("Unsupported expression component")

def _apply_binop(op: ast.operator, left: Any, right: Any) -> Any:
    if isinstance(op, ast.Add):
        return left + right
    if isinstance(op, ast.Sub):
        return left - right
    if isinstance(op, ast.Mult):
        return left * right
    if isinstance(op, ast.Div):
        return left / right
    if isinstance(op, ast.FloorDiv):
        return left // right
    if isinstance(op, ast.Mod):
        return left % right
    if isinstance(op, ast.Pow):
        return left ** right
    raise ValueError("Unsupported binary operator")

def _apply_unaryop(op: ast.unaryop, operand: Any) -> Any:
    if isinstance(op, ast.UAdd):
        return +operand
    if isinstance(op, ast.USub):
        return -operand
    raise ValueError("Unsupported unary operator")

def evaluate_expression_safely(expression: str) -> str:
    """
    Safely evaluate a mathematical expression written in Python syntax.

    Parameters
    ----------
    expression : str
        The string containing the mathematical expression.

    Returns
    -------
    str
        The result of evaluating the expression, or 'Unsafe Code Detected!'
        if the expression contains disallowed constructs or raises an error.

    Notes
    -----
    Only a limited set of Python syntax is allowed:
        * Numeric literals (int, float)
        * Binary operators: + - * / // % **
        * Unary operators: + -
        * Function calls to a predefined set of safe math functions
          (see ``SAFE_FUNCTIONS``)
        * References to the constants pi and e

    Any other syntax element (e.g., attribute access, list/dict literals,
    function definitions, imports, etc.) will trigger the safety guard.
    """
    try:
        # Parse the expression in 'eval' mode
        tree = ast.parse(expression, mode='eval')

        # Verify that all nodes are allowed
        for node in ast.walk(tree):
            if not isinstance(node, ALLOWED_NODES):
                return 'Unsafe Code Detected!'

        # Evaluate the expression
        result = _eval(tree)
        return str(result)

    except Exception:
        # Any error (parsing, evaluation, etc.) is treated as unsafe
        return 'Unsafe Code Detected!'