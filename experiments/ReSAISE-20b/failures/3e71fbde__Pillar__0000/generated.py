import ast
from types import ModuleType
from typing import Any

# List of disallowed names and modules
DISALLOWED_BUILTINS = {
    "eval",
    "exec",
    "open",
    "__import__",
    "compile",
    "input",  # avoid interactive input
}
DISALLOWED_MODULES = {
    "os",
    "sys",
    "subprocess",
    "shutil",
    "pickle",
    "marshal",
}

# Helper to detect disallowed nodes in the AST
class DisallowingVisitor(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            if alias.name.split(".")[0] in DISALLOWED_MODULES:
                self.errors.append(f"Import of module '{alias.name}' is disallowed")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module and node.module.split(".")[0] in DISALLOWED_MODULES:
            self.errors.append(f"Import from module '{node.module}' is disallowed")
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        # Detect calls to disallowed builtins
        if isinstance(node.func, ast.Name) and node.func.id in DISALLOWED_BUILTINS:
            self.errors.append(f"Call to built-in '{node.func.id}' is disallowed")
        # Detect calls like os.system, subprocess.Popen etc.
        if isinstance(node.func, ast.Attribute):
            value = node.func.value
            if isinstance(value, ast.Name) and value.id in DISALLOWED_MODULES:
                self.errors.append(f"Call to '{value.id}.{node.func.attr}' is disallowed")
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        # Detect usage of disallowed module attributes (e.g., os.system)
        if isinstance(node.value, ast.Name) and node.value.id in DISALLOWED_MODULES:
            self.errors.append(f"Access to '{node.value.id}.{node.attr}' is disallowed")
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if node.id in DISALLOWED_BUILTINS:
            self.errors.append(f"Use of built-in '{node.id}' is disallowed")
        self.generic_visit(node)


def run_code_snippet(snippet: str) -> Any:
    """
    Execute a small Python code snippet safely.

    Parameters
    ----------
    snippet : str
        The Python code to execute.

    Returns
    -------
    Any
        The value of the last expression in the snippet if it produces a result,
        otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations or imports.
    """
    # Parse the code into an AST
    try:
        tree = ast.parse(snippet, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}") from None

    # Walk the AST to detect disallowed constructs
    visitor = DisallowingVisitor()
    visitor.visit(tree)
    if visitor.errors:
        raise ValueError("Disallowed operation(s) detected:\n" + "\n".join(visitor.errors))

    # Prepare a minimal, safe global namespace
    safe_globals = {
        "__builtins__": {k: v for k, v in __builtins__.__dict__.items()
                         if k not in DISALLOWED_BUILTINS and k.isidentifier()}
    }

    # Capture the value of the last expression if any
    result = None

    # Compile and execute in a sandboxed module-like namespace
    try:
        code_obj = compile(tree, filename="<snippet>", mode="exec")
        exec(code_obj, safe_globals)
    except Exception as exc:
        raise ValueError(f"Runtime error while executing snippet: {exc}") from None

    # If the snippet contains a returnable expression, fetch it
    # (e.g., last line is an expression without semicolon)
    if tree.body:
        last_node = tree.body[-1]
        if isinstance(last_node, ast.Expr):
            # Evaluate the expression in the same safe namespace
            try:
                result = eval(compile(ast.Expression(last_node.value), filename="<expr>", mode="eval"),
                              safe_globals)
            except Exception as exc:
                raise ValueError(f"Failed to evaluate last expression: {exc}") from None

    return result