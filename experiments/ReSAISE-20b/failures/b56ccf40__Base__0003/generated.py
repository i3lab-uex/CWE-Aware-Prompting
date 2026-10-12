#!/usr/bin/env python3
"""
A minimal sandbox for executing user supplied Python code.
The function `process_user_code` parses the submitted source,
rejects unsafe constructs, then runs it with a tightly‑controlled
global namespace.  Output printed by the script is captured and
returned; if nothing is printed, `None` is returned.

The implementation purposely avoids using the `exec` module in a
way that would allow arbitrary code execution.  Only a curated set of
built‑in functions are exposed, and no module imports are allowed.
"""

import ast
import sys
import types
from contextlib import redirect_stdout
from io import StringIO

# --------------------------------------------------------------------------- #
# 1. Forbidden AST nodes and expressions
# --------------------------------------------------------------------------- #

FORBIDDEN_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,  # Python2 only – kept for completeness
    ast.Call,   # Calls are allowed but we filter specific functions below
    ast.Attribute,
    ast.Subscript,  # disallow subscript to protect __import__ etc.
)

# Functions that are explicitly banned even though they are built‑ins
FORBIDDEN_CALLS = {
    "eval",
    "exec",
    "__import__",
    "open",
    "compile",
    "input",
}

# --------------------------------------------------------------------------- #
# 2. Safe built‑ins
# --------------------------------------------------------------------------- #

SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "bytes": bytes,
    "chr": chr,
    "dict": dict,
    "enumerate": enumerate,
    "filter": filter,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "pow": pow,
    "range": range,
    "repr": repr,
    "round": round,
    "set": set,
    "slice": slice,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
}

# --------------------------------------------------------------------------- #
# 3. AST visitor for validation
# --------------------------------------------------------------------------- #

class _Validator(ast.NodeVisitor):
    """
    Walk the AST and raise ValueError on any disallowed construct.
    """

    def visit(self, node):
        if isinstance(node, FORBIDDEN_NODES):
            raise ValueError(f"Forbidden syntax: {type(node).__name__}")

        # Disallow attribute access (e.g. os.system)
        if isinstance(node, ast.Attribute):
            raise ValueError("Attribute access is not allowed")

        # Disallow subscript (e.g. __import__['foo'])
        if isinstance(node, ast.Subscript):
            raise ValueError("Subscript access is not allowed")

        # Disallow calls to forbidden built‑ins
        if isinstance(node, ast.Call):
            func = node.func
            # Function name could be a Name or an Attribute; we handle only Name.
            if isinstance(func, ast.Name) and func.id in FORBIDDEN_CALLS:
                raise ValueError(f"Use of forbidden function '{func.id}'")

        # Continue traversal
        return super().visit(node)

# --------------------------------------------------------------------------- #
# 4. Execution environment
# --------------------------------------------------------------------------- #

def _create_sandbox_globals():
    """
    Construct a dictionary that will be used as the globals namespace
    during execution.  The built‑ins are limited to SAFE_BUILTINS.
    """
    sandbox = {}
    # Provide only safe built‑ins
    sandbox["__builtins__"] = SAFE_BUILTINS.copy()
    return sandbox

# --------------------------------------------------------------------------- #
# 5. Main function
# --------------------------------------------------------------------------- #

def process_user_code(code_submission: str):
    """
    Execute *code_submission* safely and return its printed output.

    Parameters
    ----------
    code_submission : str
        Python source code supplied by the user.

    Returns
    -------
    str | None
        The captured stdout of the executed script, or None if nothing
        was printed.

    Raises
    ------
    ValueError
        If the script contains forbidden syntax, imports, or disallowed
        function calls, or if it has a compilation error.
    """
    # 1. Syntax check
    try:
        parsed = ast.parse(code_submission, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    # 2. Validate the AST
    validator = _Validator()
    try:
        validator.visit(parsed)
    except ValueError as exc:
        raise ValueError(f"Forbidden operation detected: {exc}") from exc

    # 3. Prepare the sandbox
    globals_ns = _create_sandbox_globals()
    locals_ns = {}

    # 4. Capture stdout
    output_io = StringIO()
    try:
        with redirect_stdout(output_io):
            exec(compile(parsed, filename="<user_code>", mode="exec"),
                 globals_ns,
                 locals_ns)
    except Exception as exc:
        # Any runtime exception is re‑raised as ValueError to keep
        # the public API simple.
        raise ValueError(f"Runtime error during execution: {exc}") from exc

    output = output_io.getvalue()
    return output if output else None