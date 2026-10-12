import ast
from types import FunctionType, CodeType

# A minimal set of safe built‑ins that are unlikely to be harmful.
SAFE_BUILTINS = {
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
    'tuple': tuple,
    'zip': zip,
}

# Node visitor that rejects unsafe constructs.
class SafeNodeVisitor(ast.NodeVisitor):
    def visit_Import(self, node):
        raise ValueError("Imports are not allowed")

    def visit_ImportFrom(self, node):
        raise ValueError("Imports are not allowed")

    def visit_Call(self, node):
        # Disallow calls to dangerous built‑ins or arbitrary functions.
        if isinstance(node.func, ast.Name):
            name = node.func.id
            if name in {'open', 'exec', 'eval', 'compile', '__import__'}:
                raise ValueError(f"Call to forbidden function `{name}`")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Disallow accessing attributes that could be dangerous
        if isinstance(node.value, ast.Name) and node.value.id == '__builtins__':
            raise ValueError("Access to __builtins__ is forbidden")
        self.generic_visit(node)

    def visit_Subscript(self, node):
        # Prevent subscript access to __builtins__
        if isinstance(node.value, ast.Name) and node.value.id == '__builtins__':
            raise ValueError("Subscript access to __builtins__ is forbidden")
        self.generic_visit(node)

    def visit_Global(self, node):
        raise ValueError("Global declarations are not allowed")

    def visit_Nonlocal(self, node):
        raise ValueError("Nonlocal declarations are not allowed")

    def visit_Delete(self, node):
        raise ValueError("Delete statements are not allowed")

    def visit_Exec(self, node):  # Python 2 compatibility
        raise ValueError("exec statements are not allowed")

    def visit_ImportFrom(self, node):
        raise ValueError("Imports are not allowed")

def execute_user_code(submitted_code: str):
    """
    Execute user supplied Python code in a restricted environment.

    Parameters
    ----------
    submitted_code : str
        The code to execute.

    Returns
    -------
    Any
        Value of the variable `result` defined by the user code, if present;
        otherwise None.

    Raises
    ------
    ValueError
        If the code contains disallowed syntax or uses prohibited operations.
    """
    try:
        parsed = ast.parse(submitted_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    # Validate the AST for disallowed constructs
    SafeNodeVisitor().visit(parsed)

    # Prepare a safe execution environment
    exec_globals = {"__builtins__": SAFE_BUILTINS}
    exec_locals = {}

    # Execute the code
    try:
        exec(compile(parsed, filename="<user_code>", mode="exec"),
             exec_globals,
             exec_locals)
    except Exception as exc:
        raise ValueError(f"Error during execution: {exc}") from exc

    # Return the value of a variable named 'result', if defined
    return exec_locals.get("result", None)