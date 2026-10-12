import ast
import io
import sys
from types import ModuleType

# List of AST node types that are considered safe.
SAFE_NODES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.Return,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.ClassDef,
    ast.arguments,
    ast.arg,
    ast.Name,
    ast.Constant,
    ast.Num,          # for Python <3.8
    ast.Str,          # for Python <3.8
    ast.Bytes,        # for Python <3.8
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.NameConstant, # for Python <3.8
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.Call,
    ast.Attribute,
    ast.Subscript,
    ast.Index,        # for Python <3.9
    ast.Slice,
    ast.ExtSlice,
    ast.comprehension,
    # Operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitXor, ast.BitAnd, ast.Invert, ast.Not,
    ast.And, ast.Or,
    # Comparators
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    # Others
    ast.Pass,
    ast.Break,
    ast.Continue,
    ast.For,
    ast.While,
    ast.If,
    ast.With,
    ast.Raise,
    ast.Try,
    ast.ExceptHandler,
}

# Disallowed node types
DISALLOWED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # Python 2
    ast.Global,
    ast.Nonlocal,
}

class SafeVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        if type(node) in DISALLOWED_NODES:
            raise ValueError(f"Disallowed operation: {type(node).__name__}")
        if type(node) not in SAFE_NODES:
            # Allow certain simple expression nodes implicitly
            raise ValueError(f"Disallowed syntax: {type(node).__name__}")
        super().generic_visit(node)

def evaluate_code_string(code_string: str):
    """
    Execute a Python code snippet safely.

    Parameters
    ----------
    code_string : str
        The Python source code to execute.

    Returns
    -------
    str | None
        Captured stdout output if any; otherwise None.

    Raises
    ------
    ValueError
        If the code contains disallowed operations or syntax.
    """
    # 1. Parse and validate AST
    try:
        tree = ast.parse(code_string, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}") from None

    SafeVisitor().visit(tree)

    # 2. Prepare a restricted execution environment
    safe_globals = {
        "__builtins__": {
            # Expose only a minimal subset of built-ins
            "abs": abs,
            "all": all,
            "any": any,
            "bool": bool,
            "dict": dict,
            "float": float,
            "int": int,
            "len": len,
            "list": list,
            "max": max,
            "min": min,
            "print": print,   # we capture output below
            "range": range,
            "str": str,
            "sum": sum,
        }
    }

    # 3. Capture stdout
    old_stdout = sys.stdout
    out_buffer = io.StringIO()
    try:
        sys.stdout = out_buffer
        exec(compile(tree, filename="<string>", mode="exec"), safe_globals)
    finally:
        sys.stdout = old_stdout

    output = out_buffer.getvalue()
    return output if output else None