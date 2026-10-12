import ast
import builtins
import io
import sys
from types import ModuleType, FunctionType
from typing import Any, Dict

# --------------------------------------------------------------------------- #
# 1. Define a whitelist of safe built‑in functions and constants
# --------------------------------------------------------------------------- #

SAFE_BUILTINS: Dict[str, Any] = {
    name: getattr(builtins, name)
    for name in [
        "abs",
        "all",
        "any",
        "ascii",
        "bin",
        "bool",
        "bytes",
        "chr",
        "complex",
        "dict",
        "divmod",
        "enumerate",
        "filter",
        "float",
        "format",
        "frozenset",
        "hash",
        "hex",
        "int",
        "isinstance",
        "issubclass",
        "iter",
        "len",
        "list",
        "map",
        "max",
        "min",
        "next",
        "oct",
        "ord",
        "pow",
        "print",          # allow printing
        "range",
        "repr",
        "reversed",
        "round",
        "set",
        "slice",
        "sorted",
        "str",
        "sum",
        "tuple",
        "type",
        "zip",
    ]
}

# --------------------------------------------------------------------------- #
# 2. Visitor to validate the AST
# --------------------------------------------------------------------------- #

class SafeASTValidator(ast.NodeVisitor):
    """
    Traverses an AST and raises ValueError if any disallowed node is found.
    """

    # Nodes that are inherently dangerous
    DISALLOWED_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,          # Python 2; present only if user passes older code
        ast.Call,
    )

    # Allowed call targets (by name)
    ALLOWED_CALLS = {
        "print",
        "__import__",   # Not allowed, but we will filter calls explicitly
    }

    def __init__(self):
        super().__init__()

    def generic_visit(self, node: ast.AST) -> Any:
        if isinstance(node, self.DISALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        return super().generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        # Reject calls to __import__, eval, exec, open, etc.
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            # Allow only whitelisted built‑ins
            if func_name not in SAFE_BUILTINS:
                raise ValueError(f"Call to forbidden function '{func_name}'")
        elif isinstance(node.func, ast.Attribute):
            # Reject attribute calls like os.system(), subprocess.Popen(), etc.
            raise ValueError("Attribute calls are forbidden")
        else:
            # Other call forms (e.g., lambda()) are disallowed
            raise ValueError("Unsupported call form")

        # Recursively visit arguments
        for arg in node.args:
            self.visit(arg)
        for keyword in node.keywords:
            self.visit(keyword.value)

        return super().generic_visit(node)


# --------------------------------------------------------------------------- #
# 3. Main execution function
# --------------------------------------------------------------------------- #

def process_python_code(code_str: str) -> Any:
    """
    Safely executes a user‑supplied Python snippet.

    Parameters
    ----------
    code_str : str
        The code to execute. Must be valid Python syntax.

    Returns
    -------
    Any
        The value of the last expression in the snippet, if any; otherwise None.

    Raises
    ------
    ValueError
        If the code contains forbidden operations or invalid syntax.
    """
    # 1. Parse the code into an AST
    try:
        parsed = ast.parse(code_str, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from None

    # 2. Validate the AST
    validator = SafeASTValidator()
    try:
        validator.visit(parsed)
    except ValueError as exc:
        raise ValueError(f"Forbidden operation detected: {exc}") from None

    # 3. Prepare a restricted execution environment
    safe_globals: Dict[str, Any] = {"__builtins__": SAFE_BUILTINS}
    safe_locals: Dict[str, Any] = {}

    # 4. Capture stdout to detect print statements
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    # 5. Execute the code
    try:
        exec(compile(parsed, filename="<safe>", mode="exec"), safe_globals, safe_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    # 6. If the last statement was an expression, evaluate and return its value
    if parsed.body:
        last_stmt = parsed.body[-1]
        if isinstance(last_stmt, ast.Expr):
            try:
                # Evaluate the expression in the same environment
                expr_value = eval(compile(ast.Expression(last_stmt.value), filename="<safe>", mode="eval"),
                                  safe_globals, safe_locals)
                return expr_value
            except Exception:
                # If evaluation fails, ignore and fall through to None
                pass

    return None