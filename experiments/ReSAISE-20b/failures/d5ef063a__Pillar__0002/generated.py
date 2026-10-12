import ast
import io
import sys
from typing import Any, Dict

# ------------------------------------------------------------
# 1. Safe AST node visitor – only allows a small set of nodes
# ------------------------------------------------------------
class _SafeNodeVisitor(ast.NodeVisitor):
    """
    Traverses an AST and ensures that only a whitelist of nodes are present.
    Raises ValueError on any disallowed node.
    """
    # Allowed AST node types
    _ALLOWED_NODES = {
        ast.Module,
        ast.Expr,
        ast.Assign,
        ast.AugAssign,
        ast.Name,
        ast.Load,
        ast.Store,
        ast.Constant,
        ast.Num,          # for Python < 3.8
        ast.Str,          # for Python < 3.8
        ast.Tuple,
        ast.List,
        ast.Dict,
        ast.Set,
        ast.BinOp,
        ast.UnaryOp,
        ast.Compare,
        ast.BoolOp,
        ast.Call,
        ast.Attribute,
        ast.Subscript,
        ast.Index,       # for Python < 3.9
        ast.Slice,
        ast.keyword,
    }

    # Allowed operators (binary, unary, boolean, comparison)
    _ALLOWED_OPS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
        ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
        ast.FloorDiv,
        ast.Invert, ast.Not, ast.UAdd, ast.USub,
        ast.And, ast.Or,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        ast.Is, ast.IsNot, ast.In, ast.NotIn,
    }

    # Allowed function names (builtins)
    _ALLOWED_BUILTINS = {
        'print',
        'len',
        'range',
        'int',
        'float',
        'str',
        'bool',
        'list',
        'dict',
        'set',
        'tuple',
        'abs',
        'min',
        'max',
        'sum',
    }

    def visit(self, node: ast.AST) -> Any:
        if type(node) not in self._ALLOWED_NODES:
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        super().visit(node)

    def visit_BinOp(self, node: ast.BinOp) -> None:
        if type(node.op) not in self._ALLOWED_OPS:
            raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")
        self.generic_visit(node)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> None:
        if type(node.op) not in self._ALLOWED_OPS:
            raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
        self.generic_visit(node)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        if type(node.op) not in self._ALLOWED_OPS:
            raise ValueError(f"Disallowed boolean operator: {type(node.op).__name__}")
        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare) -> None:
        for op in node.ops:
            if type(op) not in self._ALLOWED_OPS:
                raise ValueError(f"Disallowed comparison operator: {type(op).__name__}")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        # Only allow calls to whitelisted builtins and no keyword arguments
        if isinstance(node.func, ast.Name):
            if node.func.id not in self._ALLOWED_BUILTINS:
                raise ValueError(f"Disallowed function call: {node.func.id}")
        else:
            # Disallow attribute calls (e.g., os.system)
            raise ValueError(f"Disallowed call type: {type(node.func).__name__}")

        for kw in node.keywords:
            raise ValueError(f"Disallowed keyword argument: {kw.arg}")

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        # Disallow attribute access (e.g., obj.attr)
        raise ValueError(f"Disallowed attribute access: {ast.dump(node)}")

    def visit_Subscript(self, node: ast.Subscript) -> None:
        # Disallow complex subscripting (e.g., obj[0][1])
        self.generic_visit(node)

    def visit_Index(self, node: ast.Index) -> None:
        # For Python <3.9
        self.generic_visit(node)

# ------------------------------------------------------------
# 2. Restricted execution environment
# ------------------------------------------------------------
def _restricted_globals() -> Dict[str, Any]:
    """
    Returns a dictionary containing only whitelisted builtins.
    No __import__ or other dangerous globals are provided.
    """
    safe_builtins = {name: __builtins__[name] for name in _SafeNodeVisitor._ALLOWED_BUILTINS}
    return {"__builtins__": safe_builtins}

# ------------------------------------------------------------
# 3. Main function
# ------------------------------------------------------------
def restricted_run_code(run_code: str) -> Any:
    """
    Execute a user supplied Python script in a restricted environment.

    Parameters
    ----------
    run_code : str
        The user's Python script as a string.

    Returns
    -------
    Any
        Output printed by the script, captured from stdout.
        If nothing is printed, returns None.

    Raises
    ------
    ValueError
        If the script contains disallowed syntax or operations.
    """
    # 1. Parse the code to ensure syntactic correctness
    try:
        tree = ast.parse(run_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in script: {exc}") from exc

    # 2. Validate the AST
    _SafeNodeVisitor().visit(tree)

    # 3. Prepare restricted globals & locals
    globs = _restricted_globals()
    locs: Dict[str, Any] = {}

    # 4. Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        exec(compile(tree, filename="<restricted>", mode="exec"), globs, locs)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None