import ast
import io
import sys
from contextlib import redirect_stdout

# List of safe built‑in functions that the user may call
SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'sum': sum,
    'max': max,
    'min': min,
    'abs': abs,
    'round': round,
    # add more safe functions as needed
}

# Allowed AST node types
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Load,
    ast.Call,
    ast.Name,
    ast.Constant,
    ast.Num,            # for Python <3.8
    ast.Str,            # for Python <3.8
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.BinOp,
    ast.UnaryOp,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift,
    ast.BitOr, ast.BitAnd, ast.BitXor,
    ast.UAdd, ast.USub,
    ast.Compare,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # you can add more operators if needed
}

class SafeVisitor(ast.NodeVisitor):
    """AST visitor that ensures only safe nodes are present."""
    def visit(self, node):
        if type(node) not in ALLOWED_NODES:
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        super().visit(node)

    def visit_Name(self, node):
        # Only allow names that are in SAFE_BUILTINS or literals
        if node.id not in SAFE_BUILTINS:
            raise ValueError(f"Use of undefined name '{node.id}' is not allowed")
        self.generic_visit(node)

    def visit_Call(self, node):
        # Ensure the function being called is a Name and in SAFE_BUILTINS
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed")
        if node.func.id not in SAFE_BUILTINS:
            raise ValueError(f"Call to '{node.func.id}' is not allowed")
        self.generic_visit(node)

def execute_user_code(script_to_execute: str):
    """
    Execute a user supplied Python script in a sandboxed environment.

    Parameters
    ----------
    script_to_execute : str
        The Python code to execute.

    Returns
    -------
    output : str or None
        Captured stdout from the script, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the script contains disallowed syntax or attempts prohibited actions.
    """
    # 1. Parse and validate the AST
    try:
        parsed = ast.parse(script_to_execute, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from None

    # 2. Walk the AST to enforce safety rules
    SafeVisitor().visit(parsed)

    # 3. Prepare a restricted globals dictionary
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}

    # 4. Capture stdout
    output_io = io.StringIO()
    try:
        with redirect_stdout(output_io):
            exec(compile(parsed, filename="<user_script>", mode="exec"), sandbox_globals)
    except Exception as exc:
        # Re‑raise as ValueError to keep the API consistent
        raise ValueError(f"Execution error: {exc}") from None

    # 5. Return captured output if any
    result = output_io.getvalue()
    return result or None

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     user_code = """
# print('Hello', len([1,2,3]))
# x = sum(range(5))
# print('Sum:', x)
# """
#     print(execute_user_code(user_code))