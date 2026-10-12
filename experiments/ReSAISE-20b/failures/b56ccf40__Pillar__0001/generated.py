import ast
import sys
import io
from contextlib import redirect_stdout

# ------------------------------------------------------------------
# 1. Whitelist of safe AST node types
SAFE_NODES = {
    ast.Module,
    ast.Expr,
    ast.Call,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.Compare,
    ast.BoolOp,
    ast.operator,
    ast.unaryop,
    ast.cmpop,
    ast.keyword,
    ast.ListComp,
    ast.DictComp,
    ast.SetComp,
    ast.GeneratorExp,
    ast.comprehension,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.IfExp,
    ast.Lambda,
    ast.Attribute,  # but restrict attribute names
}

# ------------------------------------------------------------------
# 2. Whitelist of safe builtins
SAFE_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'sum': sum,
    'min': min,
    'max': max,
}

# ------------------------------------------------------------------
def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively verify that the node and its children are of an allowed type.
    Also check that attribute accesses are to whitelisted attributes only.
    """
    if not isinstance(node, tuple(SAFE_NODES)):
        return False

    # Special handling for Attribute: only allow safe attributes on builtins
    if isinstance(node, ast.Attribute):
        # e.g., math.sqrt would be disallowed because 'math' is not allowed
        if isinstance(node.value, ast.Name) and node.value.id in SAFE_BUILTINS:
            # allow attribute if it exists on the builtin
            return hasattr(SAFE_BUILTINS[node.value.id], node.attr)
        return False

    for child in ast.iter_child_nodes(node):
        if not _is_safe_node(child):
            return False
    return True

# ------------------------------------------------------------------
def process_user_code(code_submission: str):
    """
    Safely execute a user‑supplied Python script.

    Parameters
    ----------
    code_submission : str
        The source code to execute.

    Returns
    -------
    output : str or None
        Captured stdout if any, otherwise None.

    Raises
    ------
    ValueError
        If the script contains forbidden operations or has syntax errors.
    """
    # 1. Parse code to AST and check for syntax errors
    try:
        parsed = ast.parse(code_submission, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from None

    # 2. Verify that the AST only contains safe nodes
    if not _is_safe_node(parsed):
        raise ValueError("User code contains forbidden operations or unsafe constructs.")

    # 3. Prepare restricted globals
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    # Provide a local namespace for the exec
    safe_locals = {}

    # 4. Capture stdout
    output_buffer = io.StringIO()
    try:
        with redirect_stdout(output_buffer):
            exec(compile(parsed, filename="<user_script>", mode="exec"),
                 safe_globals,
                 safe_locals)
    except Exception as exc:
        raise ValueError(f"Runtime error in user code: {exc}") from None

    output = output_buffer.getvalue()
    return output if output else None