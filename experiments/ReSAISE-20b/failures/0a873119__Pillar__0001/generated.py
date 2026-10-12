import ast
import math
from typing import Any

# Allowed modules and their safe members
SAFE_MODULES = {
    "math": math,
}

# Whitelist of allowed AST node types
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.Load,
    ast.Store,
    ast.Subscript,
    ast.Index,
    ast.Slice,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
}

# Whitelist of allowed operators
ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.FloorDiv,
    ast.UAdd, ast.USub, ast.Not, ast.Invert,
    ast.And, ast.Or,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Is, ast.IsNot, ast.In, ast.NotIn
}

class SafeVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.last_expr = None

    def generic_visit(self, node: ast.AST):
        if type(node) not in ALLOWED_NODES:
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Import(self, node: ast.Import):
        raise ValueError("Import statements are not allowed")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        raise ValueError("Import statements are not allowed")

    def visit_Call(self, node: ast.Call):
        # Allow only calls to functions from SAFE_MODULES
        if isinstance(node.func, ast.Attribute):
            if not (isinstance(node.func.value, ast.Name) and
                    node.func.value.id in SAFE_MODULES):
                raise ValueError("Only functions from safe modules are allowed")
        elif isinstance(node.func, ast.Name):
            if node.func.id not in SAFE_MODULES:
                raise ValueError("Only functions from safe modules are allowed")
        else:
            raise ValueError("Unsupported call structure")

        # Validate arguments
        for arg in node.args:
            self.visit(arg)
        for kw in node.keywords:
            self.visit(kw.value)

    def visit_BinOp(self, node: ast.BinOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed operator: {type(node.op).__name__}")
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node: ast.UnaryOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed operator: {type(node.op).__name__}")
        self.visit(node.operand)

    def visit_BoolOp(self, node: ast.BoolOp):
        if type(node.op) not in ALLOWED_OPERATORS:
            raise ValueError(f"Disallowed operator: {type(node.op).__name__}")
        for val in node.values:
            self.visit(val)

    def visit_Compare(self, node: ast.Compare):
        if any(type(op) not in ALLOWED_OPERATORS for op in node.ops):
            raise ValueError("Disallowed comparison operator")
        self.visit(node.left)
        for comparator in node.comparators:
            self.visit(comparator)

    def visit_Expr(self, node: ast.Expr):
        # Capture the last expression's value
        self.last_expr = node.value
        self.generic_visit(node)

def safe_run_script(script_code: str) -> Any:
    """
    Execute user-provided Python code in a highly restricted environment.

    Parameters
    ----------
    script_code : str
        The Python code submitted by the user.

    Returns
    -------
    Any
        The value of the last expression in the script, or None if there is no result.

    Raises
    ------
    ValueError
        If the script contains prohibited operations, imports, or invalid syntax.
    """
    try:
        tree = ast.parse(script_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from None

    # Validate the AST
    visitor = SafeVisitor()
    visitor.visit(tree)

    # Prepare restricted globals
    safe_globals = {"__builtins__": None}
    for mod_name, mod_obj in SAFE_MODULES.items():
        safe_globals[mod_name] = mod_obj

    # Compile and execute
    try:
        compiled = compile(tree, filename="<safe_script>", mode="exec")
        exec(compiled, safe_globals, {})
    except Exception as exc:
        raise ValueError(f"Script execution failed: {exc}") from None

    # Return the result of the last expression, if any
    return visitor.last_expr.value if hasattr(visitor, "last_expr") else None