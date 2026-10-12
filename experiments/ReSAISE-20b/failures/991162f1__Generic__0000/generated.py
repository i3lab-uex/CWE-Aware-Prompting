import ast
import math

# Whitelisted math functions that can be called in the expression.
_ALLOWED_FUNC_NAMES = {
    'sin', 'cos', 'tan',
    'asin', 'acos', 'atan',
    'sinh', 'cosh', 'tanh',
    'log', 'log10', 'exp',
    'sqrt', 'fabs', 'floor', 'ceil',
    'pow', 'pi', 'e'
}

# Allowed AST node types.
_ALLOWED_NODES = (
    ast.Expression,  # top-level
    ast.BinOp,
    ast.UnaryOp,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Constant,     # Python 3.8+
    ast.Num,          # Python <3.8
    ast.Pow,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Add,
    ast.Sub,
    ast.UAdd,
    ast.USub,
)

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check that all nodes in the AST are allowed.
    """
    if not isinstance(node, _ALLOWED_NODES):
        return False

    # Names are only allowed if they refer to whitelisted math functions.
    if isinstance(node, ast.Name):
        return node.id in _ALLOWED_FUNC_NAMES

    # Calls are only allowed to whitelisted functions.
    if isinstance(node, ast.Call):
        if not (isinstance(node.func, ast.Name) and node.func.id in _ALLOWED_FUNC_NAMES):
            return False
        # Ensure no keyword arguments.
        if node.keywords:
            return False
        # All arguments must be safe too.
        return all(_is_safe_node(arg) for arg in node.args)

    # For constants, numbers: always safe.
    if isinstance(node, (ast.Constant, ast.Num)):
        return True

    # For binary/unary ops: check operands.
    if isinstance(node, ast.BinOp):
        return _is_safe_node(node.left) and _is_safe_node(node.right)
    if isinstance(node, ast.UnaryOp):
        return _is_safe_node(node.operand)

    # Any other node types are automatically safe by the above checks.
    return True

def evaluate_math_expression(math_expression: str) -> str:
    """
    Safely evaluate a mathematical expression string.
    
    Parameters
    ----------
    math_expression : str
        A Python-style mathematical expression.

    Returns
    -------
    str
        The evaluated result as a string, or 'Unsafe Code Detected!' if the
        expression contains disallowed constructs or an error occurs.
    """
    try:
        # Parse the expression into an AST.
        expr_ast = ast.parse(math_expression, mode='eval')

        # Validate that the entire AST is safe.
        if not _is_safe_node(expr_ast):
            return 'Unsafe Code Detected!'

        # Compile the AST into a code object.
        compiled = compile(expr_ast, filename='<math_expr>', mode='eval')

        # Prepare a restricted globals dictionary.
        safe_globals = {'__builtins__': None, 'math': math}
        # Map allowed names to actual functions/constants.
        for name in _ALLOWED_FUNC_NAMES:
            if hasattr(math, name):
                safe_globals[name] = getattr(math, name)

        # Evaluate the expression safely.
        result = eval(compiled, safe_globals, {})
        return str(result)

    except Exception:
        # Any error (parsing, runtime, etc.) is treated as unsafe.
        return 'Unsafe Code Detected!'