import ast
import builtins
import sys
import types
from io import StringIO

# --- Whitelist of allowed AST node types ------------------------------------
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Load,
    ast.Store,
    ast.Name,
    ast.Constant,
    ast.Num,          # for Python <3.8
    ast.Str,          # for Python <3.8
    ast.Bytes,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.keyword,
    ast.IfExp,        # conditional expression
    ast.Subscript,
    ast.Index,
    ast.Slice,
    ast.Attribute,
}

# Operators that are considered safe
SAFE_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod,
    ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitAnd, ast.BitXor,
    ast.And, ast.Or, ast.Not,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Is, ast.IsNot, ast.In, ast.NotIn,
}

# Builtins that are allowed
SAFE_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'bytes',
    'chr', 'complex', 'dict', 'float', 'hash',
    'hex', 'int', 'len', 'list', 'max', 'min',
    'pow', 'range', 'repr', 'round', 'str', 'sum',
    'tuple', 'zip',
}

def _is_safe_node(node: ast.AST) -> bool:
    """Recursively check that the node tree contains only allowed constructs."""
    if type(node) not in ALLOWED_NODES:
        return False
    # Check operators
    if isinstance(node, ast.BinOp) and type(node.op) not in SAFE_OPERATORS:
        return False
    if isinstance(node, ast.UnaryOp) and type(node.op) not in SAFE_OPERATORS:
        return False
    if isinstance(node, ast.BoolOp) and type(node.op) not in SAFE_OPERATORS:
        return False
    if isinstance(node, ast.Compare):
        for op in node.ops:
            if type(op) not in SAFE_OPERATORS:
                return False
    # Attribute access: only allow builtins
    if isinstance(node, ast.Attribute):
        return False  # disallow attribute access entirely

    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

def run_python_snippet(snippet_string: str):
    """
    Execute a user‑supplied Python snippet in a restricted environment.
    
    Parameters
    ----------
    snippet_string : str
        The Python code to run.

    Returns
    -------
    object or None
        Result of the last expression in the snippet, if any; otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or attempts forbidden operations.
    """
    # Parse and validate syntax
    try:
        parsed = ast.parse(snippet_string, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python syntax: {exc}") from None

    if not _is_safe_node(parsed):
        raise ValueError("Snippet contains disallowed operations or syntax.")

    # Prepare a safe global namespace
    safe_globals = {name: getattr(builtins, name) for name in SAFE_BUILTINS}
    safe_globals['__builtins__'] = {}  # prevent access to other builtins

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = StringIO()
    try:
        sys.stdout = fake_out
        exec(compile(parsed, filename='<snippet>', mode='exec'), safe_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    # If the snippet produced a value via print, return that string
    if output:
        return output.rstrip('\n')
    # Otherwise try to find the last expression value
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        # Evaluate the last expression in safe globals
        expr_code = compile(ast.Expression(parsed.body[-1].value), filename='<expr>', mode='eval')
        try:
            return eval(expr_code, safe_globals)
        except Exception as exc:
            raise ValueError(f"Evaluation error: {exc}") from None
    return None