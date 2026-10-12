import ast
import sys
from contextlib import redirect_stdout
from io import StringIO

# --------------------------------------------------------------------------- #
# Safe AST validation utilities
# --------------------------------------------------------------------------- #

ALLOWED_NODES = {
    ast.Module,
    ast.Expr,
    ast.Import,
    ast.ImportFrom,
    ast.FunctionDef,
    ast.Return,
    ast.Assign,
    ast.AugAssign,
    ast.For,
    ast.While,
    ast.If,
    ast.With,
    ast.ListComp,
    ast.DictComp,
    ast.SetComp,
    ast.GeneratorExp,
    # Expressions
    ast.Lambda,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,
    ast.Name,
    ast.Constant,
    ast.Num,  # for Python <3.8
    ast.Str,  # for Python <3.8
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod,
    ast.Pow, ast.LShift, ast.RShift, ast.BitOr, ast.BitXor, ast.BitAnd,
    ast.And, ast.Or, ast.Not,
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Unary ops
    ast.UAdd, ast.USub, ast.Invert,
}

ALLOWED_BUILTINS = {
    'abs': abs,
    'min': min,
    'max': max,
    'sum': sum,
    'len': len,
    'range': range,
    'print': print,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    # add more safe builtins as needed
}

def _validate_ast(node):
    """
    Recursively validate that the AST contains only allowed nodes and names.
    Raises ValueError if an illegal node is found.
    """
    for child in ast.iter_child_nodes(node):
        if type(child) not in ALLOWED_NODES:
            raise ValueError(f"Disallowed syntax: {type(child).__name__}")
        if isinstance(child, ast.Name):
            # Names used in calls must be from allowed builtins or local variables
            if child.id not in ALLOWED_BUILTINS and not isinstance(node, (ast.FunctionDef, ast.Module)):
                # This simple check assumes local names are defined elsewhere in the script
                pass
        if isinstance(child, ast.Call):
            # Validate function name
            func = child.func
            if isinstance(func, ast.Name):
                if func.id not in ALLOWED_BUILTINS:
                    raise ValueError(f"Calling disallowed function '{func.id}'")
            elif isinstance(func, ast.Attribute):
                # Disallow attribute access entirely
                raise ValueError("Attribute access is disallowed")
        _validate_ast(child)

# --------------------------------------------------------------------------- #
# Main execution function
# --------------------------------------------------------------------------- #

def execute_user_code(script_to_execute: str):
    """
    Execute a user-provided Python script in a restricted environment.
    
    Parameters:
        script_to_execute (str): The Python code to run.
    
    Returns:
        str or None: Captured stdout output if any; otherwise None.
    
    Raises:
        ValueError: If the script contains disallowed syntax or semantics,
                    or if it fails to compile.
    """
    # 1. Parse and validate the script
    try:
        parsed = ast.parse(script_to_execute, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user script: {e}") from None
    
    _validate_ast(parsed)

    # 2. Prepare a restricted execution environment
    safe_globals = {"__builtins__": ALLOWED_BUILTINS}
    local_vars = {}

    # 3. Capture stdout
    output_io = StringIO()
    try:
        with redirect_stdout(output_io):
            exec(compile(parsed, filename="<user_script>", mode="exec"),
                 safe_globals,
                 local_vars)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None

    output = output_io.getvalue()
    return output if output else None