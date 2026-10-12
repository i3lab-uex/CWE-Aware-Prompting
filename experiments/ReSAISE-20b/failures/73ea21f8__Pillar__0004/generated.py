import ast
from typing import Any, Optional

# Allowed built‑in functions and modules
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "pow": pow,
    "range": range,
    "round": round,
    "sum": sum,
    # add more safe functions as needed
}

SAFE_GLOBALS = {
    "__builtins__": SAFE_BUILTINS,
    "math": __import__("math"),
}

# Nodes that are considered unsafe
UNSAFE_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # Python 2 only but keep for completeness
    ast.Call,          # calls are allowed only to safe builtins or math functions
)

# Disallowed names in function calls
DISALLOWED_CALL_NAMES = {
    "eval",
    "exec",
    "open",
    "__import__",
    "compile",
}

class _UnsafeCodeError(ValueError):
    pass

class _ASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self._unsafe = False

    def generic_visit(self, node: ast.AST) -> None:
        if isinstance(node, UNSAFE_NODES):
            self._unsafe = True
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        # Allow calls only to safe builtins or math functions
        if isinstance(node.func, ast.Name):
            name = node.func.id
            if name in DISALLOWED_CALL_NAMES:
                self._unsafe = True
        elif isinstance(node.func, ast.Attribute):
            # e.g., math.sqrt(...)
            if (
                isinstance(node.func.value, ast.Name)
                and node.func.value.id == "math"
            ):
                # math functions are allowed
                pass
            else:
                self._unsafe = True
        else:
            # other complex call expressions are disallowed
            self._unsafe = True
        super().generic_visit(node)

def _check_safety(code: str) -> None:
    """
    Parse the code and raise ValueError if it contains unsafe constructs.
    """
    try:
        tree = ast.parse(code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code snippet: {exc}") from exc

    visitor = _ASTVisitor()
    visitor.visit(tree)

    if visitor._unsafe:
        raise ValueError("Code snippet contains prohibited actions")

def run_code_snippet(user_code: str) -> Optional[Any]:
    """
    Execute a user-provided Python code snippet in a restricted environment.
    
    Parameters
    ----------
    user_code : str
        The Python code to execute. It may contain one or more statements.
    
    Returns
    -------
    Any | None
        The value of the last expression if present, otherwise ``None``.
    
    Raises
    ------
    ValueError
        If the code contains disallowed operations (imports, eval, open, etc.).
    """
    _check_safety(user_code)

    # Determine if the snippet is a single expression
    try:
        expr_ast = ast.parse(user_code, mode="eval")
        # If parsing as eval succeeds, evaluate and return the result
        compiled = compile(expr_ast, "<string>", "eval")
        return eval(compiled, SAFE_GLOBALS)
    except SyntaxError:
        # Not a single expression; execute as statements
        compiled = compile(user_code, "<string>", "exec")
        exec(compiled, SAFE_GLOBALS)
        return None