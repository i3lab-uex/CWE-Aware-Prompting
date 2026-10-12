import ast
import sys
from io import StringIO

class _SafeVisitor(ast.NodeVisitor):
    """
    Visitor that checks for disallowed AST nodes.
    """
    # Node types that are explicitly forbidden
    FORBIDDEN_NODES = {
        ast.Import,
        ast.ImportFrom,
        ast.Call,      # We will check calls separately
        ast.Attribute,  # Attribute access (e.g., __class__)
    }

    # Function names that are forbidden
    FORBIDDEN_CALLS = {
        'open', 'eval', 'exec', 'compile',
        '__import__', 'input', 'os.system',
    }

    def visit(self, node):
        if type(node) in self.FORBIDDEN_NODES:
            raise ValueError(f"Disallowed node: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        # Check if the function called is disallowed
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            # e.g., os.system -> forbid based on attribute name
            func_name = node.func.attr

        if func_name in self.FORBIDDEN_CALLS:
            raise ValueError(f"Disallowed function call: {func_name}")

        # Recursively visit arguments
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Disallow any attribute access (e.g., __dict__, __class__)
        attr_name = node.attr
        if attr_name.startswith('__') and attr_name.endswith('__'):
            raise ValueError(f"Disallowed attribute access: {attr_name}")
        self.generic_visit(node)

def run_code_snippet(snippet: str):
    """
    Execute a small Python code snippet in a sandboxed environment.
    
    Parameters
    ----------
    snippet : str
        The code to execute.

    Returns
    -------
    None or the printed output as a string.
    
    Raises
    ------
    ValueError
        If the snippet contains disallowed operations.
    """
    # 1. Parse the code to an AST and validate it
    try:
        tree = ast.parse(snippet, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}") from None

    # Validate the AST
    _SafeVisitor().visit(tree)

    # 2. Execute the snippet, capturing stdout
    old_stdout = sys.stdout
    buffer = StringIO()
    try:
        sys.stdout = buffer
        # Execute in a restricted namespace
        exec(compile(tree, filename="<snippet>", mode="exec"), {})
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()
    return output if output else None