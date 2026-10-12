import ast

# Allowed built‑ins for the sandboxed environment
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'chr': chr,
    'complex': complex,
    'dict': dict,
    'divmod': divmod,
    'enumerate': enumerate,
    'filter': filter,
    'float': float,
    'format': format,
    'hash': hash,
    'hex': hex,
    'int': int,
    'isinstance': isinstance,
    'issubclass': issubclass,
    'iter': iter,
    'len': len,
    'list': list,
    'map': map,
    'max': max,
    'min': min,
    'next': next,
    'oct': oct,
    'ord': ord,
    'pow': pow,
    'range': range,
    'repr': repr,
    'reversed': reversed,
    'round': round,
    'sorted': sorted,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    'zip': zip,
}

# AST visitor that rejects disallowed nodes
class SafeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    # Disallow import statements
    def visit_Import(self, node):
        self.errors.append(f"Disallowed Import statement at line {node.lineno}")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.errors.append(f"Disallowed ImportFrom statement at line {node.lineno}")
        self.generic_visit(node)

    # Disallow calls to dangerous built‑ins or functions
    def visit_Call(self, node):
        # Check the function being called
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            # Disallow explicit calls to eval/exec/open, etc.
            if func_name in {'eval', 'exec', 'open', '__import__', 'compile'}:
                self.errors.append(
                    f"Disallowed function call '{func_name}' at line {node.lineno}"
                )
        elif isinstance(node.func, ast.Attribute):
            # Disallow attribute access to modules like os or sys
            if isinstance(node.func.value, ast.Name):
                if node.func.value.id in {'os', 'sys', 'subprocess'}:
                    self.errors.append(
                        f"Disallowed attribute call '{node.func.value.id}.{node.func.attr}' at line {node.lineno}"
                    )
        self.generic_visit(node)

    # Disallow attribute access to dangerous modules
    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id in {'os', 'sys', 'subprocess'}:
            self.errors.append(
                f"Disallowed attribute access '{node.value.id}.{node.attr}' at line {node.lineno}"
            )
        self.generic_visit(node)

    # Disallow usage of globals() or locals()
    def visit_Name(self, node):
        if node.id in {'globals', 'locals'}:
            self.errors.append(
                f"Disallowed use of '{node.id}' at line {node.lineno}"
            )
        self.generic_visit(node)

def execute_user_code(submitted_code: str):
    """
    Execute a user‑supplied Python script in a restricted environment.
    
    Parameters
    ----------
    submitted_code : str
        The code to execute.

    Returns
    -------
    Any
        Result of the executed script if a variable named 'result' is set;
        otherwise None.

    Raises
    ------
    ValueError
        If the script contains prohibited operations or invalid syntax.
    """
    # Parse code to AST and validate syntax
    try:
        tree = ast.parse(submitted_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Invalid syntax: {e}") from None

    # Walk the AST to detect disallowed patterns
    visitor = SafeVisitor()
    visitor.visit(tree)
    if visitor.errors:
        raise ValueError("Prohibited operations detected:\n" + "\n".join(visitor.errors))

    # Prepare the sandboxed globals dictionary
    sandbox_globals = {'__builtins__': SAFE_BUILTINS}

    # Execute the code
    try:
        exec(compile(tree, filename="<user_code>", mode="exec"), sandbox_globals)
    except Exception as e:
        raise ValueError(f"Execution error: {e}") from None

    # Return a result if the user assigned to 'result'
    return sandbox_globals.get('result')