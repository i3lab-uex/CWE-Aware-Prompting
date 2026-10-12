import ast
import math

# List of allowed names from the math module
_ALLOWED_NAMES = {
    name for name in dir(math)
    if not name.startswith("_") and callable(getattr(math, name))
}
# Also allow basic constants like pi, e
_ALLOWED_NAMES.update({"pi", "e"})

class _MathValidator(ast.NodeVisitor):
    """
    Validate that the parsed AST only contains safe mathematical constructs.
    """

    def visit(self, node):
        method = getattr(self, f"visit_{node.__class__.__name__}", None)
        if method is None:
            raise ValueError(f"Unsupported node type: {node.__class__.__name__}")
        return method(node)

    def visit_Module(self, node):
        if len(node.body) != 1:
            raise ValueError("Only a single expression is allowed")
        return self.visit(node.body[0])

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_BinOp(self, node):
        # Allowed binary operators: + - * / // % **
        if not isinstance(node.op, (ast.Add, ast.Sub, ast.Mult,
                                    ast.Div, ast.FloorDiv, ast.Mod,
                                    ast.Pow)):
            raise ValueError("Disallowed binary operator")
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        # Allowed unary operators: + -
        if not isinstance(node.op, (ast.UAdd, ast.USub)):
            raise ValueError("Disallowed unary operator")
        self.visit(node.operand)

    def visit_Num(self, node):
        # Numbers are allowed
        pass

    def visit_Constant(self, node):
        if not isinstance(node.value, (int, float)):
            raise ValueError("Only numeric constants are allowed")

    def visit_Name(self, node):
        if node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Name '{node.id}' is not allowed")

    def visit_Call(self, node):
        # Only allow calls to math functions
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed")
        if node.func.id not in _ALLOWED_NAMES:
            raise ValueError(f"Function '{node.func.id}' is not allowed")
        for arg in node.args:
            self.visit(arg)
        if node.keywords:
            raise ValueError("Keyword arguments are not allowed")

    def generic_visit(self, node):
        # Disallow any other node types
        raise ValueError(f"Disallowed construct: {node.__class__.__name__}")

def evaluate_math_expression(math_expression: str) -> str:
    """
    Safely evaluate a mathematical expression written in Python syntax.
    Returns the result as a string or 'Unsafe Code Detected!' if validation fails.
    """
    try:
        # Parse the expression
        parsed = ast.parse(math_expression, mode="eval")

        # Validate AST
        _MathValidator().visit(parsed)

        # Prepare safe globals
        safe_globals = {"__builtins__": None}
        for name in _ALLOWED_NAMES:
            safe_globals[name] = getattr(math, name)

        # Evaluate
        result = eval(compile(parsed, filename="<ast>", mode="eval"),
                      safe_globals, {})
        return str(result)
    except Exception:
        # Any exception is treated as unsafe
        return "Unsafe Code Detected!"