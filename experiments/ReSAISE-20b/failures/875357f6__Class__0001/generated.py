import ast
import sys
import io
from contextlib import redirect_stdout

# List of AST node types that are considered safe.
SAFE_NODES = {
    ast.Module,
    ast.Expr,
    ast.Load,
    ast.Store,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.Call,          # only certain builtins
    ast.Attribute,
    ast.Subscript,
    ast.Index,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.keyword,
}

# Builtins that are allowed in user scripts
ALLOWED_BUILTINS = {
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
    'sum': sum,
    'min': min,
    'max': max,
    # add more as needed
}

class SafeVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.errors = []

    def generic_visit(self, node):
        if type(node) not in SAFE_NODES:
            self.errors.append(f"Forbidden node: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node):
        # Allow only calls to whitelisted builtins
        if isinstance(node.func, ast.Name):
            if node.func.id not in ALLOWED_BUILTINS:
                self.errors.append(f"Forbidden function call: {node.func.id}")
        elif isinstance(node.func, ast.Attribute):
            # disallow attribute calls (e.g., os.system)
            self.errors.append(f"Forbidden method call: {ast.dump(node.func)}")
        else:
            self.errors.append("Unsupported function type")
        self.generic_visit(node)

def execute_user_script(submitted_script: str):
    """
    Safely executes a user-provided Python script.
    
    Parameters:
        submitted_script (str): The script to execute.

    Returns:
        str or None: Captured stdout output if any, otherwise None.

    Raises:
        ValueError: If the script contains forbidden operations or syntax errors.
    """
    # Parse the script to AST
    try:
        parsed = ast.parse(submitted_script, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in script: {e}")

    # Validate the AST
    visitor = SafeVisitor()
    visitor.visit(parsed)
    if visitor.errors:
        raise ValueError(f"Forbidden operations detected: {', '.join(visitor.errors)}")

    # Prepare a restricted global namespace
    safe_globals = {"__builtins__": ALLOWED_BUILTINS}
    safe_locals = {}

    # Capture stdout
    output_buffer = io.StringIO()
    try:
        with redirect_stdout(output_buffer):
            exec(compile(parsed, filename="<user_script>", mode="exec"),
                 safe_globals,
                 safe_locals)
    except Exception as exc:
        raise ValueError(f"Error during execution: {exc}")

    output = output_buffer.getvalue()
    return output if output else None