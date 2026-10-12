import ast
import builtins
from contextlib import redirect_stdout
from io import StringIO


# --------------------------------------------------------------------------- #
# 1. Allowed AST node types – everything else is considered unsafe
# --------------------------------------------------------------------------- #
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Constant,          # literals: numbers, strings, bools, None
    ast.BinOp,
    ast.UnaryOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.FloorDiv,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitXor,
    ast.BitAnd,
    ast.USub,
    ast.UAdd,
    ast.IfExp,
    ast.Compare,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.And,
    ast.Or,
    ast.Not,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Index,             # for subscript support
    ast.Subscript,
    ast.Slice,
    ast.keyword,
}

# --------------------------------------------------------------------------- #
# 2. Forbidden built‑in names – any attempt to use them raises an error
# --------------------------------------------------------------------------- #
FORBIDDEN_BUILTINS = {
    'open', 'exec', 'eval', '__import__',
    'compile', 'input', 'locals', 'globals',
    'dir', 'vars', 'help', 'quit', 'exit'
}

# --------------------------------------------------------------------------- #
# 3. Visitor to check that the AST contains only allowed nodes
# --------------------------------------------------------------------------- #
class SafeVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        if type(node) not in ALLOWED_NODES:
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id in FORBIDDEN_BUILTINS:
            raise ValueError(f"Forbidden built‑in used: {node.id}")
        super().visit_Name(node)

    def visit_Call(self, node):
        # Disallow calls to forbidden built‑ins
        if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_BUILTINS:
            raise ValueError(f"Forbidden function call: {node.func.id}")
        super().visit_Call(node)

# --------------------------------------------------------------------------- #
# 4. Main evaluation function
# --------------------------------------------------------------------------- #
def evaluate_user_input(user_code: str):
    """
    Safely execute a small user‑supplied Python script.

    Parameters
    ----------
    user_code : str
        The code to execute. Must not contain disallowed syntax or built‑ins.

    Returns
    -------
    str | None
        The captured stdout output, or ``None`` if nothing was printed.

    Raises
    ------
    ValueError
        If the code contains forbidden syntax, a disallowed built‑in,
        or if it fails to compile.
    """
    # 1. Parse the code – this will raise SyntaxError if it is invalid
    try:
        tree = ast.parse(user_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user code: {e}") from None

    # 2. Validate the AST
    try:
        SafeVisitor().visit(tree)
    except ValueError as e:
        raise ValueError(f"User code is unsafe: {e}") from None

    # 3. Prepare a restricted execution environment
    safe_globals = {
        '__builtins__': {k: getattr(builtins, k) for k in dir(builtins)
                         if k not in FORBIDDEN_BUILTINS and not k.startswith('__')}
    }
    safe_locals = {}

    # 4. Execute the code while capturing stdout
    out_stream = StringIO()
    try:
        with redirect_stdout(out_stream):
            exec(compile(tree, filename='<user>', mode='exec'), safe_globals, safe_locals)
    except Exception as e:
        # Wrap any runtime error into ValueError to keep a consistent API
        raise ValueError(f"Execution failed: {e}") from None

    output = out_stream.getvalue()
    return output if output else None