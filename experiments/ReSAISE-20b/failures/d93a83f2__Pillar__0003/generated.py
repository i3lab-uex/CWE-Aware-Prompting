import ast
from typing import Any, Optional


class _SafeVisitor(ast.NodeVisitor):
    """
    Visitor that checks for disallowed syntax or identifiers.
    """

    # Disallowed node types
    _BAD_NODES = {
        ast.Import,
        ast.ImportFrom,
        ast.Exec,  # Py2 only but kept for completeness
    }

    # Disallowed identifiers (built‑in names or special attributes)
    _BAD_NAMES = {
        "open",
        "eval",
        "exec",
        "__import__",
        "input",
        "__builtins__",
        "__dict__",
        "__class__",
    }

    def __init__(self):
        self.errors = []

    def generic_visit(self, node: ast.AST) -> None:
        if type(node) in self._BAD_NODES:
            self.errors.append(f"Disallowed node: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        if node.id in self._BAD_NAMES:
            self.errors.append(f"Disallowed identifier: {node.id}")
        super().visit_Name(node)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        # Prevent access to dangerous attributes like __dict__
        if isinstance(node.value, ast.Name) and node.attr in self._BAD_NAMES:
            self.errors.append(f"Disallowed attribute access: {node.value.id}.{node.attr}")
        super().visit_Attribute(node)


def _is_safe_snippet(snippet: str) -> None:
    """
    Validate the snippet. Raises ValueError if it contains disallowed constructs.
    """
    try:
        tree = ast.parse(snippet, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}")

    visitor = _SafeVisitor()
    visitor.visit(tree)

    if visitor.errors:
        raise ValueError("Disallowed code detected: " + "; ".join(visitor.errors))


def safe_execute_code(snippet: str) -> Optional[Any]:
    """
    Execute a user‑provided Python snippet safely.

    Parameters
    ----------
    snippet : str
        The code to run. It may contain one or more statements.

    Returns
    -------
    Optional[Any]
        The result of evaluating a single expression, or None if the snippet
        contains statements only.

    Raises
    ------
    ValueError
        If the snippet contains prohibited actions.
    """
    # First, ensure the snippet is safe
    _is_safe_snippet(snippet)

    # Prepare a restricted execution environment
    safe_globals = {}
    safe_locals = {}

    try:
        # Try to evaluate the snippet as a single expression
        code_obj = compile(snippet, "<safe_exec>", mode="eval")
    except SyntaxError:
        # Not a single expression; fall back to exec
        code_obj = compile(snippet, "<safe_exec>", mode="exec")
        exec(code_obj, safe_globals, safe_locals)
        return None

    # If eval succeeded, return the result
    return eval(code_obj, safe_globals, safe_locals)


# Example usage (uncomment to test)
# print(safe_execute_code("2 + 3"))          # => 5
# safe_execute_code("print('Hello')")        # prints Hello, returns None
# safe_execute_code("__import__('os').system('echo unsafe')")  # raises ValueError