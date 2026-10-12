import ast
from types import FunctionType

# A set of AST node types that are disallowed for safety reasons
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # disallow all function calls
    ast.Attribute,     # prevent attribute access like __import__
    ast.Subscript,
    ast.Lambda,
    ast.ListComp,      # comprehensions can be abused
    ast.DictComp,
    ast.SetComp,
    ast.GeneratorExp,
}

# A set of names that are forbidden to be used in expressions
DISALLOWED_NAMES = {
    "__import__",
    "open",
    "exec",
    "eval",
    "compile",
}

def _check_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if a disallowed node
    or name is encountered.
    """
    for child in ast.iter_child_nodes(node):
        if type(child) in DISALLOWED_NODES:
            raise ValueError(f"Disallowed construct: {type(child).__name__}")
        if isinstance(child, ast.Name) and child.id in DISALLOWED_NAMES:
            raise ValueError(f"Disallowed name: {child.id}")
        _check_ast(child)

def run_python_snippet(python_snippet: str):
    """
    Execute a user-provided Python snippet in a highly restricted environment.
    
    Parameters
    ----------
    python_snippet : str
        The code to execute. It may contain multiple statements but must not
        use any disallowed constructs such as imports, function calls,
        attribute access or the built‑in functions listed in
        DISALLOWED_NAMES.
    
    Returns
    -------
    Any
        The value of the last expression in the snippet, if any.
    
    Raises
    ------
    ValueError
        If the snippet contains prohibited actions or unsafe constructs.
    """
    # Parse the code into an AST
    try:
        parsed = ast.parse(python_snippet, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python syntax: {exc}") from None

    # Perform safety checks
    _check_ast(parsed)

    # Prepare a restricted global namespace
    safe_globals = {
        "__builtins__": {},          # no built‑ins available
        "None": None,
        "True": True,
        "False": False,
    }

    # Compile the AST into a code object
    compiled = compile(parsed, filename="<snippet>", mode="exec")

    # Execute the code in a restricted environment
    exec(compiled, safe_globals)

    # Try to evaluate the last expression if it exists
    # We look for an Expr node as the last statement
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        expr_code = compile(ast.Expression(body=parsed.body[-1].value),
                            filename="<snippet>", mode="eval")
        return eval(expr_code, safe_globals)
    return None