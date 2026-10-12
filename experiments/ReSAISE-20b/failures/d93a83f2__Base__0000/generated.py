import ast
from typing import Any, Optional


class UnsafeCodeError(ValueError):
    """Raised when the snippet contains disallowed constructs."""


# List of AST node types that are considered unsafe
UNSAFE_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,  # exec is not a node in Python3 but kept for completeness
    ast.Call,  # we will filter specific calls later
)

# Disallowed function names that should not be called
DISALLOWED_CALLS = {
    "eval",
    "exec",
    "open",
    "__import__",
    "compile",
    "input",
}

# Safe builtins that are allowed in the sandbox
SAFE_BUILTINS = {
    "abs",
    "all",
    "any",
    "bool",
    "chr",
    "complex",
    "dict",
    "divmod",
    "enumerate",
    "filter",
    "float",
    "format",
    "hash",
    "hex",
    "int",
    "isinstance",
    "issubclass",
    "len",
    "list",
    "map",
    "max",
    "min",
    "next",
    "pow",
    "range",
    "repr",
    "reversed",
    "round",
    "set",
    "slice",
    "sorted",
    "str",
    "sum",
    "tuple",
    "zip",
}


def _validate_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise UnsafeCodeError if a disallowed
    construct is found.
    """
    for child in ast.walk(node):
        # Disallow imports
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            raise UnsafeCodeError("Import statements are not allowed.")

        # Disallow calls to unsafe functions
        if isinstance(child, ast.Call):
            func = child.func
            # Handle simple names like eval()
            if isinstance(func, ast.Name) and func.id in DISALLOWED_CALLS:
                raise UnsafeCodeError(f"Call to disallowed function '{func.id}'.")
            # Handle attribute calls like os.system()
            if isinstance(func, ast.Attribute):
                raise UnsafeCodeError("Attribute function calls are not allowed.")

        # Disallow lambda expressions
        if isinstance(child, ast.Lambda):
            raise UnsafeCodeError("Lambda expressions are not allowed.")

        # Disallow comprehensions that could access globals
        if isinstance(child, (ast.GeneratorExp, ast.ListComp, ast.DictComp, ast.SetComp)):
            raise UnsafeCodeError("Comprehensions are not allowed.")

        # Disallow exec as a statement (Python3 uses ast.Exec only in Py2)
        if isinstance(child, ast.Expr) and isinstance(child.value, ast.Call):
            # Already handled by Call checks
            pass

        # Disallow 'with' statements (could be used for file access)
        if isinstance(child, ast.With):
            raise UnsafeCodeError("With statements are not allowed.")


def safe_execute_code(snippet: str) -> Optional[Any]:
    """
    Execute a user-provided Python snippet in a sandboxed environment.

    Parameters
    ----------
    snippet : str
        The code to execute. It may contain expressions or statements.

    Returns
    -------
    Any
        The result of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed constructs.
    """
    # Parse the code to an AST and validate it
    try:
        parsed = ast.parse(snippet, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python syntax: {exc}") from exc

    _validate_ast(parsed)

    # Prepare a restricted global namespace
    sandbox_globals = {"__builtins__": {k: __builtins__[k] for k in SAFE_BUILTINS}}
    sandbox_locals = {}

    # Execute the code
    exec(compile(parsed, filename="<sandbox>", mode="exec"), sandbox_globals, sandbox_locals)

    # If the last node is an expression, return its value
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        # Evaluate the expression in the sandbox
        expr_code = compile(ast.Expression(parsed.body[-1].value), filename="<expr>", mode="eval")
        return eval(expr_code, sandbox_globals, sandbox_locals)

    return None