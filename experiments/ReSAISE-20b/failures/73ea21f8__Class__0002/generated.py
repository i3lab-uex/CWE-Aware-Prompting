import ast
from types import SimpleNamespace

# -------------------------------------------------------------
# A very small safe sandbox for executing user supplied snippets.
# -------------------------------------------------------------

SAFE_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'dict', 'float', 'int',
    'len', 'list', 'max', 'min', 'pow', 'range', 'round',
    'sum', 'tuple'
}

# Node visitor that rejects disallowed constructs
class SafeVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.errors = []

    # Disallow imports
    def visit_Import(self, node):
        self.errors.append("import statements are not allowed")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.errors.append("import statements are not allowed")
        self.generic_visit(node)

    # Disallow exec/eval calls
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id in ('eval', 'exec'):
            self.errors.append(f"call to forbidden builtin {node.func.id}")
        # disallow calls to open or other unsafe builtins
        if isinstance(node.func, ast.Name) and node.func.id in ('open', 'os', 'sys'):
            self.errors.append(f"call to forbidden builtin {node.func.id}")
        self.generic_visit(node)

    # Disallow attribute access (e.g., os.system)
    def visit_Attribute(self, node):
        self.errors.append("attribute access is forbidden")
        self.generic_visit(node)

    # Disallow lambda, comprehensions, etc. for simplicity
    def visit_Lambda(self, node):
        self.errors.append("lambda expressions are not allowed")
        self.generic_visit(node)

    def visit_ListComp(self, node):
        self.errors.append("list comprehensions are not allowed")
        self.generic_visit(node)

    def visit_DictComp(self, node):
        self.errors.append("dict comprehensions are not allowed")
        self.generic_visit(node)

    def visit_SetComp(self, node):
        self.errors.append("set comprehensions are not allowed")
        self.generic_visit(node)

    def visit_GeneratorExp(self, node):
        self.errors.append("generator expressions are not allowed")
        self.generic_visit(node)

    # Allow other nodes by default
    def generic_visit(self, node):
        super().generic_visit(node)


def run_code_snippet(user_code: str):
    """
    Execute a user provided Python snippet in a highly restricted sandbox.

    Parameters
    ----------
    user_code : str
        The Python code to run.

    Returns
    -------
    Any
        Result of the executed snippet if it contains a single expression,
        otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains prohibited actions.
    """
    # Parse the code and check for safety
    try:
        tree = ast.parse(user_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user code: {e}")

    visitor = SafeVisitor()
    visitor.visit(tree)

    if visitor.errors:
        raise ValueError(f"Prohibited code detected: {', '.join(visitor.errors)}")

    # Prepare a restricted global namespace
    safe_globals = {"__builtins__": {k: __builtins__[k] for k in SAFE_BUILTINS if k in __builtins__}}
    local_ns = {}

    # If the snippet is a single expression, evaluate it
    if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr):
        expr = tree.body[0].value
        code_obj = compile(ast.Expression(expr), filename="<user>", mode="eval")
        return eval(code_obj, safe_globals, local_ns)

    # Otherwise execute the code block
    exec(compile(tree, filename="<user>", mode="exec"), safe_globals, local_ns)
    return None