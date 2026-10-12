import ast
import sys
from contextlib import redirect_stdout
from io import StringIO

# List of AST node types that are considered unsafe
UNSAFE_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,                # Python 2 only, harmless for py3 but kept for clarity
    ast.Call,
    ast.Attribute,
)

# List of built‑in functions that are disallowed
DISALLOWED_BUILTINS = {
    "eval",
    "exec",
    "open",
    "compile",
    "input",
    "__import__",
    "globals",
    "locals",
    "vars",
}

class _SafetyVisitor(ast.NodeVisitor):
    def visit(self, node):
        # Reject unsafe nodes outright
        if isinstance(node, UNSAFE_NODES):
            raise ValueError(f"Disallowed construct: {type(node).__name__}")
        # For Call nodes, check if calling a disallowed builtin
        if isinstance(node, ast.Call):
            func = node.func
            # Handle simple name calls like eval()
            if isinstance(func, ast.Name) and func.id in DISALLOWED_BUILTINS:
                raise ValueError(f"Disallowed builtin call: {func.id}")
            # Handle attribute calls like __builtins__.eval()
            if isinstance(func, ast.Attribute):
                attr_name = func.attr
                if attr_name in DISALLOWED_BUILTINS:
                    raise ValueError(f"Disallowed builtin attribute call: {attr_name}")
        # Continue traversal
        super().visit(node)

def restricted_run_code(run_code: str):
    """
    Execute `run_code` in a sandboxed environment.
    
    Parameters
    ----------
    run_code : str
        The user supplied Python script.

    Returns
    -------
    str or None
        Captured stdout output, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the script contains syntax errors or uses disallowed constructs.
    """
    # 1. Syntax check & safety validation
    try:
        tree = ast.parse(run_code, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}")

    # Walk the AST to detect unsafe patterns
    _SafetyVisitor().visit(tree)

    # 2. Prepare restricted globals & locals
    safe_builtins = {k: v for k, v in __builtins__.__dict__.items()
                     if k not in DISALLOWED_BUILTINS}
    sandbox_globals = {"__builtins__": safe_builtins}

    # 3. Execute and capture stdout
    output = StringIO()
    try:
        with redirect_stdout(output):
            exec(compile(tree, filename="<restricted>", mode="exec"),
                 sandbox_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None

    result = output.getvalue()
    return result if result else None