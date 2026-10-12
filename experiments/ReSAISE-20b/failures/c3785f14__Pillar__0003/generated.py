import ast
from typing import Any

# ----------------------------------------------------------------------
#   Restricted execution helpers
# ----------------------------------------------------------------------


class _DisallowedNodeVisitor(ast.NodeVisitor):
    """
    Traverses an AST and raises ValueError if any disallowed node is found.
    """

    DISALLOWED_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,          # Python 2 legacy (not present in Py3)
        ast.Call,
    )

    DISALLOWED_FUNCTIONS = {
        'eval',
        'exec',
        '__import__',
        'open',
        'input',
        'compile',
        'locals',
        'globals',
    }

    def visit(self, node: ast.AST) -> Any:
        if isinstance(node, self.DISALLOWED_NODES):
            raise ValueError(f"Disallowed operation: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        # Disallow calls to forbidden built‑ins
        if isinstance(node.func, ast.Name) and node.func.id in self.DISALLOWED_FUNCTIONS:
            raise ValueError(f"Disallowed function call: {node.func.id}")
        self.generic_visit(node)


def _is_expression(code_str: str) -> bool:
    """
    Return True if the code is a single expression (not a statement block).
    """
    try:
        parsed = ast.parse(code_str, mode='eval')
    except SyntaxError:
        return False
    # Ensure no additional statements are present
    if len(parsed.body) != 1:
        return False
    return True


# ----------------------------------------------------------------------
#   Main function
# ----------------------------------------------------------------------


def evaluate_code_string(code_string: str) -> Any:
    """
    Safely evaluates a small Python code snippet.

    Parameters
    ----------
    code_string : str
        The Python code to run.  It may contain either a single expression
        or a small block of statements.

    Returns
    -------
    Any
        The result of evaluating the expression, or None if the code has no
        return value.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    if not isinstance(code_string, str):
        raise TypeError("code_string must be a string")

    # Strip leading/trailing whitespace
    code = code_string.strip()
    if not code:
        return None

    # ------------------------------------------------------------------
    #   1. Parse and check for disallowed syntax
    # ------------------------------------------------------------------
    try:
        parsed = ast.parse(code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python syntax: {exc}") from None

    # Validate AST
    _DisallowedNodeVisitor().visit(parsed)

    # ------------------------------------------------------------------
    #   2. Prepare a restricted execution environment
    # ------------------------------------------------------------------
    safe_builtins = {
        'range': range,
        'len': len,
        'int': int,
        'float': float,
        'str': str,
        'bool': bool,
        'list': list,
        'dict': dict,
        'set': set,
        'tuple': tuple,
        'sum': sum,
        'min': min,
        'max': max,
        'abs': abs,
        'print': print,          # allow printing
    }

    exec_globals = {"__builtins__": safe_builtins}
    exec_locals: dict[str, Any] = {}

    # ------------------------------------------------------------------
    #   3. Execute or evaluate
    # ------------------------------------------------------------------
    if _is_expression(code):
        # Single expression: use eval to get the value
        return eval(compile(parsed, filename="<string>", mode="eval"), exec_globals, exec_locals)
    else:
        # Block of statements: use exec
        exec(compile(parsed, filename="<string>", mode="exec"), exec_globals, exec_locals)
        return None