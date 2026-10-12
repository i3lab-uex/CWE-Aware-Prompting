# Safe execution of user supplied Python snippets.
#
# The function parses the code with `ast` and rejects any
# construct that could lead to unsafe behaviour (imports,
# exec/eval calls, attribute access to dangerous modules,
# etc.).  Only a very small set of built‑ins is made
# available and the snippet runs in an empty global scope.
#
# Any output printed by the snippet is captured and returned
# as a string.  If there is no output, `None` is returned.
#
# The implementation follows the guidance for CWE‑94
# by performing a static analysis before executing the code.

import ast
import sys
from types import ModuleType
from contextlib import redirect_stdout
from io import StringIO


# Allowed built‑ins – we expose only safe helpers.
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
    "sum": sum,
    "min": min,
    "max": max,
    "abs": abs,
    # Add more as needed
}


class _ForbiddenNodeVisitor(ast.NodeVisitor):
    """
    Visits AST nodes and raises ValueError if any forbidden
    construct is encountered.
    """

    def __init__(self):
        super().__init__()
        self.forbidden = [
            ast.Import,
            ast.ImportFrom,
            ast.Call,          # we will inspect calls separately
            ast.Attribute,     # disallow attribute access to dangerous modules
            ast.Exec,          # Python 2 legacy – kept for completeness
        ]

    def generic_visit(self, node):
        # Reject any node types that are explicitly forbidden
        if isinstance(node, tuple(self.forbidden)):
            raise ValueError(f"Forbidden construct: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # Disallow calls to eval/exec or any built‑in that can run code
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in ("eval", "exec"):
                raise ValueError(f"Disallowed function call: {func_name}")
        # Disallow calls to os.system, subprocess.Popen etc.
        if isinstance(node.func, ast.Attribute):
            attr_chain = self._get_attribute_chain(node.func)
            if "os" in attr_chain or "subprocess" in attr_chain:
                raise ValueError(f"Disallowed system call: {'.'.join(attr_chain)}")
        super().generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        # Disallow attribute access that could reach dangerous modules
        if isinstance(node.value, ast.Name):
            if node.value.id in ("os", "subprocess", "__import__"):
                raise ValueError(f"Disallowed attribute access: {node.value.id}.{node.attr}")
        super().generic_visit(node)

    def _get_attribute_chain(self, node):
        """Return the dotted chain of attribute names."""
        parts = []
        while isinstance(node, ast.Attribute):
            parts.insert(0, node.attr)
            node = node.value
        if isinstance(node, ast.Name):
            parts.insert(0, node.id)
        return parts


def execute_python_code(snippet_code: str):
    """
    Execute a user supplied Python snippet safely.

    Parameters
    ----------
    snippet_code : str
        The code to run. Must not contain imports, eval/exec or other
        potentially dangerous operations.

    Returns
    -------
    str | None
        The captured stdout output, or `None` if nothing was printed.

    Raises
    ------
    ValueError
        If the code contains forbidden constructs or is syntactically invalid.
    """
    # 1. Parse and statically analyse the code
    try:
        parsed = ast.parse(snippet_code, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from exc

    visitor = _ForbiddenNodeVisitor()
    visitor.visit(parsed)

    # 2. Prepare the execution environment
    exec_globals = {"__builtins__": SAFE_BUILTINS}
    exec_locals = {}

    # 3. Execute while capturing stdout
    output_stream = StringIO()
    try:
        with redirect_stdout(output_stream):
            exec(compile(parsed, filename="<user_snippet>", mode="exec"),
                 exec_globals,
                 exec_locals)
    except Exception as exc:
        # Re‑raise as ValueError to keep the API consistent
        raise ValueError(f"Execution error: {exc}") from exc

    # 4. Return captured output if any
    result = output_stream.getvalue()
    return result if result else None