import ast
import builtins
from typing import Any, Optional

# Whitelist of safe built‑in functions / types that students can use
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "pow": pow,
    "range": range,
    "round": round,
    "str": str,
    "sum": sum,
    "tuple": tuple,
}

# List of AST node types that are disallowed in the snippet
PROHIBITED_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # Python 2 only – kept for completeness
    ast.Call,         # Calls to disallowed builtins will be caught by name check
    ast.Attribute,
    ast.Subscript,
    ast.Lambda,
    ast.FunctionDef,
    ast.ClassDef,
    ast.With,
    ast.Try,
    ast.AsyncFunctionDef,
    ast.Await,
    ast.Yield,
    ast.YieldFrom,
    ast.FormattedValue,  # f-strings that could evaluate expressions
}

class SafeCodeVisitor(ast.NodeVisitor):
    """Walk the AST and raise ValueError on disallowed constructs."""
    def visit(self, node):
        if isinstance(node, tuple(PROHIBITED_NODES)):
            raise ValueError(f"Disallowed statement: {type(node).__name__}")
        # Disallow any function calls that are not in SAFE_BUILTINS
        if isinstance(node, ast.Call):
            func = node.func
            # Allow calls to safe builtins only
            if isinstance(func, ast.Name):
                if func.id not in SAFE_BUILTINS:
                    raise ValueError(f"Use of disallowed function '{func.id}'")
            else:
                # Any other call form (e.g., attribute or lambda) is disallowed
                raise ValueError("Only direct calls to whitelisted builtins are allowed")
        self.generic_visit(node)

def safe_execute_code(snippet: str) -> Optional[Any]:
    """
    Execute a user supplied snippet in a restricted environment.

    Parameters
    ----------
    snippet : str
        The code to run.  It may be a single expression or a block of statements.

    Returns
    -------
    Optional[Any]
        The value of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains prohibited syntax or disallowed operations.
    """
    # Parse to AST and validate
    try:
        parsed = ast.parse(snippet, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}") from None

    SafeCodeVisitor().visit(parsed)

    # Prepare a minimal global namespace
    exec_globals = {"__builtins__": SAFE_BUILTINS}
    exec_locals: dict[str, Any] = {}

    # Determine if the last node is an expression
    if parsed.body and isinstance(parsed.body[-1], ast.Expr):
        # Evaluate the last expression separately
        expr_code = compile(ast.Module([parsed.body[-1]], type_ignores=[]), "<string>", "eval")
        # Execute all preceding statements
        if len(parsed.body) > 1:
            exec(compile(ast.Module(parsed.body[:-1], type_ignores=[]), "<string>", "exec"),
                 exec_globals, exec_locals)
        return eval(expr_code, exec_globals, exec_locals)

    # No expression at the end – just execute all
    exec(compile(parsed, "<string>", "exec"), exec_globals, exec_locals)
    return None