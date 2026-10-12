import ast
import sys
import io
from types import FunctionType

# Allowed AST node types – anything not listed will raise an error.
_ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.Return,
    ast.Import,  # We'll allow imports only from a whitelist
    ast.ImportFrom,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.If,
    ast.While,
    ast.For,
    ast.Call,
    ast.Attribute,
    ast.Subscript,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Lambda,
    ast.IfExp,
    ast.JoinedStr,
    ast.FormattedValue,
}

# Whitelisted modules that can be imported
_WHITELISTED_MODULES = {"math", "datetime"}

# Whitelisted built‑in functions
_WHITELISTED_BUILTINS = {
    "abs", "min", "max", "sum", "len", "range", "print",
    "str", "int", "float", "bool", "list", "dict", "set",
}

def _check_node(node):
    """Recursively check that all nodes are allowed."""
    if type(node) not in _ALLOWED_NODES:
        raise ValueError(f"Forbidden construct: {type(node).__name__}")
    for child in ast.iter_child_nodes(node):
        _check_node(child)

def _validate_imports(tree):
    """Ensure that only whitelisted modules are imported."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = node.names
            for alias in names:
                mod_name = alias.name.split('.')[0]
                if mod_name not in _WHITELISTED_MODULES:
                    raise ValueError(f"Import of module '{mod_name}' is forbidden")

def _prepare_namespace():
    """Create a safe execution namespace."""
    safe_builtins = {k: __builtins__[k] for k in _WHITELISTED_BUILTINS if k in __builtins__}
    return {"__builtins__": safe_builtins}

def evaluate_user_input(user_code: str):
    """
    Execute a user‑supplied Python script in a restricted environment.
    
    Parameters
    ----------
    user_code : str
        The Python code to execute.

    Returns
    -------
    Any
        The value of the last expression evaluated, or None if there is no output.

    Raises
    ------
    ValueError
        If the code contains forbidden syntax or constructs.
    """
    try:
        # Parse to AST and validate
        tree = ast.parse(user_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    _check_node(tree)
    _validate_imports(tree)

    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    try:
        namespace = _prepare_namespace()
        exec(compile(tree, filename="<user_script>", mode="exec"), namespace)
        # If the script defines a variable named '__result__', return it
        result = namespace.get("__result__")
    finally:
        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

    # If there was printed output but no explicit result, return that
    if result is None and output:
        return output.rstrip()
    return result

# Example usage
if __name__ == "__main__":
    code = """
import math
x = 10
y = math.sqrt(x)
__result__ = y * 2
"""
    print(evaluate_user_input(code))   # Should output 6.324555320336759