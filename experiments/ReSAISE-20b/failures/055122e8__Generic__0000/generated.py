import ast

# List of AST node types that are disallowed
PROHIBITED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # function calls (e.g., open(), eval(), exec())
    ast.Attribute,     # attribute access like os.system
    ast.Subscript,     # e.g., open('file').read()
    ast.Global,
    ast.Nonlocal,
)

# Disallowed function names that are commonly dangerous
PROHIBITED_FUNCTIONS = {
    'open',
    'exec',
    'eval',
    'compile',
    '__import__',
}

# Disallowed module names
PROHIBITED_MODULES = {
    'os',
    'sys',
    'subprocess',
    'socket',
    'shutil',
    'pickle',
    'marshal',
    'inspect',
}

class SafetyVisitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def generic_visit(self, node):
        if isinstance(node, PROHIBITED_NODES):
            self.errors.append(f"Disallowed node type: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node):
        # Check if the function being called is disallowed
        func_name = self._get_call_func_name(node.func)
        if func_name in PROHIBITED_FUNCTIONS:
            self.errors.append(f"Disallowed function call: {func_name}")
        super().visit_Call(node)

    def visit_Attribute(self, node):
        # Prevent attribute access to dangerous modules
        attr_chain = self._get_attribute_chain(node)
        if any(part in PROHIBITED_MODULES for part in attr_chain):
            self.errors.append(f"Disallowed attribute access: {'.'.join(attr_chain)}")
        super().visit_Attribute(node)

    def _get_call_func_name(self, func):
        if isinstance(func, ast.Name):
            return func.id
        elif isinstance(func, ast.Attribute):
            return func.attr
        return None

    def _get_attribute_chain(self, node):
        parts = []
        current = node
        while isinstance(current, ast.Attribute):
            parts.insert(0, current.attr)
            current = current.value
        if isinstance(current, ast.Name):
            parts.insert(0, current.id)
        return parts

def execute_python_script(python_code: str):
    """
    Execute a user-provided Python script in a restricted environment.

    Parameters
    ----------
    python_code : str
        The user-provided Python code to execute.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the script contains disallowed operations or invalid syntax.
    """
    # 1. Syntax check
    try:
        parsed = ast.parse(python_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in script: {e}") from None

    # 2. Static safety checks
    visitor = SafetyVisitor()
    visitor.visit(parsed)
    if visitor.errors:
        raise ValueError(f"Prohibited operations detected: {', '.join(visitor.errors)}")

    # 3. Execute in a very restricted namespace
    safe_globals = {
        "__builtins__": {  # expose only a minimal set of safe built-ins
            "abs": abs,
            "all": all,
            "any": any,
            "bool": bool,
            "chr": chr,
            "dict": dict,
            "float": float,
            "int": int,
            "len": len,
            "list": list,
            "max": max,
            "min": min,
            "print": print,
            "range": range,
            "str": str,
            "sum": sum,
        },
    }
    safe_locals = {}

    try:
        exec(compile(parsed, filename="<user_script>", mode="exec"), safe_globals, safe_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None

    return None