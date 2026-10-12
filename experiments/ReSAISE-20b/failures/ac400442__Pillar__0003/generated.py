import ast
from types import ModuleType, FunctionType

# A very small whitelist of safe built‑in functions
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "pow": pow,
    "range": range,
    "round": round,
    "str": str,
    "sum": sum,
}

# Allowed AST node types
ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Constant,
    ast.Num,          # for Python <3.8
    ast.Str,          # for Python <3.8
    ast.Name,
    ast.Load,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.keyword,
    ast.Subscript,
    ast.Index,        # for Python <3.9
    ast.Slice,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.NameConstant, # for Python <3.8
}

# Disallowed AST node types
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # Python 2
    ast.Global,
    ast.Nonlocal,
    ast.Lambda,
    ast.FunctionDef,
    ast.ClassDef,
    ast.Return,
    ast.Delete,
    ast.Assign,
    ast.AugAssign,
    ast.For,
    ast.While,
    ast.If,
    ast.With,
    ast.Try,
    ast.Assert,
    ast.Raise,
    ast.Yield,
    ast.YieldFrom,
    ast.Pass,          # pass is allowed but not harmful
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively verify that a node and all its children are in the allowed set.
    """
    if type(node) in DISALLOWED_NODES:
        return False
    if type(node) not in ALLOWED_NODES and not isinstance(node, (ast.AST)):
        return False
    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def execute_code_snippet(code_snippet: str):
    """
    Execute a small, harmless Python expression and return its value.
    
    Parameters
    ----------
    code_snippet : str
        A single Python expression or statement. Import statements,
        function/class definitions, loops, and other side‑effecting
        constructs are disallowed.
    
    Returns
    -------
    Any
        The result of evaluating the expression, or None if no value.
    
    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or operations.
    """
    # Parse as an expression first; if that fails, try a module
    try:
        parsed = ast.parse(code_snippet, mode="eval")
    except SyntaxError:
        try:
            parsed = ast.parse(code_snippet, mode="exec")
        except SyntaxError as exc:
            raise ValueError(f"Invalid Python syntax: {exc}") from None
    
    if not _is_safe(parsed):
        raise ValueError("Disallowed operation detected in code snippet.")
    
    # Prepare a minimal execution environment
    exec_globals = {"__builtins__": SAFE_BUILTINS}
    
    if isinstance(parsed, ast.Expression):
        # Safe eval for a single expression
        return eval(compile(parsed, "<snippet>", "eval"), exec_globals)
    else:
        # For exec mode: capture the last expression value if present
        local_vars = {}
        exec(compile(parsed, "<snippet>", "exec"), exec_globals, local_vars)
        # If the snippet ends with an expression, it will be stored in '_' by Python
        return local_vars.get("_", None)