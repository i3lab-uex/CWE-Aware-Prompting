import ast
import builtins
import sys
import io

# ----------------------------------------------------------------------
# 1.  Whitelist of safe built‑in functions and names
# ----------------------------------------------------------------------
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
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
    'tuple': tuple,
}

# You can extend this list with more math functions if needed
SAFE_MODULES = {
    'math': __import__('math')
}

# ----------------------------------------------------------------------
# 2.  AST visitor that checks for forbidden nodes
# ----------------------------------------------------------------------
class SafeVisitor(ast.NodeVisitor):
    """
    Walk the AST and raise ValueError if any forbidden node is found.
    Only a minimal set of nodes are allowed for expression evaluation.
    """
    # Allowed node types
    ALLOWED_NODES = {
        ast.Module,
        ast.Expr,
        ast.Expression,
        ast.Assign,
        ast.AugAssign,
        ast.Name,
        ast.Load,
        ast.Store,
        ast.Constant,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,
        ast.Attribute,
        ast.Subscript,
        ast.Index,
        ast.Slice,
        ast.List,
        ast.Tuple,
        ast.Dict,
        ast.Set,
        ast.IfExp,
        # operators
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
        ast.BitXor, ast.BitAnd, ast.Invert, ast.Not,
        ast.UAdd, ast.USub,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        ast.Is, ast.IsNot, ast.In, ast.NotIn,
    }

    # Forbidden builtins (e.g., open, exec)
    FORBIDDEN_BUILTINS = {'open', 'exec', 'eval', '__import__'}

    def visit(self, node):
        if type(node) not in self.ALLOWED_NODES:
            raise ValueError(f"Forbidden node detected: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        # Disallow calls to forbidden builtins
        if isinstance(node.func, ast.Name) and node.func.id in self.FORBIDDEN_BUILTINS:
            raise ValueError(f"Forbidden builtin call: {node.func.id}")
        super().visit_Call(node)

    def visit_Import(self, node):
        raise ValueError("Imports are not allowed")

    def visit_ImportFrom(self, node):
        raise ValueError("Imports are not allowed")


# ----------------------------------------------------------------------
# 3.  The evaluation function
# ----------------------------------------------------------------------
def evaluate_user_input(user_code: str):
    """
    Execute *user_code* in a sandboxed environment.
    
    Parameters
    ----------
    user_code : str
        The Python script submitted by the user.
    
    Returns
    -------
    Any
        The result of the last expression, or None if no output.
    
    Raises
    ------
    ValueError
        If the script contains forbidden actions or is syntactically invalid.
    """
    # 3.1 Parse the code and validate syntax
    try:
        parsed = ast.parse(user_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user code: {e}")

    # 3.2 Ensure no forbidden nodes exist
    SafeVisitor().visit(parsed)

    # 3.3 Prepare the sandboxed globals and locals
    sandbox_globals = {
        '__builtins__': SAFE_BUILTINS,
        **SAFE_MODULES
    }
    sandbox_locals = {}

    # 3.4 Capture stdout (if any)
    old_stdout = sys.stdout
    stdout_buffer = io.StringIO()
    try:
        sys.stdout = stdout_buffer
        exec(compile(parsed, filename='<user_code>', mode='exec'), sandbox_globals, sandbox_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    # 3.5 Return captured output or last expression result
    output = stdout_buffer.getvalue()
    if output:
        return output.rstrip('\n')
    # If nothing printed, try to find a result in locals
    if sandbox_locals:
        return next(iter(sandbox_locals.values()))
    return None

# ----------------------------------------------------------------------
# 4.  Example usage (commented out – remove for production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    code = """
x = 10
y = 20
print('Sum:', x + y)
"""
    print("Result:", evaluate_user_input(code))