import ast
import io
from contextlib import redirect_stdout

# --------------------------------------------------------------------------- #
# Safe AST visitor that rejects disallowed nodes and built‑in calls
# --------------------------------------------------------------------------- #

ALLOWED_NODES = {
    # Literals, expressions and operations
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.Return,
    ast.FunctionDef,
    ast.AsyncFunctionDef,
    ast.Lambda,
    ast.If,
    ast.For,
    ast.While,
    ast.Break,
    ast.Continue,
    ast.Pass,
    ast.Return,

    # Statements
    ast.Import,  # We'll reject these in the visitor
    ast.ImportFrom,

    # Expressions
    ast.Name,
    ast.Constant,
    ast.Num,  # for Python <3.8
    ast.Str,  # for Python <3.8
    ast.Bytes,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.NameConstant,

    # Operators
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,

    # Call
    ast.Call,

    # Subscript
    ast.Subscript,
    ast.Index,  # Python <3.9

    # Attribute access
    ast.Attribute,

    # Others that are generally safe
    ast.ListComp,
    ast.DictComp,
    ast.SetComp,
    ast.GeneratorExp,

    # Comprehension targets
    ast.comprehension,
}

# Disallowed names (builtins or special attributes)
DISALLOWED_NAMES = {
    "__import__",
    "eval",
    "exec",
    "open",
    "compile",
    "input",
    "__builtins__",
}

# Disallowed attribute names
DISALLOWED_ATTRS = {
    "__dict__",
    "__class__",
    "__bases__",
    "__globals__",
    "__code__",
    "__closure__",
    "__func__",
    "__self__",
}

class SafeVisitor(ast.NodeVisitor):
    def visit(self, node):
        if type(node) not in ALLOWED_NODES:
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        super().visit(node)

    def visit_Import(self, node):
        raise ValueError("Imports are not allowed")

    def visit_import_from(self, node):
        raise ValueError("Import from is not allowed")

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load) and node.id in DISALLOWED_NAMES:
            raise ValueError(f"Use of disallowed name: {node.id}")
        super().visit_Name(node)

    def visit_Attribute(self, node):
        if isinstance(node.ctx, ast.Load) and node.attr in DISALLOWED_ATTRS:
            raise ValueError(f"Access to disallowed attribute: {node.attr}")
        super().visit_Attribute(node)

    def visit_Call(self, node):
        # Prevent calls to disallowed built‑ins
        if isinstance(node.func, ast.Name) and node.func.id in DISALLOWED_NAMES:
            raise ValueError(f"Call to disallowed function: {node.func.id}")
        super().visit_Call(node)

# --------------------------------------------------------------------------- #
# Main execution function
# --------------------------------------------------------------------------- #

def process_code_input(code_input: str):
    """
    Execute a small Python code snippet safely.

    Parameters
    ----------
    code_input : str
        The code to run. It may contain multiple statements.

    Returns
    -------
    None or str
        None if there is no printed output, otherwise the captured stdout string.

    Raises
    ------
    ValueError
        If the code contains disallowed operations or syntax.
    """
    # 1. Parse and validate
    try:
        parsed = ast.parse(code_input, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code: {exc}") from None

    SafeVisitor().visit(parsed)

    # 2. Prepare a restricted execution environment
    safe_globals = {"__builtins__": None}
    # Provide minimal built‑in functions that are harmless
    safe_builtins = {
        "print": print,
        "len": len,
        "range": range,
        "abs": abs,
        "min": min,
        "max": max,
        "sum": sum,
    }
    safe_globals.update(safe_builtins)

    # 3. Capture stdout
    output = io.StringIO()
    try:
        with redirect_stdout(output):
            exec(compile(parsed, filename="<ast>", mode="exec"), safe_globals, {})
    except Exception as exc:
        # Re‑raise as ValueError to keep the API consistent
        raise ValueError(f"Execution error: {exc}") from None

    # 4. Return output if any
    result = output.getvalue()
    return result or None

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     code = """
# for i in range(3):
#     print(i)
# """
#     print(process_code_input(code))