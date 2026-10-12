import ast
from typing import Any, Optional

# Allowed AST node types for a safe snippet
_ALLOWED_NODES = {
    # Expressions
    ast.Expression,
    ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
    ast.Call, ast.Name, ast.Constant,
    ast.Attribute, ast.Subscript, ast.Index,
    ast.Tuple, ast.List, ast.Dict,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.LShift, ast.RShift, ast.BitOr, ast.BitAnd, ast.BitXor,
    ast.FloorDiv, ast.Invert, ast.Not, ast.UAdd, ast.USub,
    # Comparisons
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Logical
    ast.And, ast.Or,
    # Assignments
    ast.Assign, ast.AugAssign,
    # Control flow
    ast.IfExp,  # ternary expressions
}

# Disallowed node types that would allow unsafe behavior
_DISALLOWED_NODES = {
    ast.Import, ast.ImportFrom,
    ast.Exec, ast.Call,  # calls are allowed only to builtins
    ast.FunctionDef, ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.Lambda,
    ast.Global, ast.Nonlocal,
    ast.With, ast.AsyncWith,
    ast.Try, ast.ExceptHandler,
    ast.Delete,
}

# Allowed builtins
_ALLOWED_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'chr', 'complex',
    'dict', 'divmod', 'float', 'int', 'len',
    'list', 'max', 'min', 'pow', 'range', 'round',
    'str', 'sum', 'tuple'
}

class SafeVisitor(ast.NodeVisitor):
    def visit(self, node: ast.AST) -> Any:
        if type(node) in _DISALLOWED_NODES:
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")
        if not isinstance(node, tuple(_ALLOWED_NODES)):
            raise ValueError(f"Unsupported syntax: {type(node).__name__}")
        return super().visit(node)

    def visit_Call(self, node: ast.Call):
        # Only allow calls to builtins from the whitelist
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in _ALLOWED_BUILTINS:
                raise ValueError(f"Calling disallowed function '{func_name}'")
        else:
            # e.g., attribute calls like math.sqrt are disallowed
            raise ValueError("Only direct builtin function calls allowed")
        # Validate arguments recursively
        for arg in node.args:
            self.visit(arg)
        for keyword in node.keywords:
            self.visit(keyword.value)

def run_python_snippet(python_snippet: str) -> Optional[Any]:
    """
    Execute a small Python snippet safely.

    Parameters
    ----------
    python_snippet : str
        The code to run.  It may contain expressions, assignments,
        and simple control flow but cannot import modules or define
        functions/classes.

    Returns
    -------
    Any | None
        The value of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed or unsafe constructs.
    """
    # Parse into an AST module
    try:
        parsed = ast.parse(python_snippet, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from None

    # Validate the AST
    SafeVisitor().visit(parsed)

    # Prepare a safe execution environment
    safe_globals = {"__builtins__": {name: __builtins__[name] for name in _ALLOWED_BUILTINS}}
    safe_locals = {}

    # Execute the code
    exec(compile(parsed, filename="<safe_snippet>", mode="exec"), safe_globals, safe_locals)

    # Determine the result: if the last statement is an expression, return its value
    # In exec mode, expressions are not returned; we can capture them by checking the last node
    if parsed.body:
        last_stmt = parsed.body[-1]
        if isinstance(last_stmt, ast.Expr):
            # Evaluate the expression in the same context
            expr_code = compile(ast.Expression(last_stmt.value), filename="<safe_snippet>", mode="eval")
            return eval(expr_code, safe_globals, safe_locals)

    return None