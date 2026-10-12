import ast
import builtins
import sys
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

# ---------- Safe Builtins ----------
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'dict': dict,
    'enumerate': enumerate,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'pow': pow,
    'range': range,
    'reversed': reversed,
    'round': round,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    # Add more safe functions if needed
}

# ---------- AST Validator ----------
class SafeASTVisitor(ast.NodeVisitor):
    """
    Visitor that ensures the user script only contains safe AST nodes.
    Raises ValueError on forbidden constructs.
    """
    # Forbidden node types
    FORBIDDEN_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,          # exec is a statement in py2
        ast.Call,
        ast.Attribute,
    )

    # Forbidden function names that may be called via Call
    FORBIDDEN_CALLS = {
        'eval', 'exec', 'compile',
        'open', 'input', 'dir', 'vars', '__import__',
    }

    def visit(self, node):
        if isinstance(node, self.FORBIDDEN_NODES):
            raise ValueError(f"Forbidden construct: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        # Check if the called function is a name and forbidden
        func = node.func
        if isinstance(func, ast.Name) and func.id in self.FORBIDDEN_CALLS:
            raise ValueError(f"Forbidden function call: {func.id}")
        # Disallow attribute calls like os.system, subprocess.Popen
        if isinstance(func, ast.Attribute):
            raise ValueError(f"Attribute calls are not allowed: {ast.dump(node)}")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Disallow any attribute access (e.g., os.path)
        raise ValueError(f"Attribute access is forbidden: {ast.dump(node)}")

    def visit_Name(self, node):
        # Allow names that are either defined in locals or builtins
        # No further check needed here; globals will be restricted later.
        pass

# ---------- Execution Function ----------
def execute_user_script(submitted_script: str):
    """
    Execute a user-provided Python script in a sandboxed environment.
    
    Parameters
    ----------
    submitted_script : str
        The script to execute.

    Returns
    -------
    str or None
        Captured stdout output if any, otherwise None.

    Raises
    ------
    ValueError
        If the script contains forbidden operations or has syntax errors.
    """
    # 1. Syntax check and AST validation
    try:
        parsed = ast.parse(submitted_script, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user script: {e}") from None

    validator = SafeASTVisitor()
    try:
        validator.visit(parsed)
    except ValueError as e:
        raise

    # 2. Prepare restricted globals
    safe_globals = {
        '__builtins__': SAFE_BUILTINS,
    }

    # 3. Execute script capturing stdout
    output_io = StringIO()
    try:
        with redirect_stdout(output_io), redirect_stderr(output_io):
            exec(compile(parsed, filename='<user_script>', mode='exec'), safe_globals)
    except Exception as exc:
        # Wrap any runtime exception into ValueError for consistency
        raise ValueError(f"Runtime error during script execution: {exc}") from None

    output = output_io.getvalue()
    return output if output else None