import ast
import builtins
from contextlib import redirect_stdout
from io import StringIO

# Whitelisted builtin functions that are safe to expose
SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'sum': sum,
    'min': min,
    'max': max,
    'abs': abs,
    'round': round,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'tuple': tuple,
    'dict': dict,
    'set': set,
}

# Node types that are considered safe
SAFE_NODE_TYPES = (
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Load,
    ast.Store,
    ast.Name,
    ast.Constant,
    ast.Num,          # for Python <3.8
    ast.Str,          # for Python <3.8
    ast.Bytes,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.Subscript,
    ast.Index,        # for Python <3.9
    ast.Slice,
    ast.Call,
)

# Operators considered safe (all of them are mathematical/logic ops)
SAFE_OPERATORS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitXor, ast.BitAnd, ast.MatMult,
    ast.And, ast.Or, ast.Not,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Is, ast.IsNot, ast.In, ast.NotIn,
    ast.UAdd, ast.USub,
)

def _validate_node(node):
    """Recursively validate that a node and its children are safe."""
    if not isinstance(node, SAFE_NODE_TYPES):
        raise ValueError(f"Forbidden node type: {type(node).__name__}")

    # Validate operators
    if isinstance(node, ast.BinOp) and not isinstance(node.op, SAFE_OPERATORS):
        raise ValueError(f"Forbidden binary operator: {type(node.op).__name__}")
    if isinstance(node, ast.UnaryOp) and not isinstance(node.op, SAFE_OPERATORS):
        raise ValueError(f"Forbidden unary operator: {type(node.op).__name__}")
    if isinstance(node, ast.BoolOp) and not isinstance(node.op, SAFE_OPERATORS):
        raise ValueError(f"Forbidden boolean operator: {type(node.op).__name__}")
    if isinstance(node, ast.Compare):
        for op in node.ops:
            if not isinstance(op, SAFE_OPERATORS):
                raise ValueError(f"Forbidden comparison operator: {type(op).__name__}")

    # Validate function calls
    if isinstance(node, ast.Call):
        func = node.func
        if not isinstance(func, ast.Name) or func.id not in SAFE_BUILTINS:
            raise ValueError(f"Forbidden function call: {ast.dump(node)}")

    # Recursively validate all child nodes
    for child in ast.iter_child_nodes(node):
        _validate_node(child)

def process_python_code(code_str: str):
    """
    Execute a user-provided Python code snippet in a restricted environment.

    Parameters
    ----------
    code_str : str
        The Python source to execute.

    Returns
    -------
    str or None
        Captured stdout output if any, otherwise None.

    Raises
    ------
    ValueError
        If the code contains forbidden operations or is syntactically invalid.
    """
    # Parse the source and ensure syntax is correct
    try:
        parsed = ast.parse(code_str, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from None

    # Validate the AST
    _validate_node(parsed)

    # Prepare a restricted global namespace
    safe_globals = {"__builtins__": SAFE_BUILTINS}

    # Capture stdout
    out = StringIO()
    try:
        with redirect_stdout(out):
            exec(compile(parsed, filename="<user_code>", mode="exec"), safe_globals)
    except Exception as exc:
        # Re-raise any runtime exception as ValueError for uniformity
        raise ValueError(f"Runtime error during execution: {exc}") from None

    result = out.getvalue()
    return result if result else None