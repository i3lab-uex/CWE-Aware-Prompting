import ast
import sys
from contextlib import redirect_stdout, suppress
from io import StringIO
from types import SimpleNamespace

# --------------------------------------------------------------------------- #
#  Safe execution of a Python code snippet with strict node filtering
# --------------------------------------------------------------------------- #

class _SafeNodeVisitor(ast.NodeVisitor):
    """
    Visitor that raises ValueError if a disallowed AST node or
    function call is encountered.
    """

    # Allowed node types – this list can be extended as needed
    _ALLOWED_NODES = {
        ast.Module, ast.Expr, ast.Assign,
        ast.Name, ast.Constant, ast.Load, ast.Store,
        ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare,
        ast.IfExp, ast.Call, ast.Attribute, ast.Subscript,
        ast.Index, ast.Slice, ast.List, ast.Tuple, ast.Dict,
        ast.Set, ast.Return, ast.Pass, ast.Break, ast.Continue,
        ast.For, ast.While, ast.If, ast.With, ast.Lambda,
        ast.FunctionDef, ast.arguments, ast.arg,
    }

    # Disallowed function names
    _DISALLOWED_FUNCS = {
        "open", "eval", "exec", "__import__", "compile",
    }

    # Disallowed import statements
    _DISALLOWED_IMPORTS = {ast.Import, ast.ImportFrom}

    def visit(self, node):
        if type(node) in self._DISALLOWED_IMPORTS:
            raise ValueError(f"Import statements are not allowed: {ast.dump(node)}")
        if type(node) not in self._ALLOWED_NODES:
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        # Check for disallowed function calls
        if isinstance(node.func, ast.Name) and node.func.id in self._DISALLOWED_FUNCS:
            raise ValueError(f"Function '{node.func.id}' is disallowed.")
        # Check for calls like __import__('module')
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in self._DISALLOWED_FUNCS:
                raise ValueError(f"Method '{node.func.attr}' is disallowed.")
        super().visit_Call(node)


def run_code_snippet(snippet: str):
    """
    Execute a Python code snippet safely.

    Parameters
    ----------
    snippet : str
        The Python source to run.

    Returns
    -------
    None | str
        If the snippet produces output on stdout, that output is returned as a string.
        Otherwise None is returned.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations or imports.
    """
    # Parse and validate AST
    try:
        tree = ast.parse(snippet, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}")

    _SafeNodeVisitor().visit(tree)

    # Prepare a sandboxed namespace
    sandbox = SimpleNamespace()
    globals_dict = {
        "__builtins__": {  # expose a minimal set of safe built-ins
            "abs": abs,
            "all": all,
            "any": any,
            "bool": bool,
            "chr": chr,
            "dict": dict,
            "float": float,
            "int": int,
            "len": len,
            "list": list,
            "max": max,
            "min": min,
            "pow": pow,
            "range": range,
            "round": round,
            "str": str,
            "tuple": tuple,
        }
    }

    # Capture stdout
    out = StringIO()
    with redirect_stdout(out):
        exec(compile(tree, filename="<snippet>", mode="exec"), globals_dict, sandbox.__dict__)

    output = out.getvalue()
    return output if output else None

# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Valid snippet
    code = """
a = 5
b = 10
print('Sum:', a + b)
"""
    print("Result:", run_code_snippet(code))

    # Invalid snippet – disallowed function
    bad = "open('file.txt', 'w')"
    try:
        run_code_snippet(bad)
    except ValueError as e:
        print("Caught error:", e)