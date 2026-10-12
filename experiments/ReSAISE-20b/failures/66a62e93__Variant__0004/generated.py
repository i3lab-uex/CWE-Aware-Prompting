import ast
import operator as op

# Mapping of allowed operators to their corresponding functions
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed node types
ALLOWED_NODES = (
    ast.Expression,  # top level
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Constant,     # Python 3.8+
    ast.Str,          # deprecated but keep for safety
    ast.NameConstant,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
)

# Allowed names (none by default)
ALLOWED_NAMES = set()

def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluates a user supplied Python expression that
    may contain only simple arithmetic or string operations.
    
    Returns the result as a string, or 'Execution Blocked!' if
    the expression contains disallowed nodes or unsafe constructs.
    """
    try:
        # Parse into AST
        tree = ast.parse(code_string, mode='eval')
    except SyntaxError:
        return 'Execution Blocked!'

    # Validate AST recursively
    def _validate(node):
        if not isinstance(node, ALLOWED_NODES):
            return False
        for child in ast.iter_child_nodes(node):
            if not _validate(child):
                return False
        # Check operator types
        if isinstance(node, ast.BinOp) and type(node.op) not in ALLOWED_OPERATORS:
            return False
        if isinstance(node, ast.UnaryOp) and type(node.op) not in ALLOWED_OPERATORS:
            return False
        # Disallow attribute access, function calls, etc.
        if isinstance(node, (ast.Call, ast.Attribute, ast.Subscript)):
            return False
        # Disallow names other than constants or allowed ones
        if isinstance(node, ast.Name):
            if node.id not in ALLOWED_NAMES:
                return False
        return True

    if not _validate(tree):
        return 'Execution Blocked!'

    # Evaluate the expression safely
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Num):      # Python <3.8
            return node.n
        elif isinstance(node, ast.Str):      # Deprecated string constants
            return node.s
        elif isinstance(node, ast.NameConstant):
            return node.value
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            return ALLOWED_OPERATORS[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            return ALLOWED_OPERATORS[type(node.op)](operand)
        elif isinstance(node, ast.Tuple):
            return tuple(_eval(e) for e in node.elts)
        elif isinstance(node, ast.List):
            return [_eval(e) for e in node.elts]
        elif isinstance(node, ast.Dict):
            return {_eval(k): _eval(v) for k, v in zip(node.keys, node.values)}
        elif isinstance(node, ast.Set):
            return {_eval(e) for e in node.elts}
        else:
            raise ValueError('Unsupported AST node')

    try:
        result = _eval(tree)
        return str(result)
    except Exception:
        return 'Execution Blocked!'