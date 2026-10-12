import ast

def evaluate_user_code(code_str: str) -> str:
    """
    Safely evaluates a user-supplied Python expression that contains only
    basic arithmetic and string operations. If the code is not safe,
    returns 'Execution Blocked!'.

    Supported constructs:
        - Literals: int, float, str
        - Binary operations: +, -, *, /, //, %, **
        - Unary operations: +, -
        - Parentheses for grouping
    """

    # List of AST node types that are considered safe
    SAFE_NODES = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,          # Python <3.8
        ast.Constant,     # Python >=3.8
        ast.Str,          # for backward compatibility
        ast.NameConstant,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow,
        ast.UAdd, ast.USub,
        ast.LParen,  # not an actual node; parentheses are handled by Expr structure
    }

    # Parse the code into an AST
    try:
        parsed = ast.parse(code_str, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Visitor to ensure only allowed nodes appear
    class SafeVisitor(ast.NodeVisitor):
        def generic_visit(self, node):
            if type(node) not in SAFE_NODES:
                raise ValueError(f"Disallowed node: {type(node).__name__}")
            super().generic_visit(node)

    try:
        SafeVisitor().visit(parsed)
    except Exception:
        return 'Execution Blocked!'

    # Evaluate the expression in a minimal environment
    try:
        result = eval(compile(parsed, filename='<user_code>', mode='eval'), {"__builtins__": None}, {})
    except Exception:
        return 'Execution Blocked!'

    return str(result)