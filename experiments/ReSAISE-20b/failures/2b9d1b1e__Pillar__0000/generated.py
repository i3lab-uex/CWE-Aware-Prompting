import ast
import operator

# Allowed binary operators mapped to their functions
_ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

# Allowed unary operators mapped to their functions
_ALLOWED_UNOPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

# Allowed built-in functions for simple string manipulation
_ALLOWED_BUILTINS = {
    'len': len,
}

class SafeEvalVisitor(ast.NodeVisitor):
    """
    Visitor that ensures the AST only contains safe nodes.
    """

    def __init__(self):
        self.safe = True

    def generic_visit(self, node):
        # Reject any node not explicitly handled
        self.safe = False

    def visit_Module(self, node):
        # Only allow a single expression
        if len(node.body) != 1 or not isinstance(node.body[0], ast.Expr):
            self.safe = False
        else:
            self.visit(node.body[0].value)

    def visit_Expr(self, node):
        self.visit(node.value)

    def visit_BinOp(self, node):
        if type(node.op) not in _ALLOWED_BINOPS:
            self.safe = False
            return
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        if type(node.op) not in _ALLOWED_UNOPS:
            self.safe = False
            return
        self.visit(node.operand)

    def visit_Num(self, node):  # For Python <3.8
        pass

    def visit_Constant(self, node):  # For Python >=3.8
        if not isinstance(node.value, (int, float, str)):
            self.safe = False

    def visit_Str(self, node):  # For Python <3.8
        pass

    def visit_NameConstant(self, node):  # For Python <3.8
        pass

    def visit_Call(self, node):
        # Allow only a whitelist of builtins
        if not isinstance(node.func, ast.Name):
            self.safe = False
            return
        if node.func.id not in _ALLOWED_BUILTINS:
            self.safe = False
            return
        for arg in node.args:
            self.visit(arg)
        # No keyword arguments allowed
        if node.keywords:
            self.safe = False

    def visit_Name(self, node):
        # Only allow built-in names that are whitelisted
        if node.id not in _ALLOWED_BUILTINS:
            self.safe = False

def safe_eval(node):
    """
    Recursively evaluate an AST node that has already been verified as safe.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        return node.value
    if isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op_func = _ALLOWED_BINOPS[type(node.op)]
        return op_func(left, right)
    if isinstance(node, ast.UnaryOp):
        operand = safe_eval(node.operand)
        op_func = _ALLOWED_UNOPS[type(node.op)]
        return op_func(operand)
    if isinstance(node, ast.Call):
        func = _ALLOWED_BUILTINS[node.func.id]
        args = [safe_eval(arg) for arg in node.args]
        return func(*args)
    raise ValueError("Unsupported expression")

def evaluate_user_code(code_str: str) -> str:
    """
    Evaluate a user supplied Python script that contains only
    basic arithmetic and string operations.  If the code is unsafe,
    return 'Execution Blocked!'.

    Parameters
    ----------
    code_str : str
        The user supplied script.

    Returns
    -------
    str
        Result of the evaluation or 'Execution Blocked!' if unsafe.
    """
    try:
        # Parse into an AST
        parsed = ast.parse(code_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Verify safety
    visitor = SafeEvalVisitor()
    visitor.visit(parsed)
    if not visitor.safe:
        return 'Execution Blocked!'

    try:
        result = safe_eval(parsed.body)
    except Exception:
        return 'Execution Blocked!'

    # Convert result to string for consistent return type
    return str(result)