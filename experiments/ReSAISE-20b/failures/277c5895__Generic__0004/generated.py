import ast
import sys
import types
from typing import Any, Dict

# --------------------------------------------------------------------------- #
# 1. Define a whitelist of safe built‑in functions and constants
# --------------------------------------------------------------------------- #
SAFE_BUILTINS: Dict[str, Any] = {
    # basic types & functions
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'bytes': bytes,
    'chr': chr,
    'dict': dict,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'pow': pow,
    'range': range,
    'repr': repr,
    'round': round,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    # constants
    'True': True,
    'False': False,
    'None': None,
}

# --------------------------------------------------------------------------- #
# 2. Visitor that detects disallowed nodes
# --------------------------------------------------------------------------- #
class _SafetyVisitor(ast.NodeVisitor):
    """
    Walks the AST and raises ValueError if any disallowed construct is found.
    """

    # Nodes that are outright forbidden
    _FORBIDDEN_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Exec,            # present only in Python 2; harmless here but keep for clarity
        ast.Global,
        ast.Nonlocal,
        ast.With,            # may be used to open files
    )

    # Function names that are dangerous
    _FORBIDDEN_FUNCTIONS = {
        'eval',
        'exec',          # Python 3 doesn't have exec() built‑in, but keep for safety
        'open',
        'compile',
        'input',
        'importlib',     # modules that can import other code
        '__import__',
    }

    def visit(self, node: ast.AST) -> Any:
        if isinstance(node, self._FORBIDDEN_NODES):
            raise ValueError(f"Disallowed construct: {type(node).__name__}")
        return super().visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        # Detect calls to forbidden functions
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            # e.g., os.system()
            func_name = node.func.attr
        if func_name in self._FORBIDDEN_FUNCTIONS:
            raise ValueError(f"Forbidden function call: {func_name}")
        return self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        # Prevent attribute access that could lead to dangerous modules
        if isinstance(node.value, ast.Name):
            # e.g., os.system -> disallow 'os'
            if node.value.id in {'os', 'sys', 'subprocess'}:
                raise ValueError(f"Forbidden attribute access: {node.value.id}.{node.attr}")
        return self.generic_visit(node)

# --------------------------------------------------------------------------- #
# 3. The main execution function
# --------------------------------------------------------------------------- #
def execute_user_code(submitted_code: str) -> Any:
    """
    Execute a user supplied Python script in a restricted environment.

    Parameters
    ----------
    submitted_code : str
        The code to execute. May contain multiple statements.

    Returns
    -------
    Any
        The value of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the code contains disallowed syntax or semantics.
    SyntaxError
        If the submitted code cannot be parsed.
    """
    # 1. Parse and validate syntax
    try:
        tree = ast.parse(submitted_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid syntax: {exc}") from exc

    # 2. Walk the AST to ensure safety
    _SafetyVisitor().visit(tree)

    # 3. Prepare a restricted execution environment
    safe_globals: Dict[str, Any] = {
        '__builtins__': SAFE_BUILTINS,
    }

    # 4. Compile the code object
    code_obj = compile(tree, filename='<user_code>', mode='exec')

    # 5. Execute the code
    exec(code_obj, safe_globals)

    # 6. If the last node is an expression, evaluate and return its value
    if tree.body:
        last_stmt = tree.body[-1]
        if isinstance(last_stmt, ast.Expr):
            # Evaluate the expression in the same environment
            expr_code = compile(ast.Expression(body=last_stmt.value), filename='<user_expr>', mode='eval')
            return eval(expr_code, safe_globals)

    # 7. No result to return
    return None

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     code = """
# a = 5
# b = 10
# a + b
# """
#     print(execute_user_code(code))   # Output: 15