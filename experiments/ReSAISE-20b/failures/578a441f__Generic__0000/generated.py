import ast
from types import SimpleNamespace

# Define a whitelist of safe built‑in functions and constants
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'dict': dict,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'pow': pow,
    'range': range,
    'str': str,
    'sum': sum,
    # constants
    'True': True,
    'False': False,
    'None': None,
}

# Names that are explicitly forbidden
FORBIDDEN_NAMES = {
    '__import__',
    'open',
    'eval',
    'exec',
    'compile',
    '__file__',
    '__dict__',
    '__class__',
}

# Allowed AST node types
ALLOWED_NODE_TYPES = (
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.Name,
    ast.Constant,
    ast.Num,   # for Python <3.8
    ast.Str,   # for Python <3.8
    ast.Bytes,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.Call,
    ast.Lambda,
    ast.FunctionDef,
    ast.Return,
    ast.Pass,
    ast.Continue,
    ast.Break,
    ast.For,
    ast.While,
    ast.If,
    ast.With,
    ast.Await,
    ast.Yield,
    ast.YieldFrom,
    ast.Raise,
    ast.Try,
    ast.ExceptHandler,
    # literals
    ast.FormattedValue,
    ast.JoinedStr,
)

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and ensure that only safe nodes are present.
    Raises ValueError if a disallowed node or operation is found.
    """
    # Check the type of this node
    if not isinstance(node, ALLOWED_NODE_TYPES):
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Disallow import statements
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        raise ValueError("Import statements are not allowed")

    # Disallow calls to forbidden names
    if isinstance(node, ast.Call):
        func = node.func
        # Only allow calls to safe builtins via Name nodes
        if isinstance(func, ast.Name):
            name = func.id
            if name not in SAFE_BUILTINS and name not in FORBIDDEN_NAMES:
                raise ValueError(f"Call to forbidden function '{name}'")
        else:
            # e.g., attribute access or lambda calls are disallowed
            raise ValueError("Only direct calls to whitelisted builtins are allowed")

    # Disallow usage of forbidden names in Name nodes
    if isinstance(node, ast.Name):
        if node.id in FORBIDDEN_NAMES:
            raise ValueError(f"Usage of forbidden name '{node.id}'")

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        _check_ast(child)

def run_user_script(user_script: str):
    """
    Execute a user supplied Python script in a restricted environment.

    Parameters
    ----------
    user_script : str
        The Python code to execute.

    Returns
    -------
    Any
        Result of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the script contains disallowed operations or syntax errors.
    """
    try:
        tree = ast.parse(user_script, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from None

    # Validate the AST
    try:
        _check_ast(tree)
    except ValueError as exc:
        raise ValueError(f"Disallowed content in script: {exc}") from None

    # Prepare a restricted execution environment
    exec_globals = {'__builtins__': SAFE_BUILTINS}
    exec_locals = {}

    # If the last node is an expression, evaluate it separately
    result = None
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        # Compile the expression only
        expr_code = compile(ast.Expression(tree.body[-1].value), '<string>', 'eval')
        try:
            result = eval(expr_code, exec_globals, exec_locals)
        except Exception as exc:
            raise ValueError(f"Error evaluating expression: {exc}") from None
        # Remove the expression node before executing remaining statements
        body = tree.body[:-1]
    else:
        body = tree.body

    # Compile and execute the remaining statements
    if body:
        stmt_code = compile(ast.Module(body, type_ignores=[]), '<string>', 'exec')
        try:
            exec(stmt_code, exec_globals, exec_locals)
        except Exception as exc:
            raise ValueError(f"Error executing script: {exc}") from None

    return result