import ast
import builtins
import sys
from contextlib import redirect_stdout
from io import StringIO


class _SafeExecutionVisitor(ast.NodeVisitor):
    """
    Visitor that walks the AST and raises ValueError if it encounters
    any disallowed node types or attributes.
    """
    # Disallowed AST node types
    _DISALLOWED_NODES = {
        ast.Import,
        ast.ImportFrom,
        ast.Exec,          # Python 2 only, kept for completeness
        ast.Call,          # we will check the function name separately
    }

    # Disallowed built-in functions (names only)
    _DISALLOWED_BUILTINS = {
        'eval',
        'exec',
        'open',
        'compile',
        'input',
        '__import__',
    }

    def visit(self, node):
        if type(node) in self._DISALLOWED_NODES:
            raise ValueError(f"Disallowed statement: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node: ast.Call):
        # Check if the function being called is a disallowed builtin
        func = node.func
        if isinstance(func, ast.Name) and func.id in self._DISALLOWED_BUILTINS:
            raise ValueError(f"Disallowed builtin function: {func.id}")
        # Check for calls to os.system, subprocess.Popen etc.
        if isinstance(func, ast.Attribute):
            # Resolve the full dotted name
            names = []
            cur = func
            while isinstance(cur, ast.Attribute):
                names.append(cur.attr)
                cur = cur.value
            if isinstance(cur, ast.Name):
                names.append(cur.id)
            full_name = ".".join(reversed(names))
            if any(full_name.startswith(prefix) for prefix in (
                "os.", "subprocess.", "sys.", "shutil.", "socket."
            )):
                raise ValueError(f"Disallowed function call: {full_name}")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Disallow accessing dangerous attributes like __dict__, __class__
        if isinstance(node.value, ast.Name) and node.attr.startswith('__'):
            raise ValueError(f"Disallowed attribute access: {node.attr}")
        self.generic_visit(node)

    def visit_Name(self, node):
        # Disallow accessing builtins like __import__
        if node.id in self._DISALLOWED_BUILTINS:
            raise ValueError(f"Disallowed name usage: {node.id}")
        self.generic_visit(node)


def process_code_input(code_input: str):
    """
    Execute a small Python code snippet safely.

    Parameters
    ----------
    code_input : str
        The Python source to run.

    Returns
    -------
    None or str
        If the code prints nothing, returns None. Otherwise returns
        a string containing all printed output.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # 1. Parse the code to an AST
    try:
        parsed = ast.parse(code_input, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}")

    # 2. Validate the AST
    visitor = _SafeExecutionVisitor()
    visitor.visit(parsed)

    # 3. Prepare a restricted globals dict
    safe_builtins = {
        name: getattr(builtins, name)
        for name in ('abs', 'all', 'any', 'bool', 'bytes',
                     'chr', 'dict', 'float', 'int', 'len',
                     'list', 'max', 'min', 'pow', 'range',
                     'round', 'str', 'sum', 'tuple')
    }
    safe_globals = {"__builtins__": safe_builtins}

    # 4. Capture stdout
    f = StringIO()
    try:
        with redirect_stdout(f):
            exec(compile(parsed, filename="<string>", mode="exec"),
                 safe_globals,
                 {})
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    output = f.getvalue()
    return None if not output else output