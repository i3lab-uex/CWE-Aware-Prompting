import ast
from typing import Any, Optional

# --------------------------------------------------------------------------- #
#  Safe execution of a single snippet
# --------------------------------------------------------------------------- #

class ForbiddenNodeError(ValueError):
    """Raised when the snippet contains disallowed constructs."""


class SafeExecutor(ast.NodeVisitor):
    """
    Walks an AST and ensures that only safe nodes are present.
    Allowed constructs:
      - Literals, names, attributes (read-only)
      - Arithmetic and boolean operations
      - Comparisons, if/else, while loops, for loops over ranges or lists
      - Function definitions (no import)
      - Assignments to local names
    Forbidden constructs:
      - Import / ImportFrom
      - Call to dangerous built‑ins (open, exec, eval, compile, os.*, subprocess.*)
      - Attribute writes
      - Subprocess creation
    """

    # Whitelist of allowed node types
    _ALLOWED_NODES = {
        ast.Module,
        ast.Expr,
        ast.Assign,
        ast.AugAssign,
        ast.Name,
        ast.Load,
        ast.Store,
        ast.Constant,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.If,
        ast.For,
        ast.While,
        ast.FunctionDef,
        ast.Return,
        ast.arguments,
        ast.arg,
        ast.Call,
        ast.keyword,
        ast.Subscript,
        ast.Index,
        ast.Slice,
        ast.List,
        ast.Tuple,
        ast.Dict,
        ast.Set,
        ast.Attribute,
    }

    # Whitelist of allowed built‑ins
    _ALLOWED_BUILTINS = {
        "abs", "all", "any", "bool", "dict", "float",
        "int", "len", "list", "max", "min", "print",
        "range", "str", "sum", "tuple", "zip"
    }

    def __init__(self):
        self._found_forbidden = False

    def generic_visit(self, node: ast.AST):
        if type(node) not in self._ALLOWED_NODES:
            raise ForbiddenNodeError(f"Disallowed node type: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Disallow calls to dangerous built‑ins
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in self._ALLOWED_BUILTINS:
                raise ForbiddenNodeError(f"Call to forbidden function: {func_name}")
        elif isinstance(node.func, ast.Attribute):
            # Disallow any attribute call (e.g., os.system)
            raise ForbiddenNodeError("Attribute calls are forbidden")
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        raise ForbiddenNodeError("Import statements are forbidden")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        raise ForbiddenNodeError("Import statements are forbidden")

    def visit_Attribute(self, node: ast.Attribute):
        # Allow attribute access only for built‑ins (e.g., math.pi)
        if isinstance(node.value, ast.Name):
            if node.value.id not in self._ALLOWED_BUILTINS:
                raise ForbiddenNodeError(f"Attribute access to forbidden object: {node.value.id}")
        self.generic_visit(node)


def execute_python_code(snippet_code: str) -> Optional[Any]:
    """
    Execute a user supplied Python snippet in a safe, restricted environment.

    Parameters
    ----------
    snippet_code : str
        The Python code to execute.

    Returns
    -------
    Optional[Any]
        If the snippet ends with an expression, its value is returned.
        Otherwise None is returned.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or execution errors.
    """
    try:
        # Parse the code to an AST
        tree = ast.parse(snippet_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python syntax: {exc}") from exc

    # Validate the AST
    validator = SafeExecutor()
    try:
        validator.visit(tree)
    except ForbiddenNodeError as exc:
        raise ValueError(f"Forbidden operation detected: {exc}") from exc

    # Prepare a minimal execution environment
    safe_globals = {"__builtins__": {k: __builtins__[k] for k in SafeExecutor._ALLOWED_BUILTINS}}
    safe_locals = {}

    # Execute the code
    try:
        exec(compile(tree, filename="<safe>", mode="exec"), safe_globals, safe_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    # If the last statement is an expression, evaluate it
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        expr_node = tree.body[-1].value
        try:
            return eval(compile(ast.Expression(expr_node), filename="<safe>", mode="eval"),
                        safe_globals, safe_locals)
        except Exception as exc:
            raise ValueError(f"Evaluation error: {exc}") from exc

    return None