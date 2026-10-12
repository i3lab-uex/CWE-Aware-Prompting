import ast
import builtins
from typing import Any, Optional

# --------------------------------------------------------------------------- #
# Safety utilities
# --------------------------------------------------------------------------- #

class SafeNodeVisitor(ast.NodeVisitor):
    """
    Reject nodes that could perform dangerous operations.
    """

    # Allowed node types
    ALLOWED_NODES = {
        ast.Module,
        ast.Expr,
        ast.Load,
        ast.Store,
        ast.Name,
        ast.Constant,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Call,
        ast.keyword,
        ast.Attribute,
        ast.Subscript,
        ast.Index,
        ast.Slice,
        ast.ListComp,
        ast.DictComp,
        ast.SetComp,
        ast.GeneratorExp,
        ast.IfExp,
        ast.For,
        ast.While,
        ast.Return,
        ast.Assign,
        ast.AugAssign,
        ast.FunctionDef,
        ast.Lambda,
        ast.If,
        ast.With,
        ast.withitem,
        ast.Try,
        ast.ExceptHandler,
        ast.Import,
        ast.ImportFrom,
        ast.Pass,
        ast.Break,
        ast.Continue,
    }

    # Operations considered unsafe
    DISALLOWED_NAMES = {
        "__import__",
        "eval",
        "exec",
        "open",
        "compile",
        "__import__",
    }

    def visit_Name(self, node: ast.Name) -> None:
        if isinstance(node.ctx, ast.Load):
            if node.id in self.DISALLOWED_NAMES:
                raise ValueError(f"Use of forbidden name '{node.id}'")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        # Reject calls to disallowed functions
        if isinstance(node.func, ast.Name) and node.func.id in self.DISALLOWED_NAMES:
            raise ValueError(f"Call to forbidden function '{node.func.id}'")
        self.generic_visit(node)

    def generic_visit(self, node: ast.AST) -> None:
        if type(node) not in self.ALLOWED_NODES:
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        super().generic_visit(node)


def _validate_syntax(code: str) -> ast.Module:
    """
    Parse the code and run safety checks.
    Returns the parsed AST if safe, otherwise raises ValueError.
    """
    try:
        tree = ast.parse(code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code: {exc}") from exc

    SafeNodeVisitor().visit(tree)
    return tree


# --------------------------------------------------------------------------- #
# Execution utilities
# --------------------------------------------------------------------------- #

def _restricted_globals() -> dict:
    """
    Build a minimal, safe global namespace for execution.
    """
    allowed_builtins = {
        "print": print,
        "len": len,
        "range": range,
        "sum": sum,
        "min": min,
        "max": max,
        "abs": abs,
    }
    return {"__builtins__": allowed_builtins}


def _execute_tree(tree: ast.Module, globals_dict: dict) -> Any:
    """
    Execute the AST in a restricted environment and return the last
    evaluated expression, if any.
    """
    exec(compile(tree, filename="<user_code>", mode="exec"), globals_dict)

    # Try to find the value of the last expression
    for node in reversed(tree.body):
        if isinstance(node, ast.Expr):
            # Evaluate the expression in the same globals
            return eval(compile(ast.Expression(node.value), filename="<user_expr>", mode="eval"), globals_dict)
    return None


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def process_python_code(code_str: str) -> Optional[Any]:
    """
    Execute user-provided Python code in a safe, restricted environment.

    Parameters
    ----------
    code_str : str
        The Python source code to execute.

    Returns
    -------
    Optional[Any]
        The value produced by the last expression in the code, or None if
        no expression is present.

    Raises
    ------
    ValueError
        If the code contains syntax errors or attempts disallowed operations.
    """
    tree = _validate_syntax(code_str)
    globals_dict = _restricted_globals()
    return _execute_tree(tree, globals_dict)


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    code = """
a = 10
b = 20
print(a + b)
c = a * b
"""
    result = process_python_code(code)
    print("Result of last expression:", result)   # Should print 200