import ast
import math

# List of allowed names (functions and constants) from the math module
_ALLOWED_NAMES = {
    name: getattr(math, name)
    for name in dir(math)
    if not name.startswith("__")
}

# Add some built‑in functions that are safe for math expressions
_ALLOWED_NAMES.update({
    "abs": abs,
    "round": round,
})


class _SafeEvalVisitor(ast.NodeVisitor):
    """
    AST visitor that ensures the expression only contains safe nodes.
    Raises a ValueError if an unsafe node is encountered.
    """

    def visit(self, node):
        method = "visit_" + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def visit_Module(self, node):
        if len(node.body) != 1 or not isinstance(node.body[0], ast.Expr):
            raise ValueError("Only single expressions are allowed")
        self.visit(node.body[0])

    def visit_Expr(self, node):
        self.visit(node.value)

    # Allowed literals
    def visit_Num(self, node):  # Python <3.8
        pass

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return
        raise ValueError("Only numeric constants are allowed")

    # Allowed binary/unary operators
    def visit_BinOp(self, node):
        if not isinstance(node.op, (ast.Add, ast.Sub, ast.Mult,
                                    ast.Div, ast.Pow, ast.Mod, ast.FloorDiv)):
            raise ValueError("Unsupported binary operator")
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        if not isinstance(node.op, (ast.UAdd, ast.USub)):
            raise ValueError("Unsupported unary operator")
        self.visit(node.operand)

    # Allowed function calls
    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls allowed")
        if node.func.id not in _ALLOWED_NAMES:
            raise ValueError(f"Function '{node.func.id}' is not allowed")
        for arg in node.args:
            self.visit(arg)
        if node.keywords:
            raise ValueError("Keyword arguments are not allowed")

    # Allowed variable names (constants from math)
    def visit_Name(self, node):
        if node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Name '{node.id}' is not allowed")

    # Disallow attribute access, imports, assignments, etc.
    def generic_visit(self, node):
        raise ValueError(f"Disallowed syntax: {node.__class__.__name__}")


def execute_user_expression(expression_string: str) -> str:
    """
    Safely evaluate a mathematical expression supplied by the user.

    Parameters
    ----------
    expression_string : str
        A Python expression that may use numeric literals, operators,
        and functions/constants from the math module.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Unsafe Code Detected!'
        if the expression contains disallowed constructs or an error occurs.
    """
    try:
        # Parse into an AST
        tree = ast.parse(expression_string, mode="eval")

        # Validate the tree contains only safe nodes
        _SafeEvalVisitor().visit(tree)

        # Evaluate in a restricted environment
        result = eval(
            compile(tree, filename="<expr>", mode="eval"),
            {"__builtins__": None},
            _ALLOWED_NAMES,
        )
        return str(result)
    except Exception:
        # Any exception (parsing, validation, runtime) is treated as unsafe
        return "Unsafe Code Detected!"