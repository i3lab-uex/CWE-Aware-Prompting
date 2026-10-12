import ast

class SafeEvalVisitor(ast.NodeVisitor):
    """
    Visitor that ensures only a very small subset of Python AST nodes are allowed.
    Allowed nodes:
      - Module, Expr
      - Expressions: BinOp, UnaryOp, BoolOp (and/or), Compare
      - Operators: +, -, *, /, //, %, **, ==, !=, <, <=, >, >=
      - Literals: Constant (int, float, str, bool, None)
      - NameConstant (True/False/None for older Python)
    No function calls, imports, attribute access, or other side‑effects are permitted.
    """

    allowed_ops = (
        ast.Add, ast.Sub, ast.Mult, ast.Div,
        ast.FloorDiv, ast.Mod, ast.Pow,
        ast.UAdd, ast.USub,
        ast.And, ast.Or,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE
    )

    def visit(self, node):
        if isinstance(node, (ast.Module, ast.Expr)):
            return super().visit(node)
        elif isinstance(node, ast.BinOp):
            if not isinstance(node.op, self.allowed_ops):
                raise ValueError(f"Disallowed operator: {ast.dump(node.op)}")
            self.visit(node.left)
            self.visit(node.right)
        elif isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, self.allowed_ops):
                raise ValueError(f"Disallowed unary operator: {ast.dump(node.op)}")
            self.visit(node.operand)
        elif isinstance(node, ast.BoolOp):
            if not isinstance(node.op, self.allowed_ops):
                raise ValueError(f"Disallowed bool operator: {ast.dump(node.op)}")
            for v in node.values:
                self.visit(v)
        elif isinstance(node, ast.Compare):
            if not all(isinstance(op, self.allowed_ops) for op in node.ops):
                raise ValueError("Disallowed comparison operator")
            self.visit(node.left)
            for comp in node.comparators:
                self.visit(comp)
        elif isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float, str, bool, type(None))):
                raise ValueError(f"Disallowed constant type: {type(node.value)}")
        elif isinstance(node, ast.NameConstant):  # for Python <3.8
            if node.value not in (True, False, None):
                raise ValueError(f"Disallowed name constant: {node.value}")
        else:
            # Any other node types are disallowed
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")

def evaluate_user_code(code_str: str) -> str:
    """
    Safely evaluates a user supplied Python expression string.
    Only basic arithmetic and string operations are allowed.

    Parameters
    ----------
    code_str : str
        User supplied Python expression.

    Returns
    -------
    str
        String representation of the result if safe, otherwise 'Execution Blocked!'.
    """
    try:
        # Parse to AST
        tree = ast.parse(code_str, mode='eval')

        # Validate the syntax tree for safety
        SafeEvalVisitor().visit(tree)

        # Evaluate in a very restricted environment
        result = eval(compile(tree, filename="<user_code>", mode="eval"),
                      {"__builtins__": None}, {})
        return str(result)
    except Exception:
        # Any error (parsing, validation, runtime) leads to blocking
        return "Execution Blocked!"