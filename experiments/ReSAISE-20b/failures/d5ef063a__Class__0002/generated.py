import ast
import sys
import io
from contextlib import redirect_stdout

# List of allowed AST node types (whitelist)
_ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Subscript,
    ast.Index,
    ast.Slice,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.FloorDiv, ast.Invert, ast.Not, ast.UAdd, ast.USub,
    # Comparisons
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Logical operators
    ast.And, ast.Or,
}

# Names that are allowed to appear in the code (whitelist)
_ALLOWED_NAMES = {
    'print',   # we provide a safe print
}

class _RestrictedNodeVisitor(ast.NodeVisitor):
    def visit(self, node):
        if type(node) not in _ALLOWED_NODES:
            raise ValueError(f"Disallowed node: {type(node).__name__}")
        super().visit(node)

    def visit_Name(self, node):
        if node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Disallowed name: {node.id}")
        super().visit(node)

def restricted_run_code(run_code: str):
    """
    Execute a user-provided Python script in a highly restricted environment.
    
    Parameters
    ----------
    run_code : str
        The Python script to execute.

    Returns
    -------
    str or None
        Captured standard output if any, otherwise None.

    Raises
    ------
    ValueError
        If the script contains syntax errors or disallowed operations.
    """
    # 1. Parse to AST and validate
    try:
        parsed = ast.parse(run_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}") from None

    try:
        _RestrictedNodeVisitor().visit(parsed)
    except ValueError as e:
        raise ValueError(f"Prohibited operation: {e}") from None

    # 2. Prepare restricted globals
    safe_globals = {
        '__builtins__': {},   # no built-ins by default
        'print': print,       # allow a safe print
    }

    # 3. Capture stdout
    out = io.StringIO()
    try:
        with redirect_stdout(out):
            exec(compile(parsed, filename="<restricted>", mode="exec"), safe_globals)
    except Exception as e:
        # Re‑raise any runtime errors as ValueError to keep the API simple
        raise ValueError(f"Runtime error: {e}") from None

    result = out.getvalue()
    return result if result else None