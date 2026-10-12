import ast
import builtins
import io
import sys
from types import ModuleType

# List of safe built‑in functions that users are allowed to call
SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'dict': dict,
    'list': list,
    'set': set,
    'tuple': tuple,
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
}

# AST visitor that ensures only safe constructs are used
class SafeVisitor(ast.NodeVisitor):
    ALLOWED_NODES = (
        ast.Module,
        ast.Expr,
        ast.Assign,
        ast.AugAssign,
        ast.Return,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python 3.8+
        ast.Name,
        ast.Call,
        ast.Load,
        ast.Store,
        ast.Compare,
        ast.BoolOp,
        ast.And,
        ast.Or,
        ast.Not,
        ast.List,
        ast.Tuple,
        ast.Dict,
        ast.Set,
        ast.IfExp,        # ternary
        ast.Subscript,
        ast.Index,
        ast.Slice,
    )

    def visit(self, node):
        if not isinstance(node, self.ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        # Ensure the function called is a safe builtin
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only direct calls to built‑in functions are allowed")
        if node.func.id not in SAFE_BUILTINS:
            raise ValueError(f"Call to disallowed function: {node.func.id}")
        # Recursively check arguments
        for arg in node.args:
            self.visit(arg)
        for keyword in node.keywords:
            self.visit(keyword.value)

    def visit_Import(self, node):
        raise ValueError("Import statements are not allowed")

    def visit_ImportFrom(self, node):
        raise ValueError("Import statements are not allowed")

    def visit_Attribute(self, node):
        # Prevent attribute access (e.g., os.system)
        raise ValueError("Attribute access is disallowed")

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id not in SAFE_BUILTINS:
            # Allow only names that are safe builtins or local variables
            if not isinstance(node.ctx, ast.Store):
                raise ValueError(f"Use of undefined name: {node.id}")
        # Store context is fine; local variables will be created

def execute_user_code(script_to_execute: str):
    """
    Execute a user provided script in a restricted environment.

    Parameters
    ----------
    script_to_execute : str
        Python code to run.

    Returns
    -------
    str or None
        Captured stdout if any; otherwise None.

    Raises
    ------
    ValueError
        If the script contains disallowed operations or has syntax errors.
    """
    # Parse and validate syntax
    try:
        tree = ast.parse(script_to_execute, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user script: {e}") from None

    # Ensure only safe nodes are present
    SafeVisitor().visit(tree)

    # Prepare restricted globals and locals
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    safe_locals = {}

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        exec(compile(tree, filename="<user_script>", mode="exec"), safe_globals, safe_locals)
    except Exception as e:
        raise ValueError(f"Execution error: {e}") from None
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None