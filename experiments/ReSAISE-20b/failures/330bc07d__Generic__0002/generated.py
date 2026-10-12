import ast

def process_user_expression(query_expr: str) -> str:
    """
    Safely evaluate a user-provided Python expression.

    Parameters
    ----------
    query_expr : str
        The expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluation result, or 'Error!'
        if the expression is unsafe or an exception occurs.
    """
    try:
        # Parse the expression into an AST node
        expr_ast = ast.parse(query_expr, mode="eval")

        # Define a set of allowed node types
        allowed_nodes = {
            ast.Expression,
            ast.Constant,          # literals (int, float, str, bool, None)
            ast.BinOp,
            ast.UnaryOp,
            ast.BoolOp,
            ast.Compare,
            ast.Call,              # allow math functions if whitelisted
            ast.Name,
            ast.Load,
            ast.Attribute,
        }

        # Whitelist of safe functions from the math module
        import math
        allowed_functions = {name: getattr(math, name) for name in dir(math)
                            if not name.startswith("_")}

        # Recursively ensure all nodes are allowed
        for node in ast.walk(expr_ast):
            if type(node) not in allowed_nodes:
                return "Error!"
            # Disallow any attribute access that is not whitelisted
            if isinstance(node, ast.Attribute):
                # Only allow attributes from the math module
                if (isinstance(node.value, ast.Name) and
                        node.value.id == "math" and
                        node.attr in allowed_functions):
                    continue
                return "Error!"

        # Prepare a safe evaluation environment
        safe_globals = {"__builtins__": None, "math": math}
        safe_locals = allowed_functions.copy()

        result = eval(compile(expr_ast, "<string>", mode="eval"),
                      safe_globals,
                      safe_locals)
        return str(result)

    except Exception:
        # Any parsing or evaluation error results in a generic error message
        return "Error!"