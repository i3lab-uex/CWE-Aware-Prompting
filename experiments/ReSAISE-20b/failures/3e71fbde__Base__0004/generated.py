import ast
import builtins
import io
import sys
from types import ModuleType

# List of AST nodes or names that are disallowed in the snippet
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Call,  # we will check the function name separately
}
DISALLOWED_NAMES = {
    'open',
    'eval',
    'exec',
    'compile',
    '__import__',
    'os',
    'sys',
    'subprocess',
    'shutil',
    'pickle',
    'marshal',
    'builtins',
}

def _is_disallowed_call(node: ast.Call) -> bool:
    """
    Determine if a Call node is calling a disallowed function.
    Handles both direct calls (e.g., open()) and attribute calls
    (e.g., os.system()).
    """
    # direct function name
    if isinstance(node.func, ast.Name):
        return node.func.id in DISALLOWED_NAMES

    # attribute call (e.g., os.system)
    if isinstance(node.func, ast.Attribute):
        # Resolve the base name if it is a Name
        attr_chain = []
        cur = node.func
        while isinstance(cur, ast.Attribute):
            attr_chain.append(cur.attr)
            cur = cur.value
        if isinstance(cur, ast.Name):
            attr_chain.append(cur.id)
            full_name = ".".join(reversed(attr_chain))
            # Any part of the chain that is disallowed triggers rejection
            return any(part in DISALLOWED_NAMES for part in attr_chain)
    return False

def _check_ast(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if any disallowed
    construct is found.
    """
    for child in ast.iter_child_nodes(node):
        if type(child) in DISALLOWED_NODES:
            # Import or ImportFrom
            raise ValueError(f"Disallowed import statement at line {child.lineno}")
        if isinstance(child, ast.Call) and _is_disallowed_call(child):
            raise ValueError(f"Disallowed function call at line {child.lineno}")
        # Recurse into children
        _check_ast(child)

def run_code_snippet(snippet: str):
    """
    Execute a small Python code snippet safely.

    Parameters
    ----------
    snippet : str
        The Python code to execute.

    Returns
    -------
    None or str
        If the snippet produces output via `print`, that output is returned as a string.
        Otherwise, None is returned.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations such as imports or dangerous calls.
    """
    # Validate the code by parsing it into an AST
    try:
        tree = ast.parse(snippet, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}")

    # Walk the AST to detect disallowed constructs
    _check_ast(tree)

    # Prepare a restricted globals dictionary
    safe_builtins = {k: v for k, v in builtins.__dict__.items()
                     if k in ('abs', 'all', 'any', 'bool', 'dict',
                              'float', 'int', 'len', 'list', 'max',
                              'min', 'pow', 'range', 'round', 'str',
                              'sum', 'tuple', 'enumerate', 'zip')}
    globals_dict = {"__builtins__": safe_builtins}

    # Capture stdout
    old_stdout = sys.stdout
    buffer = io.StringIO()
    try:
        sys.stdout = buffer
        exec(compile(tree, filename="<snippet>", mode="exec"), globals_dict)
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()
    return output if output else None