import ast

def evaluate_user_math(math_expr: str) -> str:
    """
    Safely evaluates a simple arithmetic or logical expression supplied by the user.
    
    Parameters
    ----------
    math_expr : str
        The user-supplied expression to evaluate.
    
    Returns
    -------
    str
        The string representation of the result, or 'Processing Failed!' if the expression is invalid,
        contains unsafe elements, or an error occurs during evaluation.
    """
    
    # Define the set of allowed AST node types
    ALLOWED_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,          # Not allowed but included for explicit rejection
        ast.Name,
        ast.Load,
        ast.Constant,      # For Python 3.8+: numbers, strings, booleans
        ast.Num,
        ast.Str,
        ast.Bytes,
        ast.NameConstant,  # For Python <3.8: True/False/None
    }
    
    # Allowed operators and comparators
    ALLOWED_OPERATORS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
        ast.BitXor, ast.BitAnd
    }
    
    ALLOWED_UNARY_OPERATORS = {
        ast.UAdd, ast.USub, ast.Not
    }
    
    ALLOWED_BOOL_OPERATORS = {
        ast.And, ast.Or
    }
    
    ALLOWED_COMPARATORS = {
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
        ast.Gt, ast.GtE
    }
    
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        
        elif isinstance(node, ast.Constant):  # Python >=3.8
            return node.value
        
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        
        elif isinstance(node, ast.Str):
            return node.s
        
        elif isinstance(node, ast.Bytes):
            return node.s
        
        elif isinstance(node, ast.NameConstant):  # True/False/None
            return node.value
        
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in ALLOWED_OPERATORS:
                raise ValueError("Disallowed operator")
            left = _eval(node.left)
            right = _eval(node.right)
            return _apply_operator(node.op, left, right)
        
        elif isinstance(node, ast.UnaryOp):
            if type(node.op) not in ALLOWED_UNARY_OPERATORS:
                raise ValueError("Disallowed unary operator")
            operand = _eval(node.operand)
            return _apply_unary_operator(node.op, operand)
        
        elif isinstance(node, ast.BoolOp):
            if type(node.op) not in ALLOWED_BOOL_OPERATORS:
                raise ValueError("Disallowed boolean operator")
            values = [_eval(v) for v in node.values]
            return _apply_bool_operator(node.op, values)
        
        elif isinstance(node, ast.Compare):
            if any(type(comp) not in ALLOWED_COMPARATORS for comp in node.ops):
                raise ValueError("Disallowed comparison operator")
            left = _eval(node.left)
            for op, comparator in zip(node.ops, node.comparators):
                right = _eval(comparator)
                if not _apply_comparison(op, left, right):
                    return False
                left = right  # For chained comparisons
            return True
        
        else:
            raise ValueError(f"Disallowed AST node: {type(node).__name__}")
    
    def _apply_operator(op, left, right):
        if isinstance(op, ast.Add): return left + right
        if isinstance(op, ast.Sub): return left - right
        if isinstance(op, ast.Mult): return left * right
        if isinstance(op, ast.Div): return left / right
        if isinstance(op, ast.FloorDiv): return left // right
        if isinstance(op, ast.Mod): return left % right
        if isinstance(op, ast.Pow): return left ** right
        if isinstance(op, ast.LShift): return left << right
        if isinstance(op, ast.RShift): return left >> right
        if isinstance(op, ast.BitOr): return left | right
        if isinstance(op, ast.BitXor): return left ^ right
        if isinstance(op, ast.BitAnd): return left & right
        raise ValueError("Unsupported binary operator")
    
    def _apply_unary_operator(op, operand):
        if isinstance(op, ast.UAdd): return +operand
        if isinstance(op, ast.USub): return -operand
        if isinstance(op, ast.Not):  return not operand
        raise ValueError("Unsupported unary operator")
    
    def _apply_bool_operator(op, values):
        if isinstance(op, ast.And):
            result = True
            for v in values:
                result = result and v
                if not result:
                    break
            return result
        if isinstance(op, ast.Or):
            result = False
            for v in values:
                result = result or v
                if result:
                    break
            return result
        raise ValueError("Unsupported boolean operator")
    
    def _apply_comparison(op, left, right):
        if isinstance(op, ast.Eq):  return left == right
        if isinstance(op, ast.NotEq):return left != right
        if isinstance(op, ast.Lt):   return left < right
        if isinstance(op, ast.LtE):  return left <= right
        if isinstance(op, ast.Gt):   return left > right
        if isinstance(op, ast.GtE):  return left >= right
        raise ValueError("Unsupported comparison operator")
    
    try:
        if not isinstance(math_expr, str) or math_expr.strip() == '':
            return 'Processing Failed!'
        
        # Parse the expression into an AST
        parsed = ast.parse(math_expr, mode='eval')
        
        # Ensure all nodes are allowed
        for node in ast.walk(parsed):
            if not isinstance(node, tuple(ALLOWED_NODES)):
                return 'Processing Failed!'
        
        result = _eval(parsed)
        return str(result)
    
    except Exception:
        # Any error leads to failure
        return 'Processing Failed!'