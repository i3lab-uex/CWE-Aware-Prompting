import ast
import io
import sys
from typing import Optional

# A very small whitelist of safe built‑ins that the user code may call.
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
}

# Node types that are considered safe. Anything else will cause a ValueError.
SAFE_NODES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Call,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.Compare,
    ast.BoolOp,
    ast.And,
    ast.Or,
    ast.Not,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Mod,
    ast.Pow,
    ast.FloorDiv,
    ast.LShift,
    ast.RShift,
    ast.BitOr,
    ast.BitXor,
    ast.BitAnd,
    ast.USub,
    ast.UAdd,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.In,
    ast.NotIn,
    ast.Is,
    ast.IsNot,
    # literals and simple container types
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,
}

# Prohibited node types
PROHIBITED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # not present in py3 but keep for completeness
    ast.With,
    ast.AsyncWith,
    ast.Lambda,
    ast.FunctionDef,
    ast.ClassDef,
    ast.For,
    ast.While,
    ast.Try,
    ast.Return,
    ast.Raise,
    ast.Global,
    ast.Nonlocal,
    ast.Delete,
    ast.Pass,
    ast.Break,
    ast.Continue,
}


def _check_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and ensure that only safe nodes are present.
    Raises ValueError if a prohibited node or an unknown node is encountered.
    """
    for child in ast.iter_child_nodes(node):
        if type(child) in PROHIBITED_NODES:
            raise ValueError(f"Prohibited operation detected: {type(child).__name__}")
        if type(child) not in SAFE_NODES:
            raise ValueError(f"Unsafe construct detected: {type(child).__name__}")
        _check_ast(child)


def restricted_run_code(run_code: str) -> Optional[str]:
    """
    Execute a user supplied Python script in a restricted environment.
    
    Parameters
    ----------
    run_code : str
        The Python code to execute.

    Returns
    -------
    Optional[str]
        Captured stdout if the script produced output; otherwise None.

    Raises
    ------
    ValueError
        If the code contains prohibited operations or is syntactically invalid.
    """
    # Parse the source and validate the AST
    try:
        parsed = ast.parse(run_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from None

    _check_ast(parsed)

    # Prepare a minimal global namespace
    safe_globals = {'__builtins__': SAFE_BUILTINS}

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    try:
        sys.stdout = fake_out
        exec(compile(parsed, filename='<restricted>', mode='exec'), safe_globals, {})
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None