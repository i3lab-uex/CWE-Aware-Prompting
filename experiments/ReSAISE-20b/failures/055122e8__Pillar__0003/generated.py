import ast
import builtins

# Whitelist of safe built‑in functions
SAFE_BUILTINS = {
    'abs', 'all', 'any', 'bool', 'chr', 'complex', 'dict',
    'float', 'hash', 'hex', 'int', 'isinstance', 'len',
    'list', 'max', 'min', 'pow', 'range', 'round', 'str',
    'tuple', 'sum', 'zip'
}

# Disallowed node types (CWE‑707: ensure code structure is safe)
FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # exec statement (Python 2)
    ast.Call,         # function calls are allowed only for safe builtins
)

class SafeVisitor(ast.NodeTransformer):
    def visit_Call(self, node):
        # Allow calls only to whitelisted built‑ins
        if isinstance(node.func, ast.Name):
            if node.func.id not in SAFE_BUILTINS:
                raise ValueError(f"Disallowed function call: {node.func.id}")
        else:
            # Disallow method calls or other complex expressions
            raise ValueError("Only direct calls to whitelisted built‑ins are allowed")
        return self.generic_visit(node)

    def visit_Import(self, node):
        raise ValueError("Imports are not allowed")

    def visit_ImportFrom(self, node):
        raise ValueError("Imports are not allowed")

def execute_python_script(python_code: str):
    """
    Execute a user provided Python script in a restricted environment.
    Only expressions and statements that use whitelisted built‑ins are permitted.
    Returns the value of the last expression or None if there is no result.
    Raises ValueError on prohibited operations or syntax errors.
    """
    # Parse the code
    try:
        tree = ast.parse(python_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user code: {e}")

    # Check for forbidden nodes
    for node in ast.walk(tree):
        if isinstance(node, FORBIDDEN_NODES):
            raise ValueError(f"Forbidden node type: {type(node).__name__}")

    # Validate calls and other constraints
    SafeVisitor().visit(tree)

    # Prepare restricted globals & locals
    safe_globals = {k: getattr(builtins, k) for k in SAFE_BUILTINS}
    safe_globals['__builtins__'] = None  # disable all other built‑ins
    local_vars = {}

    # Execute the script
    try:
        exec(compile(tree, filename="<user_script>", mode="exec"), safe_globals, local_vars)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}")

    # If the last statement is an expression, return its value
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        try:
            return eval(compile(ast.Expression(body=tree.body[-1].value), filename="<user_script>", mode="eval"),
                         safe_globals, local_vars)
        except Exception as exc:
            raise ValueError(f"Evaluation error: {exc}")

    return None