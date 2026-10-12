#!/usr/bin/env python3
"""
Safe execution of user supplied Python scripts.

The function `execute_user_script` parses the submitted script,
ensures that only a minimal set of safe AST nodes are used, and
executes it in an isolated environment that lacks access to the
standard library, built‑ins and any other dangerous objects.
"""

import ast
import sys
from io import StringIO

# ----------------------------------------------------------------------
# 1. Whitelisted AST node types (safe to use)
# ----------------------------------------------------------------------
SAFE_NODES = {
    # Expressions
    ast.Module,
    ast.Expr,
    ast.Load,
    ast.Store,
    ast.Name,
    ast.Constant,          # literals (int/float/str/... )
    ast.Str,               # legacy string literal
    ast.Num,
    ast.Tuple,
    ast.List,
    ast.Dict,
    ast.Set,

    # Operations
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.Call,

    # Binary operators
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
    ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
    ast.BitXor, ast.BitAnd,

    # Unary operators
    ast.UAdd, ast.USub, ast.Not, ast.Invert,

    # Boolean operators
    ast.And, ast.Or,

    # Comparison operators
    ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    ast.Is, ast.IsNot, ast.In, ast.NotIn,

    # Function call nodes
    ast.Call,
    ast.Attribute,

    # Control flow (limited)
    ast.If, ast.For, ast.While,
    ast.Compare,
}

# ----------------------------------------------------------------------
# 2. Whitelisted function names that may be called by the user
#    (e.g., print, len, sum)
ALLOWED_BUILTINS = {
    "print",
    "len",
    "sum",
    "min",
    "max",
    "abs",
    "round",
    "sorted",
}

# ----------------------------------------------------------------------
# 3. Visitor that checks the AST for disallowed nodes
# ----------------------------------------------------------------------
class SafeVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.errors = []

    def generic_visit(self, node):
        if type(node) not in SAFE_NODES:
            self.errors.append(f"Disallowed node: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node):
        # Disallow calls to __import__ or other dangerous built-ins
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in ALLOWED_BUILTINS:
                self.errors.append(f"Disallowed function call: {func_name}")
        elif isinstance(node.func, ast.Attribute):
            # e.g., os.system -> disallow
            self.errors.append(f"Disallowed attribute call: {ast.unparse(node.func)}")
        super().generic_visit(node)

    def visit_Import(self, node):
        self.errors.append("Imports are disallowed")

    def visit_ImportFrom(self, node):
        self.errors.append("Imports are disallowed")


def execute_user_script(submitted_script: str) -> object:
    """
    Execute a user supplied Python script in a sandboxed environment.

    Parameters
    ----------
    submitted_script : str
        The Python code to execute.

    Returns
    -------
    object
        The captured stdout output as a string, or None if no output.

    Raises
    ------
    ValueError
        If the script contains syntax errors or disallowed operations.
    """
    # 1. Parse the script
    try:
        tree = ast.parse(submitted_script, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from exc

    # 2. Validate the AST
    visitor = SafeVisitor()
    visitor.visit(tree)
    if visitor.errors:
        raise ValueError("User script contains forbidden operations: " +
                         "; ".join(visitor.errors))

    # 3. Prepare the execution environment
    safe_globals = {"__builtins__": {}}
    # Inject allowed built-ins
    for name in ALLOWED_BUILTINS:
        safe_globals[name] = __builtins__[name]

    # 4. Capture stdout
    old_stdout = sys.stdout
    fake_out = StringIO()
    sys.stdout = fake_out

    try:
        exec(compile(tree, filename="<user_script>", mode="exec"),
             safe_globals,
             {})
    except Exception as exc:
        raise ValueError(f"Error during script execution: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None