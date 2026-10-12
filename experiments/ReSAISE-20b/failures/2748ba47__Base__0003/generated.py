import ast
import io
import sys
from types import CodeType, FunctionType
from typing import Any

# ----------------------------------------------------------------------
# Whitelisted AST node types and functions
ALLOWED_NODE_TYPES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.IfExp,
    ast.Call,
    ast.Attribute,  # for built-in functions like print
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Subscript,
    ast.Index,
    ast.Slice,
    ast.NameConstant,  # for True/False
}

# Operators that are considered safe
ALLOWED_OPERATORS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitAnd,
    ast.BitXor,
    ast.UAdd,
    ast.USub,
}

# Allowed built-in functions
ALLOWED_BUILTINS = {
    'print',
    'len',
    'range',
    'sum',
    'min',
    'max',
    'abs',
    'round',
}

# ----------------------------------------------------------------------
def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively checks that all nodes in the AST are allowed.
    Raises ValueError if an illegal node is found.
    """
    if type(node) not in ALLOWED_NODE_TYPES:
        raise ValueError(f"Disallowed node type: {type(node).__name__}")

    # Operators
    if isinstance(node, ast.BinOp) and type(node.op) not in ALLOWED_OPERATORS:
        raise ValueError(f"Disallowed binary operator: {type(node.op).__name__}")
    if isinstance(node, ast.UnaryOp) and type(node.op) not in ALLOWED_OPERATORS:
        raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")

    # Function calls
    if isinstance(node, ast.Call):
        # disallow lambda expressions and other constructs
        if not isinstance(node.func, (ast.Name, ast.Attribute)):
            raise ValueError("Only simple function calls are allowed")
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
            # e.g., builtins.print
            if node.func.value.id == "__builtins__":
                func_name = node.func.attr

        if func_name and func_name not in ALLOWED_BUILTINS:
            raise ValueError(f"Function '{func_name}' is not allowed")

    # Recursively check child nodes
    for child in ast.iter_child_nodes(node):
        _is_safe_node(child)

# ----------------------------------------------------------------------
def execute_user_code(script_to_execute: str) -> Any:
    """
    Executes a user supplied Python script in a restricted environment.
    Only safe operations are allowed. Captures stdout and returns it as
    a string. Raises ValueError on syntax errors or prohibited actions.
    """
    # 1. Parse the script and perform safety checks
    try:
        parsed = ast.parse(script_to_execute, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in user script: {e}") from None

    _is_safe_node(parsed)

    # 2. Prepare a restricted global namespace
    safe_globals = {
        "__builtins__": {name: __builtins__[name] for name in ALLOWED_BUILTINS}
    }

    # 3. Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        # 4. Compile and execute
        code_obj: CodeType = compile(parsed, filename="<user_script>", mode="exec")
        exec(code_obj, safe_globals)
    except Exception as exc:
        raise ValueError(f"Runtime error in user script: {exc}") from None
    finally:
        sys.stdout = old_stdout

    # 5. Return captured output (or None if nothing was printed)
    output = fake_out.getvalue()
    return output or None