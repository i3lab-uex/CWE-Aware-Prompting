import ast
import io
from contextlib import redirect_stdout

# Whitelist of safe built‑in functions (empty for maximum safety)
SAFE_BUILTINS = {}

# List of node types that are explicitly disallowed
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # Python 2 only; kept for completeness
    ast.Call,          # We will check calls explicitly instead of blanket ban
)

# Disallowed function names (built‑in or otherwise)
DISALLOWED_FUNCTIONS = {
    'eval',
    'exec',
    'open',
    'compile',
    '__import__',
    'input',
    'globals',
    'locals',
    'vars',
    'dir',
    'help',
}

# Disallowed attribute names
DISALLOWED_ATTRIBUTES = {
    '__dict__',
    '__class__',
    '__bases__',
    '__subclasses__',
    '__code__',
}

def _check_node(node):
    """Recursively check AST nodes for disallowed constructs."""
    if isinstance(node, DISALLOWED_NODES):
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

    if isinstance(node, ast.Call):
        # Disallow calls to dangerous functions
        func = node.func
        if isinstance(func, ast.Name) and func.id in DISALLOWED_FUNCTIONS:
            raise ValueError(f"Disallowed function call: {func.id}")
        if isinstance(func, ast.Attribute):
            # Disallow calls on dangerous attributes
            attr = func.attr
            if attr in DISALLOWED_ATTRIBUTES:
                raise ValueError(f"Disallowed attribute call: {attr}")
        # Recursively check arguments
        for arg in node.args:
            _check_node(arg)
        for keyword in node.keywords:
            _check_node(keyword.value)

    if isinstance(node, ast.Attribute):
        if node.attr in DISALLOWED_ATTRIBUTES:
            raise ValueError(f"Disallowed attribute access: {node.attr}")

    # Recurse into all child nodes
    for child in ast.iter_child_nodes(node):
        _check_node(child)

def restricted_run_code(run_code: str):
    """
    Execute a user‑supplied Python script in a restricted environment.

    Parameters
    ----------
    run_code : str
        The user’s Python code to execute.

    Returns
    -------
    str or None
        Captured stdout output, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the code contains syntax errors or disallowed operations.
    """
    # Parse the source to an AST and validate
    try:
        tree = ast.parse(run_code, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user code: {e}") from None

    # Walk the AST to ensure only safe constructs are present
    _check_node(tree)

    # Prepare a restricted execution environment
    exec_globals = {"__builtins__": SAFE_BUILTINS}
    exec_locals = {}

    # Capture stdout
    output_buffer = io.StringIO()
    try:
        with redirect_stdout(output_buffer):
            exec(compile(tree, filename="<restricted>", mode="exec"),
                 exec_globals,
                 exec_locals)
    except Exception as e:
        raise ValueError(f"Execution error: {e}") from None

    output = output_buffer.getvalue()
    return output if output else None