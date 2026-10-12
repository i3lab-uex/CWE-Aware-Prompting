import ast
import builtins
import io
import sys
from types import FunctionType, ModuleType

# Whitelist of safe built‑in functions and constants
SAFE_BUILTINS = {
    "abs", "all", "any", "bool", "chr", "dict", "float",
    "int", "len", "list", "max", "min", "pow", "range",
    "round", "str", "sum", "tuple", "zip", "enumerate",
    "print"
}

# Disallowed AST node types
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # calls will be inspected separately
    ast.Attribute,     # disallow attribute access (e.g. os.system)
    ast.Subscript,
)

# Disallowed function names that could lead to side effects
DISALLOWED_CALLS = {
    "eval", "exec", "open", "__import__",
    "compile", "input",
}

def _is_safe_call(node: ast.Call) -> bool:
    """
    Return True if the call node references a safe function.
    The function name must be a Name (no attribute access).
    """
    if isinstance(node.func, ast.Name):
        return node.func.id not in DISALLOWED_CALLS
    # Any other form (attribute, lambda, etc.) is disallowed
    return False

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if any
    disallowed node or call is found.
    """
    for child in ast.walk(node):
        if isinstance(child, DISALLOWED_NODES):
            raise ValueError(f"Disallowed construct: {type(child).__name__}")
        if isinstance(child, ast.Call):
            if not _is_safe_call(child):
                raise ValueError(f"Disallowed function call: {ast.unparse(child)}")

def process_code_input(code_input: str):
    """
    Execute a small Python snippet safely.

    Parameters
    ----------
    code_input : str
        The Python code to execute.

    Returns
    -------
    None or the value of the last expression, if any.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # Parse the source into an AST
    try:
        tree = ast.parse(code_input, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}")

    # Perform security checks
    _check_ast(tree)

    # Prepare a restricted global namespace
    safe_globals = {k: getattr(builtins, k) for k in SAFE_BUILTINS if hasattr(builtins, k)}
    safe_globals["__builtins__"] = safe_globals  # expose only the whitelisted builtins

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        # Execute the code
        exec(compile(tree, filename="<string>", mode="exec"), safe_globals)
    finally:
        # Restore stdout
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    if output:
        return output.rstrip("\n")
    # If nothing was printed, return None
    return None

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(process_code_input("print('Hello, world!')"))