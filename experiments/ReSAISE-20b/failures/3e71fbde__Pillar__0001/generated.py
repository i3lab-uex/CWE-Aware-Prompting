import ast
import sys
import io
from contextlib import redirect_stdout

# --------------------------------------------------------------------------- #
# Safe code execution – only simple expressions/statements are allowed.        #
# Disallowed constructs: imports, exec, eval, open, os.system, subprocess,   #
# attribute access (e.g. os.path), etc.                                      #
# --------------------------------------------------------------------------- #

DISALLOWED_NAMES = {
    "eval", "exec", "open",
    "os", "subprocess", "sys", "pathlib", "shutil", "socket",
    "compile", "input", "print",  # print is allowed; input not
}

DISALLOWED_ATTRS = {
    "system", "popen", "execfile",
}

class _SafeVisitor(ast.NodeVisitor):
    """AST visitor that raises ValueError on disallowed nodes."""
    def visit_Import(self, node):
        raise ValueError("Import statements are disallowed")
    def visit_ImportFrom(self, node):
        raise ValueError("Import statements are disallowed")
    def visit_Call(self, node):
        # Reject calls to disallowed functions
        if isinstance(node.func, ast.Name) and node.func.id in DISALLOWED_NAMES:
            raise ValueError(f"Call to disallowed function '{node.func.id}'")
        if isinstance(node.func, ast.Attribute):
            # e.g., os.system(...)
            attr_chain = []
            cur = node.func
            while isinstance(cur, ast.Attribute):
                attr_chain.append(cur.attr)
                cur = cur.value
            if isinstance(cur, ast.Name):
                attr_chain.append(cur.id)
            # Check for disallowed attribute chains
            if any(attr in DISALLOWED_ATTRS for attr in attr_chain):
                raise ValueError(f"Use of disallowed attribute chain: {'.'.join(reversed(attr_chain))}")
        self.generic_visit(node)
    def visit_Attribute(self, node):
        # Disallow attribute access in general (except for builtins like __name__)
        if isinstance(node.value, ast.Name) and node.attr.startswith('__'):
            # allow built-in dunder attributes like __name__
            return
        raise ValueError(f"Attribute access '{node.attr}' is disallowed")
    def visit_Name(self, node):
        # Disallow names that could be dangerous
        if node.id in DISALLOWED_NAMES:
            raise ValueError(f"Use of disallowed name '{node.id}'")
        self.generic_visit(node)
    def visit_Global(self, node):
        raise ValueError("Global statements are disallowed")
    def visit_Nonlocal(self, node):
        raise ValueError("Nonlocal statements are disallowed")

def run_code_snippet(snippet: str):
    """
    Execute a small Python code snippet in a sandboxed environment.
    
    Parameters
    ----------
    snippet : str
        Python code to run.

    Returns
    -------
    None or str
        The captured stdout output if any; otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations.
    """
    # 1. Parse the code to AST and check for forbidden nodes
    try:
        tree = ast.parse(snippet, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from None

    _SafeVisitor().visit(tree)

    # 2. Prepare restricted globals
    safe_globals = {
        "__builtins__": {k: v for k, v in __builtins__.__dict__.items()
                         if k in ("abs", "all", "any", "bool", "dict",
                                  "float", "int", "len", "list", "max",
                                  "min", "pow", "range", "str", "sum",
                                  "tuple", "zip")}
    safe_locals = {}

    # 3. Execute and capture output
    stdout_buffer = io.StringIO()
    try:
        with redirect_stdout(stdout_buffer):
            exec(compile(tree, filename="<snippet>", mode="exec"), safe_globals, safe_locals)
    except Exception as exc:
        # Re-raise with a clearer message
        raise ValueError(f"Execution error: {exc}") from None

    output = stdout_buffer.getvalue()
    return output if output else None