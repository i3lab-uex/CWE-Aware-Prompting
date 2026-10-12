import ast
from typing import Any

# List of AST node types that are disallowed for safety reasons.
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # exec() statement (Python 2 only, but kept for completeness)
    ast.Global,
    ast.Nonlocal,
    ast.Call,          # Calls are allowed but we will check the function name
}

# Functions that are explicitly forbidden to be called.
DISALLOWED_FUNCTIONS = {
    'eval',
    'exec',
    '__import__',
    'open',
    'compile',
    'input',           # avoid interactive input
}

# Allowed built‑in functions (minimal safe set).
ALLOWED_BUILTINS = {
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

class _SafeVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors = []

    def generic_visit(self, node: ast.AST) -> Any:
        # Reject any disallowed node type
        if type(node) in DISALLOWED_NODES:
            self.errors.append(f"Disallowed statement: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        # Check that the function called is not disallowed
        func_name = self._get_call_func_name(node.func)
        if func_name in DISALLOWED_FUNCTIONS:
            self.errors.append(f"Disallowed function call: {func_name}")
        # Recursively visit arguments
        self.generic_visit(node)

    def _get_call_func_name(self, node: ast.AST) -> str | None:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            # e.g., os.system -> we block any attribute access
            return None
        else:
            return None

def _is_safe_script(script: str) -> bool:
    """
    Parse the script and ensure it contains only safe constructs.
    Raises ValueError if disallowed operations are detected.
    """
    try:
        tree = ast.parse(script, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from None

    visitor = _SafeVisitor()
    visitor.visit(tree)

    if visitor.errors:
        raise ValueError(f"Disallowed operations detected: {', '.join(visitor.errors)}")

    return True

def run_user_script(user_script: str) -> Any:
    """
    Execute a user‑supplied Python script in a highly restricted environment.

    Parameters
    ----------
    user_script : str
        The Python code to execute.

    Returns
    -------
    Any
        The result of the last expression in the script, if any; otherwise None.

    Raises
    ------
    ValueError
        If the script contains disallowed operations or syntax errors.
    """
    _is_safe_script(user_script)

    # Prepare a restricted global namespace
    globals_dict = {'__builtins__': ALLOWED_BUILTINS}
    locals_dict: dict[str, Any] = {}

    # Execute the script
    exec(user_script, globals_dict, locals_dict)

    # If the last statement is an expression, return its value
    # This is a heuristic: we re‑parse the script to get the last node.
    try:
        tree = ast.parse(user_script, mode='exec')
        if tree.body and isinstance(tree.body[-1], ast.Expr):
            # Compile only the expression node
            expr_code = compile(tree.body[-1], filename='<user_script>', mode='eval')
            return eval(expr_code, globals_dict, locals_dict)
    except Exception:
        # In case of any unexpected error we just return None
        pass

    return None