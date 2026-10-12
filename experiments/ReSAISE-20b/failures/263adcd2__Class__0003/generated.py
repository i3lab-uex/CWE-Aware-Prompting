import ast

def evaluate_student_response(student_query: str) -> str:
    """
    Safely evaluates a simple Python expression provided by the user.
    
    Only numeric literals, boolean/None constants and arithmetic operators
    (+, -, *, /, //, %, **, unary +/-) are permitted. Any attempt to use
    disallowed names or constructs results in an 'Error!'.
    
    Parameters:
        student_query (str): The expression to evaluate.
    
    Returns:
        str: String representation of the result or 'Error!' on failure.
    """
    # Define a set of allowed AST node types
    ALLOWED_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python 3.8+
        ast.NameConstant, # For True/False/None in older versions
    }

    # Allowed binary operators
    ALLOWED_BINOPS = {
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.FloorDiv,
        ast.Mod,
        ast.Pow,
    }

    # Allowed unary operators
    ALLOWED_UNARYOPS = {
        ast.UAdd,
        ast.USub,
    }

    # Allowed names (none for safety)
    ALLOWED_NAMES = set()

    try:
        # Parse the expression
        tree = ast.parse(student_query, mode='eval')

        # Recursively validate nodes
        def _validate(node):
            if type(node) not in ALLOWED_NODES:
                raise ValueError(f"Disallowed node: {type(node).__name__}")

            if isinstance(node, ast.BinOp):
                if type(node.op) not in ALLOWED_BINOPS:
                    raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")
                _validate(node.left)
                _validate(node.right)

            elif isinstance(node, ast.UnaryOp):
                if type(node.op) not in ALLOWED_UNARYOPS:
                    raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
                _validate(node.operand)

            elif isinstance(node, ast.Name):
                if node.id not in ALLOWED_NAMES:
                    raise ValueError(f"Disallowed name: {node.id}")

            elif isinstance(node, (ast.Num, ast.Constant, ast.NameConstant)):
                # These are literals; no further validation needed
                pass

            else:
                # For any other node types that might appear (e.g., Call), raise error
                if not isinstance(node, ast.Expression):
                    raise ValueError(f"Unexpected node type: {type(node).__name__}")

        _validate(tree)

        # Evaluate safely with no globals or locals
        result = eval(compile(tree, filename="<ast>", mode="eval"), {}, {})

        return str(result)
    except Exception:
        # Any error, including syntax or disallowed content, results in 'Error!'
        return "Error!"