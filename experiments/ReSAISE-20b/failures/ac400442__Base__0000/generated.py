import ast
from typing import Any, Optional

# Allowed AST node types for a safe snippet
_ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Expression,
    ast.Load,
    ast.Store,
    ast.Name,
    ast.Constant,          # literals
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,              # but we will restrict the called functions
    ast.keyword,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Attribute,         # only safe attributes
}

# Allowed built-in functions (e.g., len, sum)
_ALLOWED_BUILTINS = {
    'abs', 'all', 'any', 'ascii', 'bin', 'bool',
    'chr', 'complex', 'dict', 'dir', 'divmod',
    'float', 'format', 'frozenset', 'hash',
    'hex', 'int', 'isinstance', 'issubclass',
    'iter', 'len', 'list', 'map', 'max', 'min',
    'next', 'oct', 'ord', 'pow', 'range',
    'repr', 'reversed', 'round', 'set', 'slice',
    'sorted', 'str', 'sum', 'tuple', 'zip'
}

# Whitelisted attributes for objects
_ALLOWED_ATTRIBUTES = {
    int: {'bit_length', 'to_bytes'},
    float: {'is_integer'},
    str: {'lower', 'upper', 'strip', 'split'},
    list: {'append', 'extend', 'pop', 'index', 'count'},
    dict: {'keys', 'values', 'items', 'get'},
    set: {'add', 'remove', 'discard', 'pop'},
}

class _SafeNodeVisitor(ast.NodeVisitor):
    def visit(self, node: ast.AST) -> None:
        if type(node) not in _ALLOWED_NODES:
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        # Only allow calls to allowed built-ins
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in _ALLOWED_BUILTINS:
                raise ValueError(f"Disallowed function call: {func_name}")
        else:
            # Disallow attribute calls or other forms
            raise ValueError("Only direct calls to allowed built-ins are permitted")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        # Ensure the attribute belongs to a whitelisted type
        if isinstance(node.value, ast.Name):
            # The value is a variable; we cannot know its type statically
            # So we disallow attribute access on user variables
            raise ValueError("Attribute access on variables is not allowed")
        elif isinstance(node.value, ast.Call):
            # Attribute on a literal call (e.g., int().bit_length())
            if isinstance(node.value.func, ast.Name):
                func_name = node.value.func.id
                if func_name in _ALLOWED_BUILTINS:
                    obj_type = eval(func_name)  # safe because built-in
                    if node.attr not in _ALLOWED_ATTRIBUTES.get(obj_type, set()):
                        raise ValueError(f"Disallowed attribute '{node.attr}' for {func_name}")
                else:
                    raise ValueError(f"Disallowed function call in attribute access: {func_name}")
            else:
                raise ValueError("Complex attribute chain not allowed")
        self.generic_visit(node)

def execute_code_snippet(code_snippet: str) -> Optional[Any]:
    """
    Execute a small Python code snippet safely.

    Parameters
    ----------
    code_snippet : str
        The user supplied Python code.

    Returns
    -------
    Any or None
        The result of the expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or operations.
    """
    # Parse the code into an AST
    try:
        tree = ast.parse(code_snippet, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}") from None

    # Validate the AST
    _SafeNodeVisitor().visit(tree)

    # Prepare a restricted globals dictionary
    safe_globals = {name: __builtins__[name] for name in _ALLOWED_BUILTINS}
    safe_globals['__builtins__'] = None  # prevent access to other built-ins

    # Execute the code
    exec(compile(tree, filename="<safe_snippet>", mode="exec"), safe_globals, None)

    # If the last node is an expression, return its value
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        expr_code = compile(ast.Expression(body=tree.body[-1].value), filename="<safe_snippet>", mode="eval")
        return eval(expr_code, safe_globals, None)

    return None