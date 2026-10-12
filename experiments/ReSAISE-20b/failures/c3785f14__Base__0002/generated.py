import ast
import io
import sys
from types import ModuleType, FunctionType
from typing import Any

# --------------------------------------------------------------------------- #
#  Safe execution helper
# --------------------------------------------------------------------------- #

class _DisallowedUsageError(ValueError):
    """Raised when the supplied code contains disallowed constructs."""


class _CodeSafetyChecker(ast.NodeVisitor):
    """
    AST visitor that ensures the code does not use dangerous constructs.
    """

    # Names of builtins we want to forbid
    _FORBIDDEN_BUILTINS = {
        "eval",
        "exec",
        "compile",
        "open",
        "input",
        "__import__",
    }

    # Nodes that are outright forbidden
    _FORBIDDEN_NODES = {
        ast.Import,
        ast.ImportFrom,
        ast.Call,  # Calls are inspected more closely
    }

    def __init__(self):
        self._issues = []

    def visit(self, node: ast.AST) -> Any:
        # Check for forbidden nodes first
        if type(node) in self._FORBIDDEN_NODES:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                self._issues.append(
                    f"Import statements are disallowed: {ast.dump(node)}"
                )
            elif isinstance(node, ast.Call):
                self._check_call(node)
        return super().visit(node)

    def _check_call(self, node: ast.Call) -> None:
        """
        Inspect a Call node for forbidden builtins or attribute usage.
        """
        # Check if the call is to a builtin function
        func_name = None

        # Function may be an attribute or name
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(
            node.func,
            ast.Attribute,
        ) and isinstance(node.func.value, ast.Name) and node.func.value.id == "__builtins__":
            func_name = node.func.attr

        if func_name in self._FORBIDDEN_BUILTINS:
            self._issues.append(
                f"Use of disallowed builtin '{func_name}' in call at line {node.lineno}"
            )

        # Disallow any attribute access that might reach dangerous functions
        if isinstance(node.func, ast.Attribute):
            self._check_attribute(node.func)

    def _check_attribute(self, attr: ast.Attribute) -> None:
        """
        Recursively check attribute chains for dangerous objects.
        """
        # If we reach __import__ or any builtin via attributes
        if (
            isinstance(attr.value, ast.Name)
            and attr.value.id == "__builtins__"
            and attr.attr in self._FORBIDDEN_BUILTINS
        ):
            self._issues.append(
                f"Access to forbidden attribute '{attr.attr}' via __builtins__"
            )
        # Recurse if nested
        if isinstance(attr.value, ast.Attribute):
            self._check_attribute(attr.value)

    def has_issues(self) -> bool:
        return len(self._issues) > 0

    def report(self) -> str:
        return "\n".join(self._issues)


# --------------------------------------------------------------------------- #
#  Main API
# --------------------------------------------------------------------------- #

def evaluate_code_string(code_string: str) -> Any:
    """
    Execute a small Python snippet safely.

    Parameters
    ----------
    code_string : str
        The Python source to execute. May contain any valid statements,
        but imports, eval/exec, open/input, and other dangerous
        operations are disallowed.

    Returns
    -------
    None or str
        If the code produces no printed output, returns ``None``.
        Otherwise, returns the captured standard‑output as a string.

    Raises
    ------
    ValueError
        If the code contains disallowed operations or syntax errors.
    """
    # 1. Parse and validate the AST
    try:
        tree = ast.parse(code_string, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code: {exc}") from exc

    checker = _CodeSafetyChecker()
    checker.visit(tree)

    if checker.has_issues():
        raise ValueError(f"Disallowed code detected:\n{checker.report()}")

    # 2. Prepare a restricted execution environment
    safe_globals = {
        "__builtins__": {
            # expose only a minimal, safe subset of builtins
            "print": print,
            "len": len,
            "range": range,
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "dict": dict,
            "list": list,
            "set": set,
            "tuple": tuple,
            "sum": sum,
            # Add more safe builtins if needed
        }
    }

    # 3. Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        exec(compile(tree, filename="<string>", mode="exec"), safe_globals, {})
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return None if not output.strip() else output


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Safe snippet
    print(evaluate_code_string("print('Hello, world!')"))

    # Unsafe snippet (will raise ValueError)
    try:
        evaluate_code_string("import os\nprint(os.listdir('.'))")
    except ValueError as e:
        print(f"Caught error: {e}")