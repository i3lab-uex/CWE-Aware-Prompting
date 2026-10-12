import ast
import builtins
import io
import sys
from types import SimpleNamespace

# Disallowed AST node types and names
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,          # exec() in Python 2 (kept for completeness)
)

DISALLOWED_NAMES = {
    '__import__',
    'open',
    'eval',
    'exec',
    # any other dangerous built‑ins
}

class SafetyChecker(ast.NodeVisitor):
    """
    Walks an AST and raises ValueError if any disallowed construct is found.
    """

    def visit_Name(self, node: ast.Name):
        if node.id in DISALLOWED_NAMES:
            raise ValueError(f"Use of '{node.id}' is disallowed.")
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        raise ValueError("import statements are disallowed.")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        raise ValueError("import-from statements are disallowed.")

    def visit_Call(self, node: ast.Call):
        # Disallow calls to dangerous builtins via keyword args as well
        if isinstance(node.func, ast.Name) and node.func.id in DISALLOWED_NAMES:
            raise ValueError(f"Call to '{node.func.id}' is disallowed.")
        self.generic_visit(node)

    def generic_visit(self, node):
        if isinstance(node, DISALLOWED_NODES):
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        super().generic_visit(node)


def evaluate_code_string(code_string: str):
    """
    Execute a Python code snippet in a tightly controlled environment.

    Parameters
    ----------
    code_string : str
        The Python source to execute.

    Returns
    -------
    Any
        The result of the last expression if present; otherwise None.

    Raises
    ------
    ValueError
        If the code contains disallowed operations or constructs.
    """
    # 1. Syntax check & safety validation
    try:
        parsed = ast.parse(code_string, mode='exec')
    except SyntaxError as e:
        raise ValueError(f"Syntax error in code: {e}")

    SafetyChecker().visit(parsed)

    # 2. Prepare a sandboxed globals dictionary
    safe_builtins = {k: getattr(builtins, k) for k in (
        'abs', 'all', 'any', 'bool', 'bytes', 'chr',
        'complex', 'dict', 'float', 'int', 'len', 'list',
        'max', 'min', 'pow', 'range', 'round', 'set',
        'slice', 'str', 'sum', 'tuple', 'type'
    )}
    sandbox_globals = {
        '__builtins__': safe_builtins,
        # Provide a minimal math module
        'math': SimpleNamespace(
            sin=__import__('math').sin,
            cos=__import__('math').cos,
            sqrt=__import__('math').sqrt,
        ),
    }

    # 3. Capture stdout to detect prints
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    sys.stdout = fake_out

    try:
        # Execute the code
        exec(compile(parsed, '<string>', 'exec'), sandbox_globals)
    finally:
        sys.stdout = old_stdout

    # 4. Determine return value
    output_text = fake_out.getvalue()
    if output_text:
        # If the code produced printed output, return it
        return output_text.rstrip('\n')
    # If there is a variable named __result__ in the sandbox, return it
    if '__result__' in sandbox_globals:
        return sandbox_globals['__result__']
    # Otherwise, no meaningful output
    return None


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     print(evaluate_code_string("x = 2 + 3\n__result__ = x * 5"))
#     print(evaluate_code_string("print('Hello world')"))