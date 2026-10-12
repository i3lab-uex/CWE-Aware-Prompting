import ast

class _SafeEvaluator(ast.NodeVisitor):
    """
    AST visitor that ensures the code contains only safe constructs.
    Allowed nodes:
        - Module, Expr, Expression
        - literals: Constant (str/int/float/complex/bool/None)
        - BinOp, UnaryOp, BoolOp, Compare
        - operators: +,-,*,/,//,%,**,&,^,|,<<,>>,>,<,>=,<=,==,!=,is,is not,in,not in
        - parentheses are implicit via the AST structure
    Any other node results in a ValueError.
    """
    _allowed_ops = (
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod,
        ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
        ast.UAdd, ast.USub, ast.Not, ast.Invert,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
        ast.Is, ast.IsNot, ast.In, ast.NotIn
    )
    _allowed_bool_ops = (ast.And, ast.Or)

    def visit(self, node):
        if isinstance(node, (ast.Module, ast.Expr, ast.Expression)):
            return super().visit(node)
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (str, int, float, complex, bool)) or node.value is None:
                return
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")
        elif isinstance(node, ast.BinOp):
            if not isinstance(node.op, self._allowed_ops):
                raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")
            self.visit(node.left)
            self.visit(node.right)
        elif isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, self._allowed_ops):
                raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
            self.visit(node.operand)
        elif isinstance(node, ast.BoolOp):
            if not isinstance(node.op, self._allowed_bool_ops):
                raise ValueError(f"Disallowed boolean operator: {type(node.op).__name__}")
            for v in node.values:
                self.visit(v)
        elif isinstance(node, ast.Compare):
            if any(not isinstance(op, self._allowed_ops) for op in node.ops):
                raise ValueError("Disallowed comparison operator")
            self.visit(node.left)
            for comp in node.comparators:
                self.visit(comp)
        else:
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

def safe_run_script(code: str):
    """
    Execute a user-provided Python script safely.

    Parameters
    ----------
    code : str
        The user's Python code to execute. Only simple expressions and arithmetic are allowed.

    Returns
    -------
    Any
        The result of evaluating the last expression in the code, or None if nothing is returned.

    Raises
    ------
    ValueError
        If the code contains disallowed constructs or has syntax errors.
    """
    try:
        parsed = ast.parse(code, mode='eval')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}") from None

    # Validate AST
    validator = _SafeEvaluator()
    validator.visit(parsed)

    # Evaluate safely with no globals/locals
    try:
        result = eval(compile(parsed, filename="<safe>", mode="eval"), {}, {})
    except Exception as e:
        raise ValueError(f"Execution error: {e}") from None

    return result