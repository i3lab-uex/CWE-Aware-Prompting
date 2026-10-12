import ast
from typing import Any

# Allowed operator types for arithmetic and string concatenation
ALLOWED_BINOPS = (
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
)

ALLOWED_UNARYOPS = (
    ast.UAdd,
    ast.USub,
)


class SafeEvaluator(ast.NodeVisitor):
    """
    AST visitor that ensures the expression only contains safe nodes.
    """

    def __init__(self):
        self.is_safe = True

    def generic_visit(self, node: ast.AST) -> Any:
        # Disallow any node that is not explicitly handled
        if isinstance(node, (ast.Module, ast.Expr)):
            return super().generic_visit(node)

        # Literals are allowed
        if isinstance(node, (ast.Constant, ast.Num, ast.Str)):
            return

        # Allow simple variable names that are constants
        if isinstance(node, ast.Name):
            # We do not allow any variable usage; only constants
            self.is_safe = False
            return

        # Binary operations
        if isinstance(node, ast.BinOp):
            if not isinstance(node.op, ALLOWED_BINOPS):
                self.is_safe = False
                return
            self.visit(node.left)
            self.visit(node.right)
            return

        # Unary operations
        if isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, ALLOWED_UNARYOPS):
                self.is_safe = False
                return
            self.visit(node.operand)
            return

        # Tuples, lists, dicts are disallowed
        if isinstance(node, (ast.Tuple, ast.List, ast.Dict)):
            self.is_safe = False
            return

        # Subscripts (e.g., indexing) are disallowed
        if isinstance(node, ast.Subscript):
            self.is_safe = False
            return

        # Function calls, attribute access, imports are disallowed
        if isinstance(node, (ast.Call, ast.Attribute)):
            self.is_safe = False
            return

        # Anything else is unsafe
        self.is_safe = False


def process_user_code(code_script: str) -> str:
    """
    Safely evaluate a small Python script containing arithmetic or string operations.

    Parameters
    ----------
    code_script : str
        The user supplied Python script. It should be a single expression or
        a series of simple statements that evaluate to a value.

    Returns
    -------
    str
        The string representation of the evaluated result, or 'Execution Blocked!'
        if the script contains unsafe constructs.
    """
    try:
        # Parse into an AST
        tree = ast.parse(code_script, mode="eval")
    except SyntaxError:
        # If the script is not a single expression, try as a module
        try:
            tree = ast.parse(code_script, mode="exec")
        except SyntaxError:
            return "Execution Blocked!"

    # Validate the AST
    validator = SafeEvaluator()
    validator.visit(tree)
    if not validator.is_safe:
        return "Execution Blocked!"

    # Execute in a completely empty environment
    try:
        compiled = compile(tree, filename="<user_script>", mode="eval")
        result: Any = eval(compiled, {"__builtins__": None}, {})
    except Exception:
        return "Execution Blocked!"

    # Convert result to string
    return str(result)