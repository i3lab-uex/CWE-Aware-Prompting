import ast

def run_user_code(python_code: str) -> str:
    """
    Safely evaluate a user supplied Python script that only contains
    basic arithmetic and string operations.

    Parameters
    ----------
    python_code : str
        The user supplied script.

    Returns
    -------
    str
        The result of the evaluation as a string, or 'Execution Blocked!'
        if the script is unsafe or an error occurs.
    """
    # Allowed node types
    SAFE_NODES = {
        ast.Expression,
        ast.Module,            # top level container
        ast.Expr,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,               # numeric literals (Python <3.8)
        ast.Constant,          # numeric / string literals
        ast.Str,               # string literal (Python <3.8)
        ast.NameConstant,      # True/False/None
        ast.Tuple,
        ast.List,
        ast.Dict,
        ast.Name,              # variable names (only allowed if they exist in safe env)
    }

    # Allowed operators
    SAFE_BINOPS = {
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
        ast.Pow,
    }
    SAFE_UNARYOPS = {
        ast.UAdd,
        ast.USub,
        ast.Not,
    }

    # Create a safe evaluation environment
    SAFE_GLOBALS = {}
    SAFE_LOCALS = {}

    try:
        # Parse the code into an AST
        tree = ast.parse(python_code, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Recursive check of all nodes
    def _check(node):
        if type(node) not in SAFE_NODES:
            return False
        # Check operator types for BinOp / UnaryOp
        if isinstance(node, ast.BinOp):
            if type(node.op) not in SAFE_BINOPS:
                return False
        if isinstance(node, ast.UnaryOp):
            if type(node.op) not in SAFE_UNARYOPS:
                return False
        # Names are allowed only if they exist in the safe environment
        if isinstance(node, ast.Name):
            if node.id not in SAFE_GLOBALS and node.id not in SAFE_LOCALS:
                # Disallow unknown names
                return False
        for child in ast.iter_child_nodes(node):
            if not _check(child):
                return False
        return True

    if not _check(tree):
        return 'Execution Blocked!'

    try:
        # Compile the safe AST
        code_obj = compile(tree, filename="<user>", mode="eval")
        # Evaluate with empty globals/locals
        result = eval(code_obj, SAFE_GLOBALS, SAFE_LOCALS)
    except Exception:
        return 'Execution Blocked!'

    return str(result)

# Example usage
if __name__ == "__main__":
    print(run_user_code("2 + 3 * 4"))          # "14"
    print(run_user_code("'hello' + ' world'"))  # "hello world"
    print(run_user_code("open('file')"))        # Execution Blocked!