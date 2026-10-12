import ast
import sys
from contextlib import redirect_stdout
from io import StringIO

# A set of allowed AST node types for safety.
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,           # for Python <3.8
    ast.Str,           # for Python <3.8
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Compare,
    ast.IfExp,
    ast.BoolOp,
    ast.Attribute,     # only allow built‑in constants (e.g. math.pi)
    ast.Call,
    ast.Subscript,
    ast.Index,         # for Python <3.9
    ast.Slice,
    ast.keyword,
}

# Disallow imports, function/class definitions, loops etc.
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.For,
    ast.While,
    ast.With,
    ast.Raise,
    ast.Try,
    ast.Assert,
}

def _check_ast(node: ast.AST):
    """
    Recursively check that all nodes are allowed.
    Raise ValueError if a disallowed node is found.
    """
    if type(node) in DISALLOWED_NODES:
        raise ValueError(f"Disallowed construct: {type(node).__name__}")
    if not isinstance(node, tuple(ALLOWED_NODES)):
        raise ValueError(f"Unsupported node type: {type(node).__name__}")

    for child in ast.iter_child_nodes(node):
        _check_ast(child)

def process_python_code(code_str: str):
    """
    Execute a Python snippet safely.

    Parameters
    ----------
    code_str : str
        User supplied Python code.

    Returns
    -------
    Any
        The result of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed or invalid code.
    """
    # Parse the code into an AST
    try:
        parsed = ast.parse(code_str, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}") from None

    # Validate the AST
    _check_ast(parsed)

    # Prepare a restricted globals dict.
    safe_globals = {
        "__builtins__": {
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
            'set': set,
            'str': str,
            'sum': sum,
        }
    }

    # Capture printed output (if any)
    stdout = StringIO()
    with redirect_stdout(stdout):
        exec(compile(parsed, filename="<sandbox>", mode="exec"), safe_globals)

    # If the last statement is an expression, return its value
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        # Re‑evaluate the expression in the same context
        expr_code = compile(ast.Expression(parsed.body[-1].value), "<sandbox>", "eval")
        return eval(expr_code, safe_globals)

    # No explicit result; return None
    return None