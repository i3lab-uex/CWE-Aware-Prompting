import ast

# Define a whitelist of safe node types and names
SAFE_NODES = {
    # Module & statement nodes
    ast.Module, ast.Expr,
    # Expressions
    ast.Constant, ast.Name, ast.Load,
    # Operations
    ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
    ast.UAdd, ast.USub,
    ast.And, ast.Or, ast.Not,
    # Comparisons
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Ternary
    ast.IfExp,
    # Function calls (only whitelisted)
    ast.Call, ast.Attribute,
}
SAFE_NAMES = {
    # Built‑in functions that are considered safe
    'abs', 'round', 'min', 'max',
}
SAFE_ATTRIBUTES = {
    # Allowed attributes for built‑in types (e.g., int.bit_length)
    'int': {'bit_length'},
    'float': {'is_integer'},
}

class SafeVisitor(ast.NodeVisitor):
    def visit(self, node):
        if type(node) not in SAFE_NODES:
            raise ValueError(f"Disallowed node: {type(node).__name__}")
        super().visit(node)

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id not in SAFE_NAMES:
            # Allow only whitelisted names
            raise ValueError(f"Disallowed name: {node.id}")

    def visit_Call(self, node):
        # Ensure the function being called is whitelisted
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in SAFE_NAMES:
                raise ValueError(f"Disallowed function call: {func_name}")
        elif isinstance(node.func, ast.Attribute):
            # e.g., int.bit_length()
            if not (isinstance(node.func.value, ast.Name) and
                    node.func.value.id in SAFE_ATTRIBUTES and
                    node.func.attr in SAFE_ATTRIBUTES[node.func.value.id]):
                raise ValueError(f"Disallowed attribute access: {ast.dump(node)}")
        else:
            raise ValueError("Only simple function calls are allowed.")
        self.generic_visit(node)

def run_python_snippet(python_snippet: str):
    """
    Execute a simple, safe Python snippet.

    Parameters
    ----------
    python_snippet : str
        The code to execute. Only a limited set of expressions and statements are allowed.

    Returns
    -------
    Any
        The value of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed syntax or operations.
    """
    # Parse the code into an AST
    try:
        tree = ast.parse(python_snippet, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}") from None

    # Validate the AST
    SafeVisitor().visit(tree)

    # Prepare a restricted globals dictionary
    safe_globals = {
        '__builtins__': {name: __builtins__[name] for name in SAFE_NAMES}
    }

    # Execute the code
    exec(compile(tree, filename="<snippet>", mode="exec"), safe_globals)

    # If the snippet ends with an expression, return its value
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        expr_code = compile(ast.Expression(body=tree.body[-1].value), filename="<expr>", mode="eval")
        return eval(expr_code, safe_globals)

    return None