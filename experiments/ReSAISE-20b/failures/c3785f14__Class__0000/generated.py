import ast
import sys
import types
from contextlib import redirect_stdout
from io import StringIO


class DisallowedNodeError(ValueError):
    """Raised when the code contains disallowed syntax or calls."""
    pass


# List of built‑in functions that are considered unsafe
UNSAFE_BUILTINS = {
    "open",
    "eval",
    "exec",
    "__import__",
    "input",
}

# List of modules that should not be imported
UNSAFE_MODULES = {
    "os",
    "sys",
    "subprocess",
    "shutil",
    "socket",
}


def _check_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise DisallowedNodeError if any
    disallowed node is encountered.
    """
    for child in ast.iter_child_nodes(node):
        # Disallow import statements
        if isinstance(child, (ast.Import, ast.ImportFrom)):
            module_name = (
                child.names[0].name if isinstance(child, ast.Import)
                else child.module
            )
            if module_name.split('.')[0] in UNSAFE_MODULES:
                raise DisallowedNodeError(
                    f"Importing module '{module_name}' is not allowed."
                )
            _check_ast(child)

        # Disallow calls to unsafe built‑ins
        elif isinstance(child, ast.Call):
            if isinstance(child.func, ast.Name) and child.func.id in UNSAFE_BUILTINS:
                raise DisallowedNodeError(
                    f"Call to built‑in '{child.func.id}' is not allowed."
                )
            _check_ast(child)

        # Disallow eval/exec expressions (in case they appear as strings)
        elif isinstance(child, ast.Expr) and isinstance(child.value, (ast.Call, ast.Lambda)):
            _check_ast(child)

        # Recursively inspect other nodes
        else:
            _check_ast(child)


def evaluate_code_string(code_string: str):
    """
    Execute a small Python snippet safely.

    Parameters
    ----------
    code_string : str
        The Python code to execute.

    Returns
    -------
    None or str
        If the executed code produces output on stdout, that output is returned as a string.
        Otherwise None is returned.

    Raises
    ------
    ValueError
        If the code contains disallowed operations or imports.
    """
    # Parse the code to an AST and perform a security check
    try:
        parsed = ast.parse(code_string, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from exc

    _check_ast(parsed)

    # Prepare a minimal global namespace
    safe_globals = {
        "__builtins__": {k: __builtins__[k] for k in ("abs", "all", "any", "bool",
                                                      "dict", "float", "int", "len",
                                                      "list", "max", "min", "pow",
                                                      "range", "round", "str", "sum")}
    }

    # Capture stdout
    output_buffer = StringIO()
    try:
        with redirect_stdout(output_buffer):
            exec(compile(parsed, filename="<string>", mode="exec"), safe_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    output = output_buffer.getvalue()
    return output if output else None