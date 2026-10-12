import ast
import sys
from contextlib import redirect_stdout
from io import StringIO

# Whitelist of allowed built‑in functions and modules
SAFE_BUILTINS = {
    'print',
    'len',
    'sum',
    'range',
    'min',
    'max',
    'abs',
    'round',
    'str',
    'int',
    'float',
}

# Whitelist of allowed AST node types
SAFE_NODES = {
    ast.Module,
    ast.Expr,
    ast.Call,
    ast.Name,
    ast.Load,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,          # Python <3.8
    ast.Str,          # Python <3.8
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Compare,
    ast.BoolOp,
    ast.And,
    ast.Or,
    ast.Not,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Is,
    ast.IsNot,
    ast.In,
    ast.NotIn,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.USub,
    ast.UAdd,
    # Allow simple function definitions if they contain only safe nodes
    ast.FunctionDef,
    ast.arguments,
    ast.arg,
    ast.Return,
}

def _is_safe(node: ast.AST) -> bool:
    """
    Recursively verify that a node and all its children belong to the whitelist.
    Also checks that function calls are only to whitelisted built‑ins.
    """
    if type(node) not in SAFE_NODES:
        return False

    # Special handling for function calls
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            if node.func.id not in SAFE_BUILTINS:
                return False
        else:
            # Disallow attribute calls like os.system()
            return False

    for child in ast.iter_child_nodes(node):
        if not _is_safe(child):
            return False
    return True

def execute_user_code(script_to_execute: str):
    """
    Execute a user supplied Python script in a highly restricted environment.
    Only a minimal set of safe operations are allowed. The function returns
    the captured stdout output as a string, or None if nothing was printed.
    
    Raises:
        ValueError: If the script contains prohibited syntax or unsafe
                    operations, or if it fails to parse.
    """
    # Parse the script into an AST
    try:
        tree = ast.parse(script_to_execute, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user script: {e}")

    # Validate the AST
    if not _is_safe(tree):
        raise ValueError("User script contains prohibited operations")

    # Prepare a restricted globals dictionary
    safe_globals = {"__builtins__": {name: __builtins__[name] for name in SAFE_BUILTINS}}
    safe_locals = {}

    # Capture stdout
    output_io = StringIO()
    try:
        with redirect_stdout(output_io):
            exec(compile(tree, filename="<user_script>", mode="exec"),
                 safe_globals,
                 safe_locals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from exc

    output = output_io.getvalue()
    return output if output else None