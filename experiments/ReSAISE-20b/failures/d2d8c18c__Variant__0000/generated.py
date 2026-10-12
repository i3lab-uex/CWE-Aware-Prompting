import ast
import math

# Whitelist of allowed names (functions and constants from the math module)
_ALLOWED_NAMES = {
    name: getattr(math, name) for name in dir(math) if not name.startswith("_")
}
# Optionally add a few built‑in constants
_ALLOWED_NAMES.update({"pi": math.pi, "e": math.e})

# Allowed AST node types
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,  # Python <3.8
    ast.Constant,  # Python >=3.8
    ast.Name,
    ast.Call,
    ast.Load,
    ast.operator,
    ast.unaryop,
    ast.cmpop,
    ast.BoolOp,
    ast.And,
    ast.Or,
    ast.Compare,
    ast.Subscript,
    ast.Index,
    ast.Slice,
}

class SafeEvalVisitor(ast.NodeVisitor):
    """
    Walk the AST and ensure only allowed nodes are present.
    Also checks that all called names are in the whitelist.
    """
    def visit(self, node):
        if type(node) not in _ALLOWED_NODES:
            raise ValueError(f"Disallowed node: {type(node).__name__}")
        super().visit(node)

    def visit_Name(self, node):
        if node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Disallowed name: {node.id}")

    def visit_Call(self, node):
        # The function being called must be a Name and whitelisted
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct function calls allowed")
        if node.func.id not in _ALLOWED_NAMES:
            raise ValueError(f"Disallowed function: {node.func.id}")
        # Recursively visit arguments
        for arg in node.args:
            self.visit(arg)
        for keyword in node.keywords:
            self.visit(keyword.value)

def execute_user_expression(expression_string: str) -> str:
    """
    Safely evaluate a user supplied mathematical expression.

    Parameters
    ----------
    expression_string : str
        The expression to evaluate. It may contain arithmetic operations,
        calls to math functions (e.g., sin, cos) and constants (pi, e).

    Returns
    -------
    str
        The string representation of the result or 'Unsafe Code Detected!'
        if the expression contains disallowed constructs or errors occur.
    """
    try:
        # Parse into an AST
        parsed = ast.parse(expression_string, mode="eval")

        # Verify safety of the expression
        SafeEvalVisitor().visit(parsed)

        # Compile and evaluate with restricted globals/locals
        code = compile(parsed, "<string>", mode="eval")
        result = eval(code, {"__builtins__": {}}, _ALLOWED_NAMES)

        return str(result)
    except Exception:
        # Any exception is treated as unsafe
        return "Unsafe Code Detected!"