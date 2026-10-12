import ast
from types import FunctionType, CodeType
from typing import Any, Dict

# A minimal set of safe built‑ins that we allow the user to access.
SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'dict': dict,
    'set': set,
    'tuple': tuple,
    'enumerate': enumerate,
    'zip': zip,
    'abs': abs,
    'min': min,
    'max': max,
    # Add more safe functions as needed
}

# List of node types that are considered dangerous.
FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Call,          # calls to disallowed functions
    ast.Attribute,     # attribute access can expose dangerous objects
    ast.Lambda,
    ast.Global,
    ast.Nonlocal,
    ast.Delete,
)

# Disallowed function names
FORBIDDEN_FUNC_NAMES = {
    'eval',
    'exec',
    'compile',
    '__import__',
    'open',
    'input',
    'help',
    'dir',
    'vars',
    'locals',
    'globals',
}

class SecurityVisitor(ast.NodeVisitor):
    """
    Walks the AST and raises ValueError if it finds forbidden constructs.
    """
    def __init__(self):
        self.found_forbidden = False

    def generic_visit(self, node: ast.AST):
        if isinstance(node, FORBIDDEN_NODES):
            raise ValueError(f"Forbidden statement or expression: {ast.dump(node)}")
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # disallow calls to forbidden functions
        if isinstance(node.func, ast.Name) and node.func.id in FORBIDDEN_FUNC_NAMES:
            raise ValueError(f"Call to forbidden function: {node.func.id}")
        # allow other calls, but still visit arguments
        super().visit_Call(node)

    def visit_Attribute(self, node: ast.Attribute):
        # disallow attribute access that could reach dangerous objects
        raise ValueError(f"Attribute access not allowed: {ast.dump(node)}")
        # super().visit_Attribute(node)

def _compile_snippet(code: str) -> CodeType:
    """
    Compile the snippet after ensuring it is safe.
    Returns a code object ready for exec or eval.
    """
    try:
        parsed = ast.parse(code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Invalid Python code: {e}") from None

    # Perform security checks
    SecurityVisitor().visit(parsed)

    # Check for top-level expressions that we might want to evaluate
    if len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr):
        # single expression: compile in eval mode
        return compile(parsed, filename='<user_snippet>', mode='eval')
    else:
        # statement block
        return compile(parsed, filename='<user_snippet>', mode='exec')

def execute_python_code(snippet_code: str) -> Any:
    """
    Execute a user supplied Python snippet in a sandboxed environment.
    
    Parameters
    ----------
    snippet_code : str
        The user provided Python code to execute.

    Returns
    -------
    Any
        The result of evaluating the snippet if it is a single expression,
        otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or is syntactically invalid.
    """
    if not isinstance(snippet_code, str):
        raise ValueError("snippet_code must be a string")

    code_obj = _compile_snippet(snippet_code)

    # Prepare the sandbox environment
    sandbox: Dict[str, Any] = {}
    sandbox.update(SAFE_BUILTINS)

    # Execute the compiled code
    if code_obj.co_flags & 0x0008:  # eval mode flag (CO_FUTURE_DIVISION etc.)
        # It's an expression
        return eval(code_obj, {"__builtins__": SAFE_BUILTINS}, sandbox)
    else:
        exec(code_obj, {"__builtins__": SAFE_BUILTINS}, sandbox)
        return None