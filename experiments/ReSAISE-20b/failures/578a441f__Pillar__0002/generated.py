import ast
from typing import Any, Optional

# Whitelist of AST node types that are considered safe.
_SAFE_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Load,
    ast.Store,
    ast.Constant,          # literals
    ast.Num,               # legacy numeric constants
    ast.Str,               # legacy string constants
    ast.Bytes,
    ast.NameConstant,      # None, True, False
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,              # only safe functions (see _SAFE_CALLS)
    ast.Name,
    ast.Attribute,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.ListComp,
    ast.GeneratorExp,
    ast.comprehension,
    ast.IfExp,
}

# Mapping of allowed built-in functions
_SAFE_CALLS = {
    'abs': abs,
    'len': len,
    'sum': sum,
    'min': min,
    'max': max,
    'sorted': sorted,
    # Add more safe functions if needed
}

# Whitelist of allowed attribute names (e.g., math.sqrt could be added)
_SAFE_ATTRIBUTES = {
    # Example: ('math', 'sqrt')
}

def _check_ast(node: ast.AST) -> None:
    """
    Recursively verify that all nodes in the AST are safe.
    Raise ValueError if a disallowed node is found.
    """
    if type(node) not in _SAFE_NODES:
        raise ValueError(f"Disallowed syntax: {type(node).__name__}")

    # Special checks for Call nodes
    if isinstance(node, ast.Call):
        func = node.func
        # Function must be a Name or Attribute in the whitelist
        if isinstance(func, ast.Name):
            if func.id not in _SAFE_CALLS:
                raise ValueError(f"Disallowed function call: {func.id}")
        elif isinstance(func, ast.Attribute):
            # Ensure attribute access is allowed
            if (isinstance(func.value, ast.Name) and
                (func.value.id, func.attr) in _SAFE_ATTRIBUTES):
                pass
            else:
                raise ValueError(f"Disallowed attribute access: {ast.dump(func)}")
        else:
            raise ValueError("Unsupported function type in call")

    # Recursively check all child nodes
    for child in ast.iter_child_nodes(node):
        _check_ast(child)

def run_user_script(user_script: str) -> Optional[Any]:
    """
    Execute a user supplied Python script in a restricted environment.

    Parameters
    ----------
    user_script : str
        The Python code to execute.

    Returns
    -------
    Any or None
        The value of the last expression in the script, if any.

    Raises
    ------
    ValueError
        If the script contains disallowed syntax or operations.
    """
    try:
        # Parse the script into an AST
        parsed = ast.parse(user_script, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user script: {e}")

    # Validate the AST
    _check_ast(parsed)

    # Prepare a restricted global namespace
    safe_globals = {"__builtins__": None}
    safe_globals.update(_SAFE_CALLS)

    # Execute the script
    exec(compile(parsed, filename="<user_script>", mode="exec"),
         safe_globals,
         None)

    # If the script ends with an expression, evaluate and return its value
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        expr_value = eval(compile(ast.Expression(parsed.body[-1].value),
                                 filename="<user_script>",
                                 mode="eval"),
                          safe_globals,
                          None)
        return expr_value

    return None