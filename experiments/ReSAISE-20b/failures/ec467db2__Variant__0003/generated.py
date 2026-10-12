import ast

def execute_user_code(user_code: str) -> str:
    """
    Safely evaluate a simple Python expression that may contain arithmetic or
    string operations.  If the code contains any disallowed nodes, return
    'Execution Blocked!'.

    Parameters:
        user_code (str): The user supplied Python expression.

    Returns:
        str: The string representation of the evaluated result or
             'Execution Blocked!' if unsafe.
    """
    # Allowed node types for the abstract syntax tree
    SAFE_NODES = {
        ast.Expression,   # top level
        ast.BinOp,        # + - * / // % ** << >> & | ^ ~
        ast.UnaryOp,      # + - ~
        ast.BoolOp,       # and/or
        ast.Compare,      # == != < <= > >=
        ast.Call,         # disallowed – we will reject any call node
        ast.Attribute,    # disallowed – no attribute access
        ast.Name,         # only allowed if it is a literal constant (like True/False)
        ast.Constant,     # literals: numbers, strings, bools
        ast.Num,          # legacy numeric constants (Python <3.8)
        ast.Str,          # legacy string constants
        ast.NameConstant, # True/False/None in older Python versions
        ast.List,         # disallow lists (no element access)
        ast.Tuple,
        ast.Dict,
    }

    try:
        # Parse the code into an AST
        tree = ast.parse(user_code, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Walk the tree and reject disallowed nodes
    for node in ast.walk(tree):
        if not isinstance(node, tuple(SAFE_NODES)):
            return 'Execution Blocked!'

        # Disallow any function calls
        if isinstance(node, ast.Call):
            return 'Execution Blocked!'

        # Disallow attribute access (e.g., obj.method)
        if isinstance(node, ast.Attribute):
            return 'Execution Blocked!'

        # Disallow list/tuple/dict construction or indexing
        if isinstance(node, (ast.List, ast.Tuple, ast.Dict)):
            return 'Execution Blocked!'

    # Prepare a very restricted eval environment
    safe_globals = {}
    safe_locals = {}

    try:
        result = eval(compile(tree, filename="<ast>", mode="eval"),
                      safe_globals, safe_locals)
    except Exception:
        return 'Execution Blocked!'

    # Convert the result to string for consistent output
    return str(result)