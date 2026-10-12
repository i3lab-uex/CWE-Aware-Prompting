import ast
from typing import Any, Dict

# Whitelist of safe built‑in functions and constants
SAFE_BUILTINS: Dict[str, Any] = {
    'print': print,
    'len': len,
    'range': range,
    'int': int,
    'float': float,
    'str': str,
    'list': list,
    'dict': dict,
    'set': set,
    'tuple': tuple,
    'bool': bool,
    'abs': abs,
    'min': min,
    'max': max,
}

# Names that are explicitly forbidden
FORBIDDEN_NAMES = {
    '__import__',
    'eval',
    'exec',
    'open',
    'compile',
    'input',
    'locals',
    'globals',
    'vars',
}

class _SafeVisitor(ast.NodeVisitor):
    """AST visitor that ensures the snippet only uses safe constructs."""

    def visit_Import(self, node: ast.Import):
        raise ValueError("Import statements are not allowed")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        raise ValueError("Import statements are not allowed")

    def visit_Call(self, node: ast.Call):
        # Disallow calls to forbidden built‑ins or other dangerous functions
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in FORBIDDEN_NAMES:
                raise ValueError(f"Call to forbidden function '{func_name}'")
        # Disallow attribute calls like obj.__dict__() etc.
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr in FORBIDDEN_NAMES:
                raise ValueError(f"Attribute call to forbidden '{node.func.attr}'")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        # Prevent access to private or special attributes
        if node.attr.startswith('__') and node.attr.endswith('__'):
            raise ValueError(f"Access to special attribute '{node.attr}' is forbidden")
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        # Prevent use of names that are not in the whitelist
        if isinstance(node.ctx, ast.Load) and node.id in FORBIDDEN_NAMES:
            raise ValueError(f"Use of forbidden name '{node.id}'")
        self.generic_visit(node)

def run_python_snippet(python_snippet: str) -> Any:
    """
    Execute a user‑provided Python snippet in a restricted environment.

    Parameters
    ----------
    python_snippet : str
        The Python code to execute.

    Returns
    -------
    Any
        Result of the last expression if it assigns to a variable named 'result',
        otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed constructs.
    """
    # 1. Parse the code into an AST and validate it
    try:
        parsed = ast.parse(python_snippet, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from exc

    _SafeVisitor().visit(parsed)

    # 2. Prepare a restricted global namespace
    safe_globals = {'__builtins__': SAFE_BUILTINS}
    # 3. Execute the snippet
    exec(compile(parsed, filename='<snippet>', mode='exec'), safe_globals)

    # 4. Return the value of 'result' if it was defined
    return safe_globals.get('result', None)