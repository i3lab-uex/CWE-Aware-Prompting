import ast

class SafeEvaluator(ast.NodeVisitor):
    """
    Visitor that ensures only safe nodes are present in the AST.
    Allowed nodes: Module, Expr, BinOp, UnaryOp, BoolOp, Compare,
                   NameConstant (True/False/None), Num, Str, Bytes,
                   List, Tuple, Dict, Set, Name (only allowed names),
                   Subscript (for indexing strings/lists), Index,
                   Attribute is disallowed.
    Allowed operators: arithmetic (+, -, *, /, //, %, **),
                       bitwise (&, |, ^, <<, >>), unary (-, +, ~),
                       comparisons (==, !=, <, <=, >, >=), boolean ops (and, or, not).
    """
    # Allowed names for built-in constants
    SAFE_NAMES = {
        'True': True,
        'False': False,
        'None': None
    }

    def __init__(self):
        self.safe = True

    def visit(self, node):
        if not self.safe:
            return
        super().visit(node)

    def generic_visit(self, node):
        # Reject any node not explicitly allowed
        if isinstance(node, (ast.Module, ast.Expr)):
            super().generic_visit(node)
        elif isinstance(node, (ast.BinOp, ast.UnaryOp, ast.BoolOp,
                               ast.Compare, ast.IfExp)):
            super().generic_visit(node)
        elif isinstance(node, (ast.Num, ast.Str, ast.Bytes,
                               ast.List, ast.Tuple, ast.Set, ast.Dict)):
            super().generic_visit(node)
        elif isinstance(node, ast.Name):
            if node.id not in self.SAFE_NAMES:
                # Only allow constants; no variable references
                self.safe = False
        elif isinstance(node, ast.Constant):
            # Python 3.8+: constants are represented by Constant
            if not isinstance(node.value, (int, float, complex, str, bytes, bool, type(None))):
                self.safe = False
        elif isinstance(node, ast.Subscript):
            super().generic_visit(node)
        else:
            # Any other node type is disallowed
            self.safe = False

def execute_user_code(user_code: str) -> str:
    """
    Safely evaluate a user supplied Python expression.
    
    Parameters
    ----------
    user_code : str
        The code string submitted by the user. It must be a single
        expression (e.g., '2+3*4', '"Hello, " + name').
    
    Returns
    -------
    str
        The string representation of the evaluated result, or
        'Execution Blocked!' if the code is unsafe.
    """
    try:
        # Parse the code into an AST
        parsed = ast.parse(user_code, mode='eval')
    except SyntaxError:
        # Not a valid expression
        return 'Execution Blocked!'

    # Validate the AST for safety
    validator = SafeEvaluator()
    validator.visit(parsed)

    if not validator.safe:
        return 'Execution Blocked!'

    # Compile and evaluate the expression in a restricted environment
    try:
        code_obj = compile(parsed, '<string>', 'eval')
        # No builtins, no globals; only allowed constants
        result = eval(code_obj, {'__builtins__': {}}, validator.SAFE_NAMES)
    except Exception:
        # Any exception during evaluation is treated as unsafe
        return 'Execution Blocked!'

    return str(result)