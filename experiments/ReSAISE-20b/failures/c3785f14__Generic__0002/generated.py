import ast
import sys
from contextlib import redirect_stdout
from io import StringIO
from typing import Any, Optional

# Set of safe built‑in functions that can be called from the code
SAFE_BUILTINS = {
    "print": print,
    "len": len,
    "range": range,
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
}

# Allowed AST node types
ALLOWED_NODES = (
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.Name,
    ast.Constant,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.IfExp,
    ast.Call,
    ast.Attribute,
    ast.Subscript,
    ast.Index,
    ast.Slice,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Load,
    ast.Store,
    ast.Del,
)

class CodeSafetyVisitor(ast.NodeVisitor):
    def visit(self, node: ast.AST) -> Any:
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        return super().visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        # Only allow calls to whitelisted built‑ins or user defined functions
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in SAFE_BUILTINS:
                raise ValueError(f"Call to disallowed function: {func_name}")
        elif isinstance(node.func, ast.Attribute):
            # Prevent attribute access like __import__ or os.system
            if node.func.attr.startswith("__"):
                raise ValueError(f"Disallowed attribute call: {node.func.attr}")
        else:
            # Other call types are disallowed
            raise ValueError("Disallowed function call type")
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> Any:
        if isinstance(node.ctx, ast.Load):
            # Prevent use of dangerous built‑ins like eval or exec
            if node.id in {"eval", "exec", "__import__", "open"}:
                raise ValueError(f"Use of disallowed name: {node.id}")
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> Any:
        raise ValueError("Imports are disallowed")

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        raise ValueError("Imports are disallowed")

def evaluate_code_string(code_string: str) -> Optional[Any]:
    """
    Execute a small Python code snippet safely.

    Parameters
    ----------
    code_string : str
        The code to execute.

    Returns
    -------
    Optional[Any]
        None if the code produced no output, otherwise a string containing
        whatever was printed. If the snippet is a single expression, its
        value is returned instead.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # Parse the code and perform a safety check
    try:
        parsed = ast.parse(code_string, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code: {exc}") from exc

    CodeSafetyVisitor().visit(parsed)

    # Prepare restricted globals
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    local_vars: dict[str, Any] = {}

    # If the code is a single expression, evaluate it
    if len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr):
        expr_node = parsed.body[0].value
        # Compile as expression and evaluate
        compiled_expr = compile(ast.Expression(expr_node), "<string>", "eval")
        try:
            result = eval(compiled_expr, safe_globals, local_vars)
            return result
        except Exception as exc:
            raise ValueError(f"Error during evaluation: {exc}") from exc

    # Otherwise execute the code and capture stdout
    stdout_capture = StringIO()
    try:
        with redirect_stdout(stdout_capture):
            exec(compile(parsed, "<string>", "exec"), safe_globals, local_vars)
    except Exception as exc:
        raise ValueError(f"Error during execution: {exc}") from exc

    output = stdout_capture.getvalue()
    return output if output else None