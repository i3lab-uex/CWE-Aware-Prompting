import ast

# Allowed AST node types and operators for safe evaluation
ALLOWED_NODES = {
    ast.Expression,
    ast.Module,
    ast.Expr,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # numeric literals (Python <3.8)
    ast.Constant,     # numeric/string/None literals (Python 3.8+)
    ast.Str,
    ast.NameConstant, # True/False/None in older Python
    ast.Call,
    ast.Name,
    ast.Load,
}

ALLOWED_BINOPS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
    ast.Pow, ast.FloorDiv
}

ALLOWED_UNARYOPS = {
    ast.UAdd, ast.USub,
}

# Functions that are explicitly safe to call
SAFE_FUNCTIONS = {
    "len": len,
    "abs": abs,
    "min": min,
    "max": max,
    # add more safe functions if needed
}

class SafeEvaluator(ast.NodeVisitor):
    def __init__(self, code: str):
        self.code = code
        self.parsed = ast.parse(code, mode="eval")

    def visit(self, node):
        if type(node) not in ALLOWED_NODES:
            raise ValueError(f"Disallowed node: {type(node).__name__}")
        if isinstance(node, ast.BinOp):
            if type(node.op) not in ALLOWED_BINOPS:
                raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")
        if isinstance(node, ast.UnaryOp):
            if type(node.op) not in ALLOWED_UNARYOPS:
                raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
        if isinstance(node, ast.Call):
            # Only allow calls to known safe functions
            if not (isinstance(node.func, ast.Name) and node.func.id in SAFE_FUNCTIONS):
                raise ValueError(f"Disallowed function call: {ast.dump(node)}")
        return super().visit(node)

    def eval(self):
        self.visit(self.parsed)
        # Compile the AST into a code object
        compiled = compile(self.parsed, filename="<user_script>", mode="eval")
        # Execute with no globals and safe locals
        return eval(compiled, {"__builtins__": {}}, SAFE_FUNCTIONS)

def execute_user_code(script_code: str) -> str:
    """
    Execute a user-supplied Python script string safely.

    Parameters
    ----------
    script_code : str
        The user-supplied code to evaluate.

    Returns
    -------
    str
        Result of the evaluation as a string, or 'Execution Blocked!'
        if the code is unsafe.
    """
    try:
        evaluator = SafeEvaluator(script_code)
        result = evaluator.eval()
        return str(result)
    except Exception:
        # Any exception (including ValueError, SyntaxError, etc.) leads to blocking
        return "Execution Blocked!"