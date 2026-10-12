import ast
import math

def run_safe_math_expression(math_exp: str) -> str:
    """
    Safely evaluate a mathematical expression in Python syntax.

    Parameters
    ----------
    math_exp : str
        The mathematical expression to evaluate.

    Returns
    -------
    str
        String representation of the result or 'Unsafe Code Detected!' if the
        expression contains disallowed constructs.
    """
    # Allowed AST node types
    ALLOWED_NODES = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python >=3.8
        ast.Name,
        ast.Attribute,
        ast.Call,         # only allowed for math functions
    )

    # Allowed operators
    ALLOWED_BINOPS = (
        ast.Add, ast.Sub, ast.Mult,
        ast.Div, ast.Mod, ast.Pow, ast.FloorDiv
    )
    ALLOWED_UNARYOPS = (ast.UAdd, ast.USub)

    # Allowed math functions
    ALLOWED_MATH_FUNCS = {
        name for name in dir(math)
        if not name.startswith("_") and callable(getattr(math, name))
    }

    try:
        # Parse expression to AST
        tree = ast.parse(math_exp, mode='eval')

        # Recursive node validation
        def _validate(node: ast.AST):
            if not isinstance(node, ALLOWED_NODES):
                raise ValueError(f"Disallowed node type: {type(node).__name__}")

            # Validate binary operators
            if isinstance(node, ast.BinOp):
                if not isinstance(node.op, ALLOWED_BINOPS):
                    raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")

            # Validate unary operators
            if isinstance(node, ast.UnaryOp):
                if not isinstance(node.op, ALLOWED_UNARYOPS):
                    raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")

            # Validate attribute access
            if isinstance(node, ast.Attribute):
                if not (isinstance(node.value, ast.Name) and node.value.id == "math"):
                    raise ValueError("Only 'math' module attributes are allowed")
                if node.attr not in ALLOWED_MATH_FUNCS:
                    raise ValueError(f"Disallowed math function: {node.attr}")

            # Validate calls
            if isinstance(node, ast.Call):
                if not (isinstance(node.func, ast.Attribute) and
                        isinstance(node.func.value, ast.Name) and node.func.value.id == "math"):
                    raise ValueError("Only calls to math functions are allowed")
                if node.func.attr not in ALLOWED_MATH_FUNCS:
                    raise ValueError(f"Disallowed math function call: {node.func.attr}")

            # Validate names (only 'math')
            if isinstance(node, ast.Name):
                if node.id != "math":
                    raise ValueError(f"Only 'math' name is allowed, got {node.id}")

            # Recurse into child nodes
            for child in ast.iter_child_nodes(node):
                _validate(child)

        _validate(tree)

        # Prepare safe globals
        safe_globals = {"__builtins__": None, "math": math}

        # Evaluate the expression
        result = eval(compile(tree, filename="<ast>", mode="eval"), safe_globals)

        return str(result)

    except Exception:
        # Any error leads to unsafe detection
        return "Unsafe Code Detected!"