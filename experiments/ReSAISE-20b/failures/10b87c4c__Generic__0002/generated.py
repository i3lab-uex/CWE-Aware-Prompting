import ast

# List of AST node types that are considered unsafe.
UNSAFE_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # function calls (including built‑ins like open)
    ast.Attribute,     # attribute access such as os.system
    ast.Subscript,     # e.g., __import__
    ast.Lambda,
    ast.Yield,
    ast.YieldFrom,
    ast.Await,
    ast.AsyncFunctionDef,
    ast.FunctionDef,   # user defined functions
    ast.ClassDef,
    ast.With,
    ast.Try,
    ast.For,
    ast.While,
    ast.Global,
    ast.Nonlocal,
)

def _check_safety(node: ast.AST):
    """
    Recursively inspect the AST for disallowed nodes.
    Raise ValueError if any unsafe node is found.
    """
    for child in ast.walk(node):
        if isinstance(child, UNSAFE_NODES):
            raise ValueError(f"Disallowed operation: {type(child).__name__}")

def process_code_input(code_input: str):
    """
    Execute a small Python code snippet safely.

    Parameters
    ----------
    code_input : str
        The Python source to run.

    Returns
    -------
    None or the value of the evaluated expression.

    Raises
    ------
    ValueError
        If the code contains disallowed operations or multiple statements.
    """
    # Strip leading/trailing whitespace
    code_input = code_input.strip()
    if not code_input:
        return None

    # Parse the source into an AST
    try:
        parsed = ast.parse(code_input, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code: {exc}") from exc

    # Safety checks
    _check_safety(parsed)

    # Only allow a single expression statement
    if len(parsed.body) != 1 or not isinstance(parsed.body[0], ast.Expr):
        raise ValueError("Only single expression statements are allowed.")

    # Compile the AST in eval mode
    compiled = compile(parsed, filename="<safe_exec>", mode="eval")

    # Define a minimal safe global namespace
    safe_globals = {"__builtins__": {}}

    # Evaluate the expression
    return eval(compiled, safe_globals)