import ast
import operator as op
import re

# Supported operators mapping to functions
_OPERATORS = {
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

class _EvalVisitor(ast.NodeVisitor):
    """
    Evaluates an AST node using only allowed operations and constants.
    Raises ValueError on unsupported nodes or operations.
    """
    def __init__(self, var_values):
        self.var_values = var_values

    def visit(self, node):
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        elif isinstance(node, ast.Num):          # For Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):    # For Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value)}")
        elif isinstance(node, ast.BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            func = _OPERATORS.get(type(node.op))
            if func is None:
                raise ValueError(f"Unsupported binary operator: {ast.dump(node.op)}")
            return func(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self.visit(node.operand)
            func = _OPERATORS.get(type(node.op))
            if func is None:
                raise ValueError(f"Unsupported unary operator: {ast.dump(node.op)}")
            return func(operand)
        elif isinstance(node, ast.Name):
            if node.id in self.var_values:
                val = self.var_values[node.id]
                if isinstance(val, (int, float)):
                    return val
                raise ValueError(f"Variable {node.id} has non-numeric value: {val}")
            raise ValueError(f"Undefined variable: {node.id}")
        elif isinstance(node, ast.Call):
            raise ValueError("Function calls are not allowed.")
        else:
            raise ValueError(f"Unsupported expression element: {ast.dump(node)}")

def _replace_variables(expr, var_values):
    """
    Replace variable names in the expression with their literal values.
    This step is optional because the AST visitor handles variables,
    but we keep it to catch undefined names early and avoid accidental
    function calls via name resolution.
    """
    # Ensure variable names are isolated tokens (words)
    pattern = r'\b(' + '|'.join(map(re.escape, var_values.keys())) + r')\b'
    def repl(match):
        val = var_values[match.group(0)]
        if isinstance(val, (int, float)):
            return str(val)
        raise ValueError(f"Variable {match.group(0)} has non-numeric value: {val}")
    return re.sub(pattern, repl, expr)

def simplify_math_expr(math_expr: str, var_values: dict) -> str:
    """
    Simplify a mathematical expression with optional variables.

    Parameters
    ----------
    math_expr : str
        The input expression, e.g., "2 * x + 3".
    var_values : dict
        Mapping from variable names to numeric values.

    Returns
    -------
    str
        The evaluated result as a string.

    Raises
    ------
    ValueError
        If the expression is invalid or contains disallowed operations.
    """
    if not isinstance(math_expr, str):
        raise ValueError("math_expr must be a string")
    if not isinstance(var_values, dict):
        raise ValueError("var_values must be a dictionary")

    # Sanitize variable names: only alphanumerics and underscores
    for name in var_values:
        if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', name):
            raise ValueError(f"Invalid variable name: {name}")

    # Replace variables with literals to catch undefined names early
    sanitized_expr = _replace_variables(math_expr, var_values)

    # Parse expression into AST safely
    try:
        expr_ast = ast.parse(sanitized_expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in expression: {exc}") from exc

    # Walk the AST to ensure only allowed nodes are present
    visitor = _EvalVisitor(var_values)
    try:
        result = visitor.visit(expr_ast)
    except Exception as exc:
        raise ValueError(f"Failed to evaluate expression: {exc}") from exc

    # Return result as string
    return str(result)