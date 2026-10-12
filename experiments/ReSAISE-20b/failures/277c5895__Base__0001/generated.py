import ast
from types import FunctionType

# A very small whitelist of safe built‑ins that users are allowed to use
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
}

# Disallowed AST node types
PROHIBITED_NODES = (
    ast.Import,          # import statements
    ast.ImportFrom,      # from … import …
    ast.Exec,            # exec() statement (Python 2)
    ast.Call,            # calls to builtins not in SAFE_BUILTINS
)

# Disallowed attribute names (e.g., __dict__, __class__)
PROHIBITED_ATTRS = {'__dict__', '__class__', '__bases__', '__globals__',
                    '__code__', '__closure__', '__func__'}

class _SafetyVisitor(ast.NodeVisitor):
    """
    Visitor that raises ValueError if prohibited nodes or attributes are found.
    """

    def visit_Import(self, node):
        raise ValueError("Import statements are not allowed")

    def visit_ImportFrom(self, node):
        raise ValueError("Import statements are not allowed")

    def visit_Call(self, node):
        # Allow calls only to whitelisted built‑ins
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in SAFE_BUILTINS:
                raise ValueError(f"Call to unsafe function '{func_name}' is not allowed")
        elif isinstance(node.func, ast.Attribute):
            # disallow attribute access to __dict__ etc.
            if node.func.attr in PROHIBITED_ATTRS:
                raise ValueError(f"Access to attribute '{node.func.attr}' is prohibited")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if node.attr in PROHIBITED_ATTRS:
            raise ValueError(f"Access to attribute '{node.attr}' is prohibited")
        self.generic_visit(node)

def execute_user_code(submitted_code: str):
    """
    Execute a user‑supplied Python script in a highly restricted environment.

    Parameters
    ----------
    submitted_code : str
        The code to execute.

    Returns
    -------
    object or None
        The value of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the code contains prohibited operations or has syntax errors.
    """
    # 1. Syntax check and AST analysis
    try:
        parsed = ast.parse(submitted_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in submitted code: {exc}") from None

    # 2. Walk the AST to detect disallowed constructs
    _SafetyVisitor().visit(parsed)

    # 3. Prepare a restricted execution environment
    safe_globals = {'__builtins__': SAFE_BUILTINS}
    local_vars = {}

    # 4. Execute the code
    try:
        exec(compile(parsed, filename="<user_code>", mode="exec"), safe_globals, local_vars)
    except Exception as exc:
        # Any runtime exception is reported back to the caller
        raise ValueError(f"Runtime error during execution: {exc}") from None

    # 5. If the last statement is an expression, return its value
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        expr_code = compile(ast.Expression(body=parsed.body[-1].value), filename="<user_expr>", mode="eval")
        return eval(expr_code, safe_globals, local_vars)

    return None