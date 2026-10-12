import ast
import sys
from types import ModuleType, FunctionType

# --------------------------------------------------------------------------- #
#   Safety utilities
# --------------------------------------------------------------------------- #

class ForbiddenOperationError(ValueError):
    """Raised when the code attempts a disallowed operation."""


def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ForbiddenOperationError if a node
    that would perform an unsafe operation is found.
    """
    # Disallowed nodes
    forbidden_nodes = (
        ast.Import,
        ast.ImportFrom,
        ast.With,          # prevents 'with open(...) as f'
        ast.Call,          # calls are checked more specifically below
    )

    if isinstance(node, forbidden_nodes):
        raise ForbiddenOperationError(f"Disallowed construct: {type(node).__name__}")

    # Disallow calls to dangerous builtins
    if isinstance(node, ast.Call):
        func = node.func
        # Only allow attribute access on objects we know are safe
        if isinstance(func, ast.Name):
            if func.id in {"open", "eval", "exec", "__import__", "compile"}:
                raise ForbiddenOperationError(f"Disallowed function call: {func.id}")
        elif isinstance(func, ast.Attribute):
            # e.g., os.system
            if func.attr in {"system", "popen"}:
                raise ForbiddenOperationError(f"Disallowed attribute call: {func.attr}")

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        _check_ast(child)


def _create_safe_builtins():
    """
    Return a dictionary of built-ins that are considered safe for
    educational contexts. This excludes anything that can perform I/O,
    modify the environment, or otherwise compromise safety.
    """
    allowed = {
        "abs": abs,
        "all": all,
        "any": any,
        "bool": bool,
        "chr": chr,
        "divmod": divmod,
        "float": float,
        "hash": hash,
        "int": int,
        "len": len,
        "max": max,
        "min": min,
        "pow": pow,
        "range": range,
        "round": round,
        "str": str,
        "sum": sum,
        "tuple": tuple,
        "enumerate": enumerate,
        "zip": zip,
        # small math functions
        "math": __import__("math"),
    }
    return allowed


# --------------------------------------------------------------------------- #
#   Main function
# --------------------------------------------------------------------------- #

def process_python_code(code_str: str):
    """
    Execute a Python code snippet safely.

    Parameters
    ----------
    code_str : str
        The user-provided Python code to be executed.

    Returns
    -------
    Any or None
        The value of the last expression in the snippet if it produces one,
        otherwise ``None``.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or invalid syntax.
    """
    if not isinstance(code_str, str):
        raise ValueError("code_str must be a string")

    try:
        # Parse the code to an AST
        tree = ast.parse(code_str, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from exc

    # Check for disallowed constructs
    try:
        _check_ast(tree)
    except ForbiddenOperationError as exc:
        raise ValueError(f"Forbidden operation detected: {exc}") from exc

    # Prepare restricted execution environment
    safe_builtins = _create_safe_builtins()
    exec_globals: dict = {"__builtins__": safe_builtins}
    exec_locals: dict = {}

    # Execute the code
    try:
        exec(compile(tree, filename="<safe>", mode="exec"), exec_globals, exec_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    # If the last node is an expression, evaluate and return its value
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        expr_code = compile(ast.Expression(body=tree.body[-1].value), filename="<safe>", mode="eval")
        try:
            return eval(expr_code, exec_globals, exec_locals)
        except Exception as exc:
            raise ValueError(f"Evaluation error: {exc}") from exc

    return None