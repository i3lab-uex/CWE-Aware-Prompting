import ast
import builtins
import sys
from contextlib import redirect_stdout
from io import StringIO


class DisallowedNodeVisitor(ast.NodeVisitor):
    """
    Walks the AST and raises ValueError if any disallowed construct is found.
    """

    DISALLOWED_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Call,   # we will check the function name separately
    )

    DISALLOWED_CALLS = {
        'eval',
        'exec',
        '__import__',
        'open',
        'input',
    }

    def visit(self, node):
        if isinstance(node, self.DISALLOWED_NODES):
            raise ValueError(f"Disallowed statement: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node: ast.Call):
        # Detect calls to disallowed builtins
        if isinstance(node.func, ast.Name) and node.func.id in self.DISALLOWED_CALLS:
            raise ValueError(f"Disallowed function call: {node.func.id}")
        # Prevent attribute access to builtins (e.g., os.system)
        if isinstance(node.func, ast.Attribute):
            raise ValueError(f"Attribute access is disallowed: {ast.dump(node.func)}")
        self.generic_visit(node)


def process_code_input(code_input: str):
    """
    Execute a small Python snippet safely.

    Parameters
    ----------
    code_input : str
        The Python code to execute.

    Returns
    -------
    None or str
        `None` if the snippet produced no output; otherwise the captured stdout string.

    Raises
    ------
    ValueError
        If the code contains disallowed constructs or calls.
    """
    # 1. Syntax check & AST validation
    try:
        tree = ast.parse(code_input, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}")

    # Validate the AST for disallowed constructs
    DisallowedNodeVisitor().visit(tree)

    # 2. Prepare a restricted execution environment
    allowed_builtins = {
        'abs': abs,
        'all': all,
        'any': any,
        'bool': bool,
        'chr': chr,
        'dict': dict,
        'float': float,
        'int': int,
        'len': len,
        'list': list,
        'max': max,
        'min': min,
        'pow': pow,
        'range': range,
        'round': round,
        'str': str,
        'sum': sum,
        # add more safe builtins as needed
    }

    restricted_globals = {
        '__builtins__': allowed_builtins,
    }
    restricted_locals = {}

    # 3. Capture stdout
    f = StringIO()
    try:
        with redirect_stdout(f):
            exec(compile(tree, filename='<string>', mode='exec'),
                 restricted_globals,
                 restricted_locals)
    except Exception as exc:
        # Re‑raise as ValueError to keep the API consistent
        raise ValueError(f"Execution error: {exc}") from exc

    output = f.getvalue()
    return output if output else None