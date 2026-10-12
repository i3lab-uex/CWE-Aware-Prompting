import ast

# List of forbidden AST node types or call targets
FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # exec is a statement in Python 2; kept for completeness
    ast.Call,
)

# Call names that are considered dangerous
FORBIDDEN_CALLS = {
    "eval",
    "exec",
    "__import__",
    "open",
    "os.system",
    "subprocess.Popen",
    "subprocess.call",
    "subprocess.run",
    "sys.exit",
}

# Allowed built‑in functions
ALLOWED_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'bytes', 'chr', 'complex',
    'dict', 'float', 'int', 'len', 'list', 'map', 'max',
    'min', 'print', 'range', 'repr', 'round', 'set', 'str',
    'sum', 'tuple',
}

class SafeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def generic_visit(self, node):
        if isinstance(node, FORBIDDEN_NODES):
            self.errors.append(f"Forbidden statement: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node):
        # Detect calls to forbidden functions
        func = node.func
        if isinstance(func, ast.Name):
            name = func.id
        elif isinstance(func, ast.Attribute):
            # e.g., os.system
            parts = []
            cur = func
            while isinstance(cur, ast.Attribute):
                parts.append(cur.attr)
                cur = cur.value
            if isinstance(cur, ast.Name):
                parts.append(cur.id)
            name = ".".join(reversed(parts))
        else:
            name = None

        if name in FORBIDDEN_CALLS:
            self.errors.append(f"Forbidden call: {name}")
        self.generic_visit(node)

def safe_run_script(script_code: str):
    """
    Execute a user supplied Python script in a restricted environment.
    Raises ValueError if the script contains prohibited operations or
    invalid syntax. Returns None on successful execution.
    """
    # Parse the code to detect syntax errors
    try:
        tree = ast.parse(script_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in script: {e}") from None

    # Analyse the AST for forbidden constructs
    visitor = SafeVisitor()
    visitor.visit(tree)
    if visitor.errors:
        raise ValueError(f"Prohibited operations detected: {', '.join(visitor.errors)}")

    # Prepare a restricted global namespace
    safe_globals = {
        '__builtins__': {name: __builtins__[name] for name in ALLOWED_BUILTINS if name in __builtins__},
    }

    # Execute the script
    try:
        exec(compile(tree, filename="<safe_script>", mode="exec"), safe_globals)
    except Exception as e:
        raise ValueError(f"Execution error: {e}") from None

    return None