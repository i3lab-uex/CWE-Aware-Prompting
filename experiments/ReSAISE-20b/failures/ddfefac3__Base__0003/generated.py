import ast
import io
import sys
from types import ModuleType

# -------------------------------------------------------------
# 1. Define a set of allowed built‑ins
# -------------------------------------------------------------
SAFE_BUILTINS = {
    'abs', 'all', 'any', 'ascii', 'bin', 'bool',
    'bytearray', 'bytes', 'callable', 'chr', 'complex',
    'dict', 'divmod', 'enumerate', 'filter', 'float',
    'format', 'frozenset', 'hash', 'hex', 'int', 'isinstance',
    'issubclass', 'iter', 'len', 'list', 'map', 'max',
    'min', 'next', 'object', 'oct', 'ord', 'pow',
    'range', 'repr', 'reversed', 'round', 'set',
    'slice', 'sorted', 'str', 'sum', 'tuple', 'type',
    'zip', 'print'
}

# -------------------------------------------------------------
# 2. Helper to build a restricted globals dictionary
# -------------------------------------------------------------
def _restricted_globals():
    return {
        '__builtins__': {k: __builtins__[k] for k in SAFE_BUILTINS if k in __builtins__}
    }

# -------------------------------------------------------------
# 3. AST visitor to detect forbidden constructs
# -------------------------------------------------------------
class _ForbiddenNodeVisitor(ast.NodeVisitor):
    FORBIDDEN_NODES = (
        ast.Import,           # import statements
        ast.ImportFrom,
        ast.Exec,             # exec() in Python 2 (no effect in 3 but kept for safety)
        ast.Call,             # calls are inspected further
    )

    FORBIDDEN_NAMES = {
        'exec', 'eval', 'compile',
        'open', 'input', 'os', 'sys', 'subprocess',
        '__import__', 'getattr', 'setattr', 'delattr'
    }

    def visit(self, node):
        if isinstance(node, self.FORBIDDEN_NODES):
            raise ValueError(f"Forbidden node type: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node: ast.Call):
        # disallow calls to dangerous built‑ins or modules
        if isinstance(node.func, ast.Name):
            if node.func.id in self.FORBIDDEN_NAMES:
                raise ValueError(f"Call to forbidden function: {node.func.id}")
        elif isinstance(node.func, ast.Attribute):
            # e.g., os.system(...)
            if isinstance(node.func.value, ast.Name) and node.func.value.id in self.FORBIDDEN_NAMES:
                raise ValueError(f"Call to forbidden attribute: {node.func.value.id}.{node.func.attr}")
        self.generic_visit(node)

# -------------------------------------------------------------
# 4. Main function
# -------------------------------------------------------------
def process_python_code(code_str: str):
    """
    Execute a user supplied Python code string in a restricted environment.

    Parameters
    ----------
    code_str : str
        The Python snippet to execute.

    Returns
    -------
    str | None
        Captured stdout if any, otherwise None.

    Raises
    ------
    ValueError
        If the code contains forbidden constructs or fails to parse.
    """
    # 1. Parse and validate syntax
    try:
        parsed = ast.parse(code_str, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Invalid Python code: {e}") from None

    # 2. Walk AST to ensure safety
    try:
        _ForbiddenNodeVisitor().visit(parsed)
    except ValueError as e:
        raise

    # 3. Prepare restricted execution environment
    exec_globals = _restricted_globals()
    exec_locals: dict = {}

    # 4. Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    try:
        sys.stdout = fake_out
        exec(compile(parsed, filename='<user_code>', mode='exec'), exec_globals, exec_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None