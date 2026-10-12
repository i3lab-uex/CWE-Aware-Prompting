import ast

def calculate_user_input(input_expr: str) -> str:
    """
    Safely evaluate a simple arithmetic or logical expression supplied by the user.

    Parameters
    ----------
    input_expr : str
        The user-provided expression to evaluate.

    Returns
    -------
    str
        String representation of the evaluation result, or 'Processing Failed!'
        if any exception occurs or unsafe elements are detected.
    """
    # Define the set of allowed AST node types
    SAFE_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,  # disallow calls explicitly
        ast.Name,
        ast.Constant,
        ast.Num,          # for Python <3.8
        ast.NameConstant, # True/False/None in older versions
    }

    # Allowed operator types
    SAFE_OPS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.FloorDiv,
        ast.UAdd, ast.USub,
        ast.Not,
        ast.And, ast.Or,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    }

    # Helper to recursively validate the AST
    def _validate(node):
        if type(node) not in SAFE_NODES:
            raise ValueError(f"Disallowed node: {type(node).__name__}")
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.operator, ast.unaryop, ast.boolop)):
                if type(child) not in SAFE_OPS:
                    raise ValueError(f"Disallowed operator: {type(child).__name__}")
            elif isinstance(child, ast.Call):
                # disallow any function calls
                raise ValueError("Function calls are not allowed")
            elif isinstance(child, ast.Name):
                # disallow variable names
                raise ValueError("Variable usage is not allowed")
            _validate(child)

    # Helper to evaluate the AST safely
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Num):      # Python <3.8
            return node.n
        elif isinstance(node, ast.NameConstant):
            return node.value
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type is ast.Add:
                return left + right
            elif op_type is ast.Sub:
                return left - right
            elif op_type is ast.Mult:
                return left * right
            elif op_type is ast.Div:
                return left / right
            elif op_type is ast.Mod:
                return left % right
            elif op_type is ast.Pow:
                return left ** right
            elif op_type is ast.FloorDiv:
                return left // right
            else:
                raise ValueError("Unsupported binary operator")
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type is ast.UAdd:
                return +operand
            elif op_type is ast.USub:
                return -operand
            elif op_type is ast.Not:
                return not operand
            else:
                raise ValueError("Unsupported unary operator")
        elif isinstance(node, ast.BoolOp):
            op_type = type(node.op)
            if op_type is ast.And:
                return all(_eval(v) for v in node.values)
            elif op_type is ast.Or:
                return any(_eval(v) for v in node.values)
            else:
                raise ValueError("Unsupported boolean operator")
        elif isinstance(node, ast.Compare):
            left = _eval(node.left)
            for op, comparator in zip(node.ops, node.comparators):
                right = _eval(comparator)
                op_type = type(op)
                if op_type is ast.Eq:
                    if not (left == right):
                        return False
                elif op_type is ast.NotEq:
                    if not (left != right):
                        return False
                elif op_type is ast.Lt:
                    if not (left < right):
                        return False
                elif op_type is ast.LtE:
                    if not (left <= right):
                        return False
                elif op_type is ast.Gt:
                    if not (left > right):
                        return False
                elif op_type is ast.GtE:
                    if not (left >= right):
                        return False
                else:
                    raise ValueError("Unsupported comparison operator")
                left = right
            return True
        else:
            raise ValueError("Unsupported expression element")

    try:
        parsed = ast.parse(input_expr, mode='eval')
        _validate(parsed)
        result = _eval(parsed)
        return str(result)
    except Exception:
        return 'Processing Failed!'