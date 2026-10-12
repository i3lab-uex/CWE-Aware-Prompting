import ast
import builtins
import math

# ----------------------------------------------------------------------
# Helper: whitelist of safe built‑in functions / constants
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
    'pow': pow,
    'range': range,
    'round': round,
    'sum': sum,
    'tuple': tuple,
    'zip': zip,
}

# ----------------------------------------------------------------------
class _SafetyVisitor(ast.NodeVisitor):
    """
    Traverses the AST and raises ValueError if any disallowed node is found.
    """

    # Nodes that are considered unsafe
    UNSAFE_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,          # Python 2 only – kept for completeness
        ast.Call,          # calls will be filtered by name
    )

    # Call names that are disallowed (dangerous built‑ins)
    DISALLOWED_CALLS = {
        'eval',
        'exec',   # Python 3 has no exec node, but guard anyway
        'open',
        'compile',
        '__import__',
    }

    def visit(self, node):
        if isinstance(node, self.UNSAFE_NODES):
            raise ValueError(f"Disallowed operation: {type(node).__name__}")
        # For Call nodes, check the function name
        if isinstance(node, ast.Call):
            func = node.func
            # Allow attribute calls only on safe objects (e.g., math.sin)
            if isinstance(func, ast.Name):
                if func.id in self.DISALLOWED_CALLS:
                    raise ValueError(f"Disallowed function call: {func.id}")
            elif isinstance(func, ast.Attribute):
                # Prevent calls on arbitrary objects like __import__.foo()
                if isinstance(func.value, ast.Name) and func.value.id == '__import__':
                    raise ValueError("Disallowed __import__ call")
        self.generic_visit(node)

# ----------------------------------------------------------------------
def execute_python_script(python_code: str):
    """
    Executes a user‑supplied Python script in a sandboxed environment.
    Only safe built‑ins and the math module are available. The script must
    not contain imports, eval/exec calls, or other disallowed operations.

    Parameters:
        python_code (str): The code to execute.

    Returns:
        None

    Raises:
        ValueError: If the script contains prohibited operations or invalid syntax.
    """
    # 1. Parse and validate syntax
    try:
        parsed = ast.parse(python_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in script: {exc}") from None

    # 2. Walk the AST to catch unsafe nodes
    visitor = _SafetyVisitor()
    try:
        visitor.visit(parsed)
    except ValueError as exc:
        raise

    # 3. Prepare sandboxed globals
    sandbox_globals = {
        '__builtins__': SAFE_BUILTINS,
        'math': math,
    }

    # 4. Execute the script
    try:
        exec(compile(parsed, filename='<user_script>', mode='exec'), sandbox_globals)
    except Exception as exc:
        # Re‑raise as ValueError to keep API consistent
        raise ValueError(f"Execution error: {exc}") from None

    # 5. No explicit result; return None
    return None