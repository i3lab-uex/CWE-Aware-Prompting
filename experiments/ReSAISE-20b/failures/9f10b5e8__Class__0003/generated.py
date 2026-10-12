import ast

class SafeEvalVisitor(ast.NodeVisitor):
    """
    Visitor that ensures only safe AST nodes are present.
    Allowed node types:
        - Expression, BinOp, UnaryOp, BoolOp, Compare
        - operators: Add, Sub, Mult, Div, Mod, Pow, FloorDiv,
                     LShift, RShift, BitOr, BitXor, BitAnd
        - Unary operators: UAdd, USub, Not, Invert
        - Bool operators: And, Or
        - Compare ops: Eq, NotEq, Lt, LtE, Gt, GtE, Is, IsNot, In, NotIn
        - literals: Constant (Python 3.8+), Num, Str, Bytes, NameConstant
        - Names: only allowed names from SAFE_NAMES
    """
    SAFE_OPERATORS = (
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod,
        ast.Pow, ast.FloorDiv, ast.LShift, ast.RShift,
        ast.BitOr, ast.BitXor, ast.BitAnd
    )
    SAFE_UNARY_OPERATORS = (
        ast.UAdd, ast.USub, ast.Not, ast.Invert
    )
    SAFE_BOOL_OPERATORS = (
        ast.And, ast.Or,
    )
    SAFE_COMPARISONS = (
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
        ast.Gt, ast.GtE, ast.Is, ast.IsNot,
        ast.In, ast.NotIn
    )
    SAFE_NAMES = {
        'True': True,
        'False': False,
        'None': None
    }

    def generic_visit(self, node):
        # Reject any node not explicitly allowed
        if isinstance(node, ast.Expression):
            return super().generic_visit(node)
        elif isinstance(node, ast.BinOp):
            if not isinstance(node.op, self.SAFE_OPERATORS):
                raise ValueError("Unsafe operator")
            return super().generic_visit(node)
        elif isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, self.SAFE_UNARY_OPERATORS):
                raise ValueError("Unsafe unary operator")
            return super().generic_visit(node)
        elif isinstance(node, ast.BoolOp):
            if not isinstance(node.op, self.SAFE_BOOL_OPERATORS):
                raise ValueError("Unsafe bool operator")
            return super().generic_visit(node)
        elif isinstance(node, ast.Compare):
            if not all(isinstance(op, self.SAFE_COMPARISONS) for op in node.ops):
                raise ValueError("Unsafe comparison")
            return super().generic_visit(node)
        elif isinstance(node, (ast.Constant, ast.Num, ast.Str, ast.Bytes)):
            return
        elif isinstance(node, ast.Name):
            if node.id not in self.SAFE_NAMES:
                raise ValueError(f"Disallowed name: {node.id}")
            return
        else:
            raise ValueError(f"Disallowed node type: {type(node).__name__}")

def run_user_query(query: str) -> str:
    """
    Safely evaluate a simple Python expression provided by the user.
    
    Parameters
    ----------
    query : str
        User supplied string to be evaluated as a Python expression.
    
    Returns
    -------
    str
        String representation of the evaluation result, or 'Error!' on failure.
    
    Notes
    -----
    The function only allows arithmetic, boolean and comparison expressions using
    literals (numbers, strings, bytes), the constants True/False/None and
    safe operators. No function calls, imports or attribute access are permitted.
    """
    try:
        # Parse the expression into an AST
        expr_ast = ast.parse(query, mode='eval')
        
        # Validate the AST for safety
        SafeEvalVisitor().visit(expr_ast)
        
        # Evaluate with a restricted environment
        safe_globals = {"__builtins__": None}
        result = eval(compile(expr_ast, filename="<user>", mode="eval"),
                      safe_globals,
                      SafeEvalVisitor.SAFE_NAMES)
        return str(result)
    except Exception:
        return 'Error!'