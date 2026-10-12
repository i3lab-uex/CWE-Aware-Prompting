import ast

# List of builtin functions that are considered safe for arithmetic / string operations.
SAFE_BUILTINS = {
    "abs": abs,
    "min": min,
    "max": max,
    "len": len,
    "str": str,
    "int": int,
    "float": float,
}

# Node types that are allowed in a safe expression.
ALLOWED_NODES = (
    ast.Expression,
    ast.Module,
    ast.Expr,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Constant,   # Python 3.8+: numbers, strings, booleans, None
    ast.Num,
    ast.Str,
    ast.NameConstant,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Subscript,
    ast.Index,      # for slicing
    ast.Slice,
)

# Operators that are allowed.
ALLOWED_OPERATORS = (
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitXor, ast.BitAnd, ast.UAdd, ast.USub,
    ast.Invert, ast.Not,
    ast.And, ast.Or,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Is, ast.IsNot, ast.In, ast.NotIn
)

class SafeNodeVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        super().generic_visit(node)

    def visit_BinOp(self, node):
        if not isinstance(node.op, ALLOWED_OPERATORS):
            raise ValueError(f"Disallowed operator: {type(node.op).__name__}")
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        if not isinstance(node.op, ALLOWED_OPERATORS):
            raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        if not isinstance(node.op, ALLOWED_OPERATORS):
            raise ValueError(f"Disallowed bool operator: {type(node.op).__name__}")
        self.generic_visit(node)

    def visit_Compare(self, node):
        for op in node.ops:
            if not isinstance(op, ALLOWED_OPERATORS):
                raise ValueError(f"Disallowed comparison operator: {type(op).__name__}")
        self.generic_visit(node)

    def visit_Call(self, node):
        # Only allow calls to safe builtins and methods on string/number objects.
        if isinstance(node.func, ast.Name):
            if node.func.id not in SAFE_BUILTINS:
                raise ValueError(f"Disallowed function call: {node.func.id}")
        elif isinstance(node.func, ast.Attribute):
            # Allow any attribute call on string/number objects (e.g., "hello".upper())
            pass
        else:
            raise ValueError("Unsupported function call type")
        self.generic_visit(node)

    def visit_Subscript(self, node):
        if not isinstance(node.slice, (ast.Index, ast.Slice)):
            raise ValueError("Unsupported subscript type")
        self.generic_visit(node)

def execute_user_code(user_code: str) -> str:
    """
    Safely evaluate a small Python expression or script that performs
    basic arithmetic or string operations.

    Returns:
        str: The evaluated result converted to a string, or
             'Execution Blocked!' if the code contains disallowed operations.
    """
    try:
        # Parse into an AST. Use mode='eval' if it's a single expression,
        # otherwise use 'exec' for simple statements (e.g., assignments).
        try:
            tree = ast.parse(user_code, mode='eval')
        except SyntaxError:
            # Fallback to exec mode; only allow a single expression or assignment.
            tree = ast.parse(user_code, mode='exec')

        # Ensure the AST contains only safe nodes.
        SafeNodeVisitor().visit(tree)

        # Prepare a restricted environment
        safe_globals = {"__builtins__": None}
        safe_locals = {}
        # Inject allowed builtins
        safe_globals.update(SAFE_BUILTINS)

        # Evaluate or execute the code
        if isinstance(tree, ast.Expression):
            result = eval(compile(tree, filename="<user>", mode="eval"),
                          safe_globals, safe_locals)
        else:
            exec(compile(tree, filename="<user>", mode="exec"),
                 safe_globals, safe_locals)
            # For exec we try to return the value of the last expression if any.
            result = safe_locals.get("_", None)

        return str(result)
    except Exception:
        # Any exception (including disallowed nodes) results in blocking.
        return "Execution Blocked!"