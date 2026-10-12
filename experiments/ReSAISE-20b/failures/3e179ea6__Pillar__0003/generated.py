import ast
from typing import Any

# Allowed AST node types for safe mathematical expressions
_ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python >=3.8
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.Mod,
    ast.FloorDiv,
    ast.UAdd,
    ast.USub,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitAnd,
    ast.BitXor,
    ast.LParen,       # not a real node but placeholder for readability
}

class SafeEvaluator(ast.NodeVisitor):
    """
    AST visitor that ensures the expression contains only safe nodes.
    """
    def visit(self, node: ast.AST) -> Any:
        if type(node) not in _ALLOWED_NODES:
            raise ValueError(f"Disallowed node: {type(node).__name__}")
        return super().visit(node)

    def visit_Name(self, node: ast.Name):
        # Disallow variable names
        raise ValueError("Names are not allowed")

    def visit_Call(self, node: ast.Call):
        # Disallow function calls
        raise ValueError("Function calls are not allowed")

    def visit_Attribute(self, node: ast.Attribute):
        # Disallow attribute access
        raise ValueError("Attribute access is not allowed")

    def visit_Subscript(self, node: ast.Subscript):
        # Disallow subscripting
        raise ValueError("Subscripts are not allowed")

    def visit_List(self, node: ast.List):
        raise ValueError("Lists are not allowed")

    def visit_Tuple(self, node: ast.Tuple):
        raise ValueError("Tuples are not allowed")

    def visit_Dict(self, node: ast.Dict):
        raise ValueError("Dictionaries are not allowed")

    def visit_Set(self, node: ast.Set):
        raise ValueError("Sets are not allowed")

def evaluate_expression_safely(expression: str) -> str:
    """
    Safely evaluates a mathematical expression given as a string.
    Returns the result as a string or 'Unsafe Code Detected!' if
    the expression contains disallowed constructs or an error occurs.
    """
    try:
        # Parse into an AST
        parsed = ast.parse(expression, mode="eval")

        # Verify safety
        SafeEvaluator().visit(parsed)

        # Compile and evaluate with empty globals/locals
        code = compile(parsed, "<string>", "eval")
        result = eval(code, {}, {})

        return str(result)
    except Exception:
        # Any exception is treated as unsafe
        return "Unsafe Code Detected!"