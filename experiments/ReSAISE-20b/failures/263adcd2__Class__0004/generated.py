import ast

def evaluate_student_response(student_query: str) -> str:
    """
    Safely evaluates a simple Python expression supplied by the user.
    Only arithmetic, boolean and comparison operations are allowed.
    Any disallowed syntax or runtime error results in 'Error!'.
    """
    # Disallow dangerous nodes
    disallowed_nodes = (
        ast.Import, ast.ImportFrom, ast.Exec,  # exec is not in py3 AST
        ast.Call,          # function calls are disallowed
        ast.Attribute,     # attribute access
        ast.Subscript,     # indexing
        ast.Lambda,
        ast.FunctionDef,
        ast.ClassDef,
        ast.With, ast.AsyncWith,
        ast.Try, ast.ExceptHandler,
    )

    try:
        # Parse the expression
        tree = ast.parse(student_query, mode='eval')

        # Walk through nodes and reject disallowed ones
        for node in ast.walk(tree):
            if isinstance(node, disallowed_nodes):
                return 'Error!'

        # Prepare a safe evaluation environment
        safe_globals = {}
        safe_locals = {}

        # Evaluate the expression
        result = eval(compile(tree, filename="<ast>", mode="eval"),
                      safe_globals, safe_locals)

        return str(result)
    except Exception:
        # Any error (syntax, runtime, etc.) results in a generic error message
        return 'Error!'