import ast
import builtins
from contextlib import redirect_stdout
from io import StringIO

# ----------------------------------------------------
# Allowed built‑ins for the sandboxed environment
ALLOWED_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'dict': dict,
    'set': set,
    'tuple': tuple,
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    # add more safe built‑ins here if needed
}

# ----------------------------------------------------
def _is_disallowed_node(node: ast.AST) -> bool:
    """
    Return True if the node represents a disallowed operation.
    """
    # Import statements
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        return True

    # Calls to dangerous built‑ins
    if isinstance(node, ast.Call):
        func = node.func

        # disallow __import__, eval, exec
        if isinstance(func, ast.Name) and func.id in ('__import__', 'eval', 'exec'):
            return True

        # disallow calls to os.system, subprocess.Popen etc.
        if isinstance(func, ast.Attribute):
            attr_name = func.attr
            if attr_name in ('system', 'popen', 'run'):
                return True

    # Disallow attribute access on built‑ins like os, sys etc.
    if isinstance(node, ast.Attribute):
        # e.g., os.path.join
        value = node.value
        if isinstance(value, ast.Name) and value.id in ('os', 'sys', 'subprocess'):
            return True

    # Disallow lambda expressions (they can be used to escape restrictions)
    if isinstance(node, ast.Lambda):
        return True

    # Disallow comprehensions that might create generators with unsafe content
    if isinstance(node, (ast.GeneratorExp)):
        return True

    # Disallow 'with' statements that could open files
    if isinstance(node, ast.With):
        return True

    # Disallow 'try/except' blocks that could hide errors (optional)
    if isinstance(node, ast.Try):
        return True

    # Disallow any other suspicious nodes if needed
    return False


def _check_ast(tree: ast.AST):
    """
    Walk the AST and raise ValueError if any disallowed node is found.
    """
    for node in ast.walk(tree):
        if _is_disallowed_node(node):
            raise ValueError(f"Disallowed operation detected: {ast.dump(node)}")


# ----------------------------------------------------
def evaluate_code_string(code_string: str):
    """
    Execute a small Python snippet in a sandboxed environment.

    Parameters
    ----------
    code_string : str
        The Python code to execute.

    Returns
    -------
    None or str
        If the executed code produces output via print, that output is returned as a string.
        If there is no output, None is returned.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # 1. Parse and validate the AST
    try:
        tree = ast.parse(code_string, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code: {exc}") from exc

    _check_ast(tree)

    # 2. Prepare the sandboxed globals
    sandbox_globals = {'__builtins__': ALLOWED_BUILTINS}

    # 3. Capture stdout
    output_io = StringIO()
    try:
        with redirect_stdout(output_io):
            exec(compile(tree, filename='<string>', mode='exec'), sandbox_globals)
    except Exception as exc:
        # Re‑raise any runtime exception with context
        raise ValueError(f"Runtime error during execution: {exc}") from exc

    # 4. Return captured output if any
    output = output_io.getvalue()
    return output or None


# ----------------------------------------------------
# Example usage (uncomment to test):
#
# if __name__ == "__main__":
#     print(evaluate_code_string("print('Hello, world!')"))
#     print(evaluate_code_string("x = 5\nprint(x * 2)"))