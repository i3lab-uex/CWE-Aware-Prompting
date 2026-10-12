import ast
import math

# ----------------------------------------------------------------------
# Safe expression evaluator
# ----------------------------------------------------------------------


class _SafeEvaluator(ast.NodeVisitor):
    """
    AST visitor that ensures only safe mathematical expressions are allowed.
    Allowed nodes:
        - Expression, BinOp, UnaryOp, Call
        - Numbers (int/float)
        - Name only for allowed math functions
    All other nodes will raise a ValueError.
    """

    # Whitelisted names from the math module
    _allowed_names = {
        name for name in dir(math)
        if not name.startswith("_") and callable(getattr(math, name))
    }

    def visit(self, node):
        if isinstance(node, ast.Expression):
            self.generic_visit(node)
        elif isinstance(node, (ast.BinOp, ast.UnaryOp)):
            self.generic_visit(node)
        elif isinstance(node, ast.Call):
            # Only allow calls to whitelisted math functions
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only simple function calls allowed")
            if node.func.id not in self._allowed_names:
                raise ValueError(f"Function '{node.func.id}' is not allowed")
            self.generic_visit(node)
        elif isinstance(node, (ast.Num, ast.Constant)):
            # Constant numbers are allowed
            if not isinstance(getattr(node, "value", None), (int, float)):
                raise ValueError("Only numeric constants allowed")
        else:
            # Any other node type is disallowed
            raise ValueError(f"Disallowed expression: {ast.dump(node)}")

    def generic_visit(self, node):
        super().generic_visit(node)


def secure_expression_evaluator(expr_input: str) -> str:
    """
    Safely evaluate a mathematical expression provided as a string.

    Parameters
    ----------
    expr_input : str
        The user supplied expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Unsafe Code Detected!'
        if the expression contains disallowed content or evaluation fails.

    Raises
    ------
    ValueError
        If the expression contains unsafe constructs.
    """
    try:
        # Parse into an AST; raise SyntaxError if invalid
        parsed = ast.parse(expr_input, mode="eval")

        # Validate the AST
        _SafeEvaluator().visit(parsed)

        # Prepare safe globals: only math module, no builtins
        safe_globals = {"__builtins__": None, "math": math}
        # Evaluate the expression
        result = eval(compile(parsed, "<string>", mode="eval"), safe_globals)

        return str(result)
    except Exception:
        # Any exception (syntax, validation, eval) is treated as unsafe
        return "Unsafe Code Detected!"