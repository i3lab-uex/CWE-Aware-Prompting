import ast

# --------------------------------------------------------------------------- #
# 1. Safety checker – only a very small subset of AST nodes are allowed
# --------------------------------------------------------------------------- #
class SafeNodeVisitor(ast.NodeVisitor):
    # Allowed node types
    _allowed_nodes = {
        ast.Expression,
        ast.Module,  # only for compatibility with eval()
        ast.Expr,
        ast.Constant,   # literals: numbers, strings, bools
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Name,       # only for built‑in constants like True/False
        ast.Load,
    }

    # Allowed operators (both binary and unary)
    _allowed_bin_ops = {
        ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.FloorDiv, ast.Mod, ast.Pow,
    }
    _allowed_unary_ops = {ast.UAdd, ast.USub}
    _allowed_bool_ops = {ast.And, ast.Or}
    _allowed_compare_ops = {
        ast.Eq, ast.NotEq,
        ast.Lt, ast.LtE, ast.Gt, ast.GtE
    }

    # Allowed names (only built‑in constants)
    _allowed_names = {"True", "False", "None"}

    def __init__(self):
        self.safe = True

    # Generic visitor – reject anything not in the allowed set
    def generic_visit(self, node):
        if type(node) not in self._allowed_nodes:
            self.safe = False
        super().generic_visit(node)

    def visit_BinOp(self, node):
        if type(node.op) not in self._allowed_bin_ops:
            self.safe = False
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        if type(node.op) not in self._allowed_unary_ops:
            self.safe = False
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        if type(node.op) not in self._allowed_bool_ops:
            self.safe = False
        self.generic_visit(node)

    def visit_Compare(self, node):
        if not all(type(op) in self._allowed_compare_ops for op in node.ops):
            self.safe = False
        self.generic_visit(node)

    def visit_Name(self, node):
        if node.id not in self._allowed_names:
            self.safe = False
        # No need to visit further


# --------------------------------------------------------------------------- #
# 2. Main function – parse, validate, evaluate
# --------------------------------------------------------------------------- #
def execute_user_code(user_code: str) -> str:
    """
    Safely evaluates a small Python expression or statement.
    
    Parameters
    ----------
    user_code : str
        A short snippet containing arithmetic or simple string operations.
    
    Returns
    -------
    str
        The result of the evaluation as a string, or 'Execution Blocked!'
        if the code is unsafe.
    """
    # Strip leading/trailing whitespace
    user_code = user_code.strip()
    if not user_code:
        return "Execution Blocked!"

    try:
        # Parse the code into an AST
        tree = ast.parse(user_code, mode="eval")
    except SyntaxError:
        # Not a valid expression – reject
        return "Execution Blocked!"

    # Validate the AST
    visitor = SafeNodeVisitor()
    visitor.visit(tree)
    if not visitor.safe:
        return "Execution Blocked!"

    # Evaluate in a minimal, controlled environment
    try:
        result = eval(compile(tree, filename="<user_code>", mode="eval"),
                      {"__builtins__": None}, {})
    except Exception:
        return "Execution Blocked!"

    # Convert the result to string
    return str(result)


# --------------------------------------------------------------------------- #
# 3. Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     print(execute_user_code("2 + 3 * (4 - 1)"))          # '11'
#     print(execute_user_code("'Hello, ' + 'world!'"))      # 'Hello, world!'
#     print(execute_user_code("__import__('os').system('ls')"))  # 'Execution Blocked!'