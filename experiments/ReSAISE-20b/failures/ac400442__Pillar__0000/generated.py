import ast

# List of names that are explicitly disallowed in the snippet.
DISALLOWED_NAMES = {
    "open",
    "eval",
    "exec",
    "__import__",
    "os",
    "sys",
    "subprocess",
    "shutil",
    "socket",
    "pickle",
}

class _SafeNodeVisitor(ast.NodeVisitor):
    """AST visitor that ensures only harmless nodes are present."""
    def visit_Import(self, node):
        raise ValueError("Import statements are not allowed.")
    
    def visit_ImportFrom(self, node):
        raise ValueError("Import-from statements are not allowed.")
    
    def visit_Call(self, node):
        # disallow any function calls (including builtins like print)
        raise ValueError("Function calls are not allowed.")
    
    def visit_Attribute(self, node):
        # disallow attribute access (e.g., os.system)
        raise ValueError("Attribute access is not allowed.")
    
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id in DISALLOWED_NAMES:
            raise ValueError(f"Use of '{node.id}' is not allowed.")
        # other names are fine (e.g., literals, math constants)
    
    def visit_Subscript(self, node):
        # allow subscript (e.g., list indexing)
        self.generic_visit(node)

    def visit_BinOp(self, node):
        # allow binary operations
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        # allow unary operations
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        # allow boolean operations
        self.generic_visit(node)

    def visit_Compare(self, node):
        # allow comparisons
        self.generic_visit(node)

    def generic_visit(self, node):
        # For any other nodes that are not explicitly handled,
        # we default to allowing them if they are harmless.
        allowed_types = (
            ast.Module,
            ast.Expr,
            ast.Expression,
            ast.Num,
            ast.Str,
            ast.Bytes,
            ast.Constant,  # Python 3.8+
            ast.NameConstant,  # older
            ast.Tuple,
            ast.List,
            ast.Dict,
        )
        if not isinstance(node, allowed_types):
            raise ValueError(f"Node type {type(node).__name__} is not allowed.")
        super().generic_visit(node)

def execute_code_snippet(code_snippet: str):
    """
    Execute a small, harmless Python code snippet.

    Parameters
    ----------
    code_snippet : str
        The Python code to be executed.

    Returns
    -------
    Any
        Result of evaluating the snippet if it is an expression, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations.
    """
    # Parse the code into an AST and validate it
    try:
        tree = ast.parse(code_snippet, mode="eval")
        # If parsing as eval succeeds, it's a single expression
        result = True
    except SyntaxError:
        # Try parsing as a module (statements)
        tree = ast.parse(code_snippet, mode="exec")
        result = None

    # Validate the AST
    _SafeNodeVisitor().visit(tree)

    # Prepare a restricted global environment
    safe_globals = {"__builtins__": {}}
    safe_locals = {}

    if isinstance(tree, ast.Expression):
        # Evaluate the expression safely
        return eval(compile(tree, filename="<snip>", mode="eval"),
                    safe_globals, safe_locals)
    else:
        # Execute statements (no result expected)
        exec(compile(tree, filename="<snip>", mode="exec"),
             safe_globals, safe_locals)
        return None