import ast
from types import FunctionType

def execute_code_snippet(code_snippet: str):
    """
    Execute a small Python code snippet in a restricted environment.
    
    Parameters
    ----------
    code_snippet : str
        The Python code to execute.  Must not contain disallowed constructs.
    
    Returns
    -------
    Any
        The value of the last expression in the snippet, or None if there is no
        expression.
    
    Raises
    ------
    ValueError
        If the snippet contains disallowed operations or unsafe code.
    """
    
    # ---------- 1. Syntax checking and AST validation ----------
    try:
        tree = ast.parse(code_snippet, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code snippet: {exc}") from None
    
    # Allowed node types
    ALLOWED_NODES = (
        ast.Module, ast.Expr, ast.Load,
        ast.Str, ast.Bytes, ast.Num, ast.Constant,  # literals
        ast.BinOp, ast.UnaryOp, ast.BoolOp,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
        ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
        ast.FloorDiv, ast.Invert, ast.Not, ast.UAdd, ast.USub,
        ast.Compare, ast.Eq, ast.NotEq, ast.Lt, ast.LtE,
        ast.Gt, ast.GtE, ast.Is, ast.IsNot, ast.In, ast.NotIn,
        ast.Call,
        ast.Name, ast.Attribute,  # for builtins and module attributes
        ast.Tuple, ast.List, ast.Dict, ast.Set,
        ast.NameConstant,  # True, False, None
        ast.keyword,
    )
    
    # Allowed built‑in functions / attributes
    SAFE_BUILTINS = {
        'print': print,
        'len': len,
        'range': range,
        'abs': abs,
        'min': min,
        'max': max,
        'sum': sum,
        'sorted': sorted,
        'list': list,
        'tuple': tuple,
        'dict': dict,
        'set': set,
    }
    
    # Helper to walk the AST
    def _check_node(node):
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(f"Disallowed construct: {type(node).__name__}")
        for child in ast.iter_child_nodes(node):
            _check_node(child)
    
    _check_node(tree)
    
    # ---------- 2. Restrict names ----------
    # Allow only safe builtins and no other globals
    restricted_globals = {"__builtins__": SAFE_BUILTINS}
    
    # Capture the value of the last expression if present
    local_vars = {}
    
    try:
        exec(compile(tree, filename="<snippet>", mode="exec"),
             restricted_globals,
             local_vars)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    
    # If the last statement was an expression, its value is in local_vars['_']
    # We can retrieve it by inspecting the AST
    last_expr_value = None
    for node in reversed(tree.body):
        if isinstance(node, ast.Expr):
            # Evaluate the expression in the same environment
            last_expr_value = eval(compile(ast.Expression(node.value),
                                            filename="<expr>",
                                            mode="eval"),
                                    restricted_globals,
                                    local_vars)
            break
    
    return last_expr_value