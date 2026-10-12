import ast
import builtins
from types import ModuleType

# --------------------------------------------------------------------------- #
#   Restricted execution environment
# --------------------------------------------------------------------------- #

SAFE_BUILTINS = {
    # Basic types and functions that are generally safe
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
    'str': str,
    'sum': sum,
    # Some math functions
    'math': __import__('math'),
}

# --------------------------------------------------------------------------- #
#   AST visitor to detect prohibited constructs
# --------------------------------------------------------------------------- #

class SafetyChecker(ast.NodeVisitor):
    """
    Raises ValueError if the AST contains disallowed nodes.
    """

    DISALLOWED_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,          # Python 2 only; kept for completeness
        ast.Call,          # calls will be filtered further
    )

    DISALLOWED_CALLS = {
        'open',   # file operations
        'eval',
        'exec',
        '__import__',
    }

    def visit(self, node):
        if isinstance(node, self.DISALLOWED_NODES):
            raise ValueError(f"Disallowed statement: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node: ast.Call):
        # Disallow calls to unsafe functions
        func_name = self._get_call_func_name(node)
        if func_name in self.DISALLOWED_CALLS:
            raise ValueError(f"Disallowed function call: {func_name}")
        self.generic_visit(node)

    def _get_call_func_name(self, node: ast.Call):
        """
        Resolve the name of a called function if possible.
        """
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            # e.g., os.system -> disallow any attribute call
            return node.func.attr
        return ""

# --------------------------------------------------------------------------- #
#   The main function
# --------------------------------------------------------------------------- #

def execute_user_code(submitted_code: str):
    """
    Execute a user-provided Python script in a restricted environment.

    Parameters
    ----------
    submitted_code : str
        The code to execute. May contain multiple statements.

    Returns
    -------
    result : Any or None
        The value of the last expression if the script consists solely of a
        single expression; otherwise None.

    Raises
    ------
    ValueError
        If the code contains prohibited operations or has syntax errors.
    """

    # 1. Syntax check
    try:
        parsed = ast.parse(submitted_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error: {exc}") from None

    # 2. Safety check
    checker = SafetyChecker()
    try:
        checker.visit(parsed)
    except ValueError as exc:
        raise

    # 3. Prepare a safe globals dictionary
    safe_globals = {"__builtins__": SAFE_BUILTINS}

    # 4. Execute the code
    exec(compile(parsed, filename="<user_script>", mode="exec"), safe_globals)

    # 5. If the user submitted a single expression, evaluate and return it
    if len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr):
        try:
            result = eval(compile(parsed, filename="<user_expr>", mode="eval"),
                          safe_globals)
            return result
        except Exception:
            # If evaluation fails, ignore and return None
            return None

    return None