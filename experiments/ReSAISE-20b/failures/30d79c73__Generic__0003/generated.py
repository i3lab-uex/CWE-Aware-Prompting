import ast
import io
import sys
from contextlib import redirect_stdout

# List of built‑in names that are disallowed in user code
FORBIDDEN_BUILTINS = {
    'open', 'exec', 'eval', 'compile', 'input',
    '__import__', 'globals', 'locals', 'vars',
}

# List of modules that should not be imported
FORBIDDEN_MODULES = {'os', 'sys', 'subprocess', 'shutil'}

# Optionally allow a very small set of safe built‑ins
SAFE_BUILTINS = {
    'print', 'len', 'sum', 'range', 'abs',
    'min', 'max', 'list', 'dict', 'set', 'tuple',
    'str', 'int', 'float', 'bool', 'type',
}

class ForbiddenNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name.split('.')[0] in FORBIDDEN_MODULES:
                self.errors.append(f"Import of module '{alias.name}' is forbidden.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module and node.module.split('.')[0] in FORBIDDEN_MODULES:
            self.errors.append(f"Import from module '{node.module}' is forbidden.")
        self.generic_visit(node)

    def visit_Call(self, node):
        # Check for calls to forbidden built‑ins
        if isinstance(node.func, ast.Name):
            if node.func.id in FORBIDDEN_BUILTINS:
                self.errors.append(f"Call to forbidden built‑in '{node.func.id}'.")
        elif isinstance(node.func, ast.Attribute):
            # e.g., os.system(...)
            if (isinstance(node.func.value, ast.Name) and
                node.func.value.id in FORBIDDEN_MODULES):
                self.errors.append(f"Call to forbidden module '{node.func.value.id}'.")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Prevent attribute access on disallowed modules
        if isinstance(node.value, ast.Name) and node.value.id in FORBIDDEN_MODULES:
            self.errors.append(f"Attribute access on forbidden module '{node.value.id}'.")
        self.generic_visit(node)

def evaluate_user_input(user_code: str):
    """
    Execute a small user supplied Python script in a restricted environment.
    Raises ValueError if the code contains forbidden constructs or syntax errors.
    Returns the captured stdout as a string, or None if nothing was printed.
    """
    # Parse code and check for syntax errors
    try:
        tree = ast.parse(user_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user code: {e}")

    # Walk the AST for forbidden patterns
    visitor = ForbiddenNodeVisitor()
    visitor.visit(tree)
    if visitor.errors:
        raise ValueError("Forbidden code detected:\n" + "\n".join(visitor.errors))

    # Prepare a safe globals dictionary
    safe_globals = {'__builtins__': {}}
    for name in SAFE_BUILTINS:
        safe_globals[name] = getattr(__builtins__, name)

    # Capture stdout
    output_io = io.StringIO()
    try:
        with redirect_stdout(output_io):
            exec(compile(tree, filename='<user_code>', mode='exec'), safe_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}")

    output = output_io.getvalue()
    return output if output else None