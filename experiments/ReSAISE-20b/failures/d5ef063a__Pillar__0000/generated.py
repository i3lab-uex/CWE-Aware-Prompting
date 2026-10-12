import ast
import sys
from contextlib import redirect_stdout
from io import StringIO

# --------------------------------------------------------------------------- #
#   Safe execution environment                                               #
# --------------------------------------------------------------------------- #

ALLOWED_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'abs': abs,
    'sum': sum,
    'min': min,
    'max': max,
    'bool': bool,
    'int': int,
    'float': float,
    'str': str,
    'list': list,
    'dict': dict,
    'set': set,
    'tuple': tuple,
}

# Whitelist of allowed AST node types
ALLOWED_NODES = {
    ast.Module, ast.Expr,
    ast.Assign, ast.AugAssign,
    ast.Name, ast.Load, ast.Store,
    ast.Constant,
    ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
    ast.If, ast.For, ast.While,
    ast.Call, ast.keyword,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.UAdd, ast.USub,
    ast.And, ast.Or, ast.Not,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Containers
    ast.List, ast.Tuple, ast.Dict, ast.Set,
    ast.Subscript, ast.Index, ast.Slice,
}

# Disallowed node types (explicit for clarity)
DISALLOWED_NODES = {
    ast.Import, ast.ImportFrom,
    ast.FunctionDef, ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.Lambda,
    ast.With, ast.Raise,
    ast.Try, ast.ExceptHandler,
    ast.Global, ast.Nonlocal,
    ast.Delete,
    ast.Attribute,  # disallow attribute access (e.g., os.system)
}

class _SafeNodeVisitor(ast.NodeVisitor):
    def __init__(self, allowed_names):
        self.allowed_names = set(allowed_names)

    def generic_visit(self, node):
        # Reject disallowed nodes outright
        if type(node) in DISALLOWED_NODES:
            raise ValueError(f"Disallowed construct: {type(node).__name__}")
        # Reject any node not explicitly allowed
        if type(node) not in ALLOWED_NODES:
            raise ValueError(f"Unsupported syntax: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node):
        # Ensure function name is a simple identifier and in allowed list
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct function calls are allowed")
        if node.func.id not in self.allowed_names:
            raise ValueError(f"Call to disallowed function: {node.func.id}")
        # Arguments are checked recursively
        self.generic_visit(node)

    def visit_Name(self, node):
        # Allow usage of built-in names; variables are allowed to be created
        if isinstance(node.ctx, ast.Load) and node.id not in self.allowed_names:
            # Variable usage is allowed; it's fine
            pass
        super().visit_Name(node)

def _validate_script(code_str, allowed_names):
    """
    Validate that the AST of code_str contains only safe constructs.
    Raises ValueError on any disallowed syntax or function call.
    """
    try:
        tree = ast.parse(code_str, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from exc

    visitor = _SafeNodeVisitor(allowed_names)
    visitor.visit(tree)

def restricted_run_code(run_code: str):
    """
    Execute a user-provided Python script in a highly restricted environment.

    Parameters
    ----------
    run_code : str
        The Python code to execute.

    Returns
    -------
    output : str | None
        Captured stdout output if any; otherwise None.

    Raises
    ------
    ValueError
        If the script contains disallowed constructs or has syntax errors.
    """
    # Step 1: Validate the code
    _validate_script(run_code, ALLOWED_BUILTINS.keys())

    # Step 2: Prepare restricted globals
    safe_globals = {'__builtins__': ALLOWED_BUILTINS}
    # No locals are provided; everything is global
    safe_locals = {}

    # Step 3: Capture stdout
    output_stream = StringIO()
    try:
        with redirect_stdout(output_stream):
            exec(run_code, safe_globals, safe_locals)
    except Exception as exc:
        # Any runtime error is surfaced as ValueError
        raise ValueError(f"Runtime error in user script: {exc}") from exc

    output = output_stream.getvalue()
    return output if output else None