#!/usr/bin/env python3
"""
evaluate_code_string: execute a Python code snippet safely.

The function parses the input string into an AST and walks it to reject any
disallowed constructs such as imports, exec/eval calls, attribute access,
or other potentially dangerous operations.  If the code passes validation
it is executed in a sandboxed environment with an empty globals dictionary
and only a minimal set of safe built‑ins.  The function captures stdout and
returns either the captured text or None if there was no output.

Raises:
    ValueError: If the code contains disallowed syntax or operations.
"""

import ast
import io
import sys
from types import ModuleType

# Whitelist of safe built‑ins
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'dict': dict,
    'enumerate': enumerate,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'pow': pow,
    'range': range,
    'str': str,
    'sum': sum,
    # Add more safe built‑ins if needed
}

class DisallowedNodeVisitor(ast.NodeVisitor):
    """
    AST visitor that raises ValueError if a node representing a disallowed
    operation is encountered.
    """
    def visit_Import(self, node):
        raise ValueError("Imports are not allowed")

    def visit_ImportFrom(self, node):
        raise ValueError("Imports are not allowed")

    def visit_Call(self, node):
        # Disallow calls to __import__ or eval/exec
        if isinstance(node.func, ast.Name):
            if node.func.id in {"__import__", "eval", "exec"}:
                raise ValueError(f"Use of {node.func.id} is disallowed")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # Disallow attribute access that could reach dangerous objects
        if isinstance(node.value, ast.Name) and node.value.id in {"os", "sys", "__builtins__"}:
            raise ValueError(f"Attribute access on {node.value.id} is disallowed")
        self.generic_visit(node)

    def visit_Subscript(self, node):
        # Disallow subscript on modules or built‑ins
        if isinstance(node.value, ast.Name) and node.value.id in {"os", "sys", "__builtins__"}:
            raise ValueError(f"Subscript on {node.value.id} is disallowed")
        self.generic_visit(node)

    def visit_Name(self, node):
        # Disallow names that refer to dangerous globals
        if node.id in {"os", "sys", "__builtins__"}:
            raise ValueError(f"Use of {node.id} is disallowed")
        self.generic_visit(node)

def evaluate_code_string(code_string: str):
    """
    Execute a Python code snippet safely and return any printed output.

    Parameters
    ----------
    code_string : str
        The Python code to execute.

    Returns
    -------
    str | None
        Captured stdout text, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the code contains disallowed operations.
    """
    # Parse and validate AST
    try:
        tree = ast.parse(code_string, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code: {exc}") from None

    DisallowedNodeVisitor().visit(tree)

    # Prepare sandboxed globals
    sandbox_globals = {"__builtins__": SAFE_BUILTINS}
    sandbox_locals = {}

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    try:
        sys.stdout = fake_out
        exec(compile(tree, filename="<string>", mode="exec"), sandbox_globals, sandbox_locals)
    except Exception as exc:
        raise ValueError(f"Runtime error: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(evaluate_code_string("print('Hello, world!')"))