import ast
from typing import Any

# Allowed binary operators for arithmetic expressions
ALLOWED_BINOPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div,
    ast.FloorDiv, ast.Mod, ast.Pow
}

# Allowed unary operators for arithmetic expressions
ALLOWED_UNARYOPS = {ast.UAdd, ast.USub}

# Allowed built‑in functions for simple string or numeric operations
ALLOWED_BUILTINS = {
    'len', 'abs', 'round',
    # string methods accessed via attribute access are allowed later
}

class SafeEvalVisitor(ast.NodeVisitor):
    """
    Visitor that ensures only safe nodes are present in the AST.
    """
    def __init__(self):
        self.is_safe = True

    def generic_visit(self, node: ast.AST) -> None:
        # If any node is not explicitly allowed, mark unsafe
        if isinstance(node, (ast.Module, ast.Expr)):
            super().generic_visit(node)
        elif isinstance(node, ast.Expression):
            self.visit(node.body)
        else:
            self.is_safe = False

    def visit_Expr(self, node: ast.Expr) -> None:
        self.visit(node.value)

    def visit_Call(self, node: ast.Call) -> None:
        # Only allow calls to whitelisted builtins
        if isinstance(node.func, ast.Name):
            if node.func.id not in ALLOWED_BUILTINS:
                self.is_safe = False
        else:
            self.is_safe = False

    def visit_Name(self, node: ast.Name) -> None:
        # Only allow builtins or literals (no variables)
        if node.id not in ALLOWED_BUILTINS:
            self.is_safe = False

    def visit_BinOp(self, node: ast.BinOp) -> None:
        if type(node.op) not in ALLOWED_BINOPS:
            self.is_safe = False
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> None:
        if type(node.op) not in ALLOWED_UNARYOPS:
            self.is_safe = False
        self.visit(node.operand)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        # Allow string methods that return strings or numbers
        if isinstance(node.value, ast.Str):
            self.visit(node.value)
        else:
            # Reject attribute access on non-constants
            self.is_safe = False

    def visit_Subscript(self, node: ast.Subscript) -> None:
        # Disallow subscript access
        self.is_safe = False

    def visit_List(self, node: ast.List) -> None:
        self.is_safe = False

    def visit_Tuple(self, node: ast.Tuple) -> None:
        self.is_safe = False

    def visit_Dict(self, node: ast.Dict) -> None:
        self.is_safe = False

    def visit_Set(self, node: ast.Set) -> None:
        self.is_safe = False

    def visit_Lambda(self, node: ast.Lambda) -> None:
        self.is_safe = False

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.is_safe = False

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.is_safe = False

    def visit_Import(self, node: ast.Import) -> None:
        self.is_safe = False

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        self.is_safe = False

def run_user_script(script_input: str) -> str:
    """
    Execute a small user supplied script safely.
    
    Parameters
    ----------
    script_input : str
        The Python code to execute.  Only arithmetic expressions,
        string literals, and whitelisted built‑ins are allowed.
    
    Returns
    -------
    str
        The string representation of the result, or 'Execution Blocked!'
        if the script is unsafe.
    """
    try:
        # Parse the code into an AST expression
        tree = ast.parse(script_input, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Verify safety of the AST
    visitor = SafeEvalVisitor()
    visitor.visit(tree)
    if not visitor.is_safe:
        return 'Execution Blocked!'

    # Prepare a restricted environment
    safe_globals = {name: __builtins__[name] for name in ALLOWED_BUILTINS}
    # For string methods we need the str class itself
    safe_globals['str'] = str

    try:
        result: Any = eval(compile(tree, filename='<user_script>', mode='eval'),
                           {"__builtins__": None}, safe_globals)
    except Exception:
        return 'Execution Blocked!'

    # Convert result to string for consistent output
    return str(result)