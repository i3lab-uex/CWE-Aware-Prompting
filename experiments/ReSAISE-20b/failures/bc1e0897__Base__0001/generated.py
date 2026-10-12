import math
import ast

# Allowed names from the math module and a few built‑in constants.
_ALLOWED_NAMES = {
    name: getattr(math, name) for name in dir(math) if not name.startswith("_")
}
_ALLOWED_NAMES.update({
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
})

# Disallowed keywords that could lead to code injection.
_DISALLOWED_PATTERNS = (
    r"\b(import|exec|eval|open|compile|input|locals|globals|__.*__)\b",
)

class _SafeEvalVisitor(ast.NodeVisitor):
    """
    Traverses the AST and ensures that only safe nodes are present.
    Raises ValueError if an unsafe node is found.
    """
    def visit(self, node):
        # Reject any node that is not in the whitelist.
        if isinstance(node, (ast.Expression,
                             ast.BinOp, ast.UnaryOp, ast.BoolOp,
                             ast.Compare, ast.Call, ast.Name,
                             ast.Num, ast.Constant, ast.Load)):
            super().visit(node)
        else:
            raise ValueError(f"Disallowed expression: {ast.dump(node)}")

    def visit_Call(self, node):
        # Ensure the function being called is in the allowed names.
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in _ALLOWED_NAMES:
                raise ValueError(f"Disallowed function: {func_name}")
        else:
            raise ValueError("Only direct function calls are allowed.")
        self.generic_visit(node)

    def visit_Name(self, node):
        # Only allow names that are in the allowed dictionary.
        if node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Disallowed name: {node.id}")

def compute_expression(query_str: str) -> str:
    """
    Safely evaluate a mathematical expression supplied as a string.

    Parameters
    ----------
    query_str : str
        User provided expression to evaluate.

    Returns
    -------
    str
        The string representation of the result, or 'Error!' if evaluation fails.
    """
    # Quick syntax check for obvious malicious patterns
    import re
    if re.search(_DISALLOWED_PATTERNS, query_str):
        return "Error!"

    try:
        # Parse the expression into an AST
        expr_ast = ast.parse(query_str, mode="eval")

        # Validate the AST for safety
        _SafeEvalVisitor().visit(expr_ast)

        # Evaluate using a restricted globals dictionary
        result = eval(compile(expr_ast, "<string>", mode="eval"),
                      {"__builtins__": None}, _ALLOWED_NAMES)

        return str(result)
    except Exception:
        # Any error (parsing, safety check, evaluation) results in an error message
        return "Error!"