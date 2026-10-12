import ast
from typing import Any, Optional

# A minimal set of built‑ins that are considered safe for user scripts
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'dict': dict,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'print': print,          # harmless
    'range': range,
    'str': str,
    'sum': sum,
    'tuple': tuple,
}

# AST nodes that are allowed in the user script
ALLOWED_NODES = {
    # Expressions
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Constant,
    ast.Name,
    ast.Load,
    # Operations
    ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod,
    ast.Pow,
    ast.USub, ast.UAdd,
    ast.And, ast.Or,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Containers
    ast.List, ast.Tuple, ast.Dict, ast.Set,
    ast.ListComp, ast.GeneratorExp,
    # Control flow
    ast.IfExp,
    # Function calls (only to allowed builtins)
    ast.Call,
    ast.keyword,
}

# Disallowed nodes
DISALLOWED_NODES = {
    ast.Import, ast.ImportFrom,
    ast.Exec,  # Python 2 only
    ast.Global,
    ast.Nonlocal,
    ast.Lambda,  # disallow lambda for simplicity
    ast.FunctionDef,
    ast.ClassDef,
    ast.With, ast.AsyncWith,
    ast.Try, ast.ExceptHandler,
    ast.For, ast.While,
    ast.Delete,
    ast.AugAssign,
    ast.Assign,
    ast.Raise,
    ast.Yield, ast.YieldFrom,
    ast.Return,
}

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check that all nodes in the AST are allowed.
    Raise ValueError if a disallowed node is encountered.
    """
    if type(node) in DISALLOWED_NODES:
        raise ValueError(f"Disallowed construct: {type(node).__name__}")
    if type(node) not in ALLOWED_NODES:
        raise ValueError(f"Unsupported syntax: {type(node).__name__}")

    for child in ast.iter_child_nodes(node):
        _is_safe_node(child)

def _evaluate_last_expr(tree: ast.Module, globals_dict: dict) -> Optional[Any]:
    """
    Execute the AST in a restricted environment and return
    the value of the last expression if present.
    """
    # Compile the tree into a code object
    code_obj = compile(tree, filename="<user_script>", mode="exec")
    # Execute the compiled code
    exec(code_obj, globals_dict, {})
    # If the last node is an expression, return its value
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        expr_node = tree.body[-1].value
        # Evaluate the expression node in the same environment
        return eval(compile(ast.Expression(expr_node), filename="<expr>", mode="eval"),
                    globals_dict, {})
    return None

def execute_python_script(python_code: str) -> Optional[Any]:
    """
    Execute a user supplied Python script in a safe sandbox.
    
    Parameters
    ----------
    python_code : str
        The Python source code to run.

    Returns
    -------
    Any or None
        Result of the last expression in the script, or None if none.

    Raises
    ------
    ValueError
        If the code contains prohibited operations or syntax errors.
    """
    try:
        # Parse into an AST
        tree = ast.parse(python_code, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from e

    # Validate the AST
    _is_safe_node(tree)

    # Restricted globals: only safe builtins, no modules or file I/O
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}

    # Execute and return result
    return _evaluate_last_expr(tree, sandbox_globals)