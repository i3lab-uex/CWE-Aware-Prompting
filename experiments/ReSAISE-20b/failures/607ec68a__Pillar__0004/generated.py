import ast
import sys
from io import StringIO
from types import SimpleNamespace

# --------------------------------------------------------------------------- #
# 1. AST visitor that rejects unsafe nodes
# --------------------------------------------------------------------------- #
class SafeNodeVisitor(ast.NodeVisitor):
    """
    Walks an AST and raises ValueError if it finds a node that is
    considered unsafe.  The list of disallowed nodes can be extended
    as needed.
    """
    # Disallowed node types
    _disallowed = (
        ast.Import,            # import statements
        ast.ImportFrom,        # from ... import ...
        ast.Exec,              # exec() statement (Python 2)
        ast.Call,              # function calls are checked separately
        ast.Attribute,         # attribute access (e.g., __dict__, os.path)
    )

    # Disallowed function names
    _disallowed_funcs = {
        'eval', 'exec', 'compile',
        'open', 'input', 'locals', 'globals',
        'vars', '__import__', 'dir'
    }

    def visit(self, node):
        if isinstance(node, self._disallowed):
            raise ValueError(f"Disallowed statement: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        # Reject calls to disallowed functions
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            # e.g., os.system()
            func_name = node.func.attr

        if func_name in self._disallowed_funcs:
            raise ValueError(f"Disallowed function call: {func_name}")

        # Recurse into arguments
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Prevent attribute access that could expose dangerous internals
        if isinstance(node.value, ast.Name) and node.value.id in ('__builtins__', 'sys'):
            raise ValueError(f"Disallowed attribute access: {node.value.id}.{node.attr}")
        self.generic_visit(node)

# --------------------------------------------------------------------------- #
# 2. Restricted globals for exec
# --------------------------------------------------------------------------- #
def _build_safe_globals():
    """
    Construct a dictionary of globals that is safe for exec.
    Only a minimal set of builtins are exposed.  All others are omitted.
    """
    safe_builtins = {
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
        # Add more safe builtins as required
    }
    return {'__builtins__': safe_builtins}

# --------------------------------------------------------------------------- #
# 3. Main function
# --------------------------------------------------------------------------- #
def safe_run_script(code: str):
    """
    Execute a user supplied Python script in a restricted environment.

    Parameters
    ----------
    code : str
        The user supplied Python script to execute.

    Returns
    -------
    Any
        If the script prints to stdout, that output is returned as a string.
        Otherwise None is returned.

    Raises
    ------
    ValueError
        If the script contains disallowed syntax or operations.
    """
    # 1. Parse the code into an AST to check for syntax errors
    try:
        parsed = ast.parse(code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in script: {e}")

    # 2. Walk the AST to ensure only safe constructs are present
    visitor = SafeNodeVisitor()
    try:
        visitor.visit(parsed)
    except ValueError as e:
        raise ValueError(f"Prohibited action detected: {e}")

    # 3. Capture stdout
    old_stdout = sys.stdout
    fake_out = StringIO()
    sys.stdout = fake_out

    # 4. Execute the script in a restricted environment
    try:
        exec(compile(parsed, filename="<user_script>", mode="exec"),
             _build_safe_globals(),
             {})
    except Exception as exc:
        # Restore stdout before re-raising
        sys.stdout = old_stdout
        raise ValueError(f"Script execution failed: {exc}") from exc

    # 5. Restore stdout and return captured output
    sys.stdout = old_stdout
    output = fake_out.getvalue()
    return output if output else None

# --------------------------------------------------------------------------- #
# Example usage (commented out for safety)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     script = '''
# print("Hello, world!")
# for i in range(3):
#     print(i)
# '''
#     print(safe_run_script(script))