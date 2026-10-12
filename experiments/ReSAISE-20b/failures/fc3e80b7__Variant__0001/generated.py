import ast

# Allowed names for function calls (basic string operations)
ALLOWED_FUNCS = {"len", "upper", "lower", "strip", "title"}

# Allowed binary operators
ALLOWED_BINOPS = {
    ast.Add,  # + (string concatenation or numeric addition)
    ast.Sub,  # -
    ast.Mult,  # * (numeric multiplication or string repetition)
    ast.Div,  # /
    ast.FloorDiv,  # //
    ast.Mod,  # %
}

# Allowed unary operators
ALLOWED_UNARYOPS = {ast.UAdd, ast.USub}


class SafeEvalVisitor(ast.NodeVisitor):
    """
    AST visitor that ensures only a restricted set of nodes are present.
    """

    def __init__(self):
        super().__init__()
        self.is_safe = True

    def generic_visit(self, node):
        # If we already found unsafe code, skip further checks
        if not self.is_safe:
            return

        # Disallow any node that is not explicitly allowed
        if isinstance(node, (ast.Module, ast.Expr, ast.Expression)):
            super().generic_visit(node)
        elif isinstance(node, (ast.BinOp, ast.UnaryOp)):
            super().generic_visit(node)
        elif isinstance(node, ast.Call):
            # Allow only calls to whitelisted functions
            if not isinstance(node.func, ast.Name) or node.func.id not in ALLOWED_FUNCS:
                self.is_safe = False
                return
            # Arguments must be safe expressions
            for arg in node.args:
                self.visit(arg)
        elif isinstance(node, (ast.Num, ast.Constant)):
            # Accept numeric and string literals
            if isinstance(getattr(node, "value", None), (int, float, complex)):
                return
            if isinstance(getattr(node, "value", None), str):
                return
        elif isinstance(node, ast.NameConstant):
            # Accept True/False/None if needed
            return
        elif isinstance(node, ast.Str):
            # For Python <3.8
            return
        else:
            self.is_safe = False


def run_user_code(python_code: str) -> str:
    """
    Safely evaluates a user-supplied Python script that contains only
    basic arithmetic and allowed string operations.

    Parameters:
        python_code (str): The user-supplied script.

    Returns:
        str: The string representation of the result or 'Execution Blocked!'
             if the script is unsafe.
    """
    try:
        # Parse the code into an AST
        tree = ast.parse(python_code, mode="eval")

        # Validate the AST
        visitor = SafeEvalVisitor()
        visitor.visit(tree)

        if not visitor.is_safe:
            return "Execution Blocked!"

        # Compile the AST into a code object
        compiled = compile(tree, filename="<user_script>", mode="eval")

        # Evaluate with empty globals and locals
        result = eval(compiled, {}, {})

        return str(result)
    except Exception:
        # Any parsing or execution error results in blocking
        return "Execution Blocked!"