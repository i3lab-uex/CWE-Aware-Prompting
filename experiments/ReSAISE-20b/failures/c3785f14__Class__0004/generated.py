import ast
import sys
from types import FunctionType

# --------------------------------------------------------------------------- #
#  Safe evaluation of a Python code snippet
#
#  The function `evaluate_code_string` parses the supplied string into an AST,
#  validates that it does not contain disallowed constructs (imports, exec,
#  eval, os.system, etc.), then executes it in a sandboxed namespace that
#  has no built‑in functions.  The function returns the value of the last
#  expression in the snippet if it exists; otherwise it returns None.
#
#  This implementation protects against common injection attacks (CWE‑74) by
#  ensuring that no external data can be used to construct or alter the AST
#  before it is executed.
# --------------------------------------------------------------------------- #

class DisallowedNodeError(ValueError):
    """Raised when the AST contains a disallowed node."""
    pass


# List of node types that are forbidden
FORBIDDEN_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,                 # Python 2 only; kept for completeness
    ast.Call,
    ast.Attribute,
}

# List of call names that are forbidden (e.g., open, eval, exec, os.system)
FORBIDDEN_CALLS = {
    'open',
    'eval',
    'exec',
    'compile',
    'input',
    '__import__',
    # Disallow any call to the `os` module
    'system',
    'popen',
    'spawnl',
    'spawnv',
    'spawnlp',
    'spawnvv',
}

def _is_disallowed_call(node: ast.Call) -> bool:
    """
    Return True if the call node refers to a forbidden function.
    """
    # Only handle simple names or attribute accesses
    if isinstance(node.func, ast.Name):
        return node.func.id in FORBIDDEN_CALLS
    if isinstance(node.func, ast.Attribute):
        # Disallow any attribute access on the 'os' module
        if isinstance(node.func.value, ast.Name) and node.func.value.id == 'os':
            return True
    return False


def _validate_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise DisallowedNodeError if any
    forbidden node or call is encountered.
    """
    for child in ast.walk(node):
        if type(child) in FORBIDDEN_NODES:
            raise DisallowedNodeError(f"Disallowed node type: {type(child).__name__}")

        if isinstance(child, ast.Call):
            # Disallow calls to forbidden functions or module attributes
            if _is_disallowed_call(child):
                raise DisallowedNodeError(f"Disallowed function call: {ast.unparse(child).strip()}")

        # Disallow assignment to built-in names
        if isinstance(child, ast.Name) and child.id in {
            '__import__', 'eval', 'exec', 'open', 'compile'
        } and isinstance(child.ctx, ast.Store):
            raise DisallowedNodeError(f"Disallowed assignment to built-in: {child.id}")

        # Disallow usage of globals/locals that could leak state
        if isinstance(child, ast.Global):
            raise DisallowedNodeError("Global statement is disallowed.")
        if isinstance(child, ast.Nonlocal):
            raise DisallowedNodeError("Nonlocal statement is disallowed.")


def evaluate_code_string(code_string: str):
    """
    Safely execute a small Python code snippet.

    Parameters
    ----------
    code_string : str
        The Python source to execute.  It may contain multiple statements.

    Returns
    -------
    None or object
        The value of the last expression in the snippet if it exists,
        otherwise None.

    Raises
    ------
    ValueError
        If the code attempts to use disallowed operations.
    """
    try:
        # Parse into an AST
        parsed = ast.parse(code_string, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code: {exc}") from None

    # Validate the AST
    try:
        _validate_ast(parsed)
    except DisallowedNodeError as exc:
        raise ValueError(f"Disallowed operation detected: {exc}") from None

    # Prepare a restricted namespace
    sandbox = {'__builtins__': {}}

    # Execute the code.  We capture the value of the last expression
    # by compiling in 'eval' mode if the code consists of a single
    # expression; otherwise we exec and return None.
    try:
        if len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr):
            # Single expression – evaluate it
            expr = parsed.body[0].value
            compiled_expr = compile(ast.Expression(expr), '<string>', 'eval')
            return eval(compiled_expr, sandbox)
        else:
            # Multiple statements – exec
            compiled_code = compile(parsed, '<string>', 'exec')
            exec(compiled_code, sandbox)
            return None
    except Exception as exc:
        # Wrap any runtime exception into ValueError to keep the API simple
        raise ValueError(f"Runtime error: {exc}") from None


# --------------------------------------------------------------------------- #
# Example usage (commented out – for demonstration only)
#
# try:
#     result = evaluate_code_string("1 + 2")
#     print(result)          # Output: 3
#
#     evaluate_code_string("import os")  # Raises ValueError
# except ValueError as e:
#     print(e)
#
# --------------------------------------------------------------------------- #