import ast
import io
import sys

def restricted_run_code(run_code: str):
    """
    Execute a user-provided Python script in a sandboxed environment.

    Parameters
    ----------
    run_code : str
        The Python code to execute.

    Returns
    -------
    str or None
        Captured stdout output if any, otherwise None.

    Raises
    ------
    ValueError
        If the code contains prohibited operations or syntax errors.
    """

    # Define a whitelist of allowed AST node types
    ALLOWED_NODES = {
        ast.Module,
        ast.Expr,
        ast.Assign,
        ast.AugAssign,
        ast.Name,
        ast.Load,
        ast.Store,
        ast.Constant,
        ast.BinOp,
        ast.UnaryOp,
        ast.operator,   # base class for operators
        ast.unaryop,    # base class for unary ops
        ast.Call,
        ast.keyword,
        ast.Tuple,
        ast.List,
        ast.Dict,
        ast.Set,
        ast.IfExp,      # ternary expressions
    }

    # Allowed built-in functions
    ALLOWED_BUILTINS = {
        'print',
        'len',
        'range',
        'int',
        'float',
        'str',
        'bool',
        'list',
        'dict',
        'set',
        'tuple',
    }

    # Parse the code and validate
    try:
        parsed = ast.parse(run_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    # Visitor to enforce node restrictions
    class RestrictionVisitor(ast.NodeVisitor):
        def generic_visit(self, node):
            if type(node) not in ALLOWED_NODES:
                raise ValueError(f"Disallowed construct: {type(node).__name__}")
            super().generic_visit(node)

        def visit_Call(self, node: ast.Call):
            # Ensure function is a simple name and allowed
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only direct function calls are allowed")
            if node.func.id not in ALLOWED_BUILTINS:
                raise ValueError(f"Calling '{node.func.id}' is not allowed")
            super().generic_visit(node)

        def visit_Import(self, node):
            raise ValueError("Import statements are not allowed")

        def visit_ImportFrom(self, node):
            raise ValueError("Import statements are not allowed")

        def visit_Global(self, node):
            raise ValueError("Global keyword is not allowed")

        def visit_Nonlocal(self, node):
            raise ValueError("Nonlocal keyword is not allowed")

        def visit_ClassDef(self, node):
            raise ValueError("Class definitions are not allowed")

        def visit_FunctionDef(self, node):
            raise ValueError("Function definitions are not allowed")

    # Validate the AST
    RestrictionVisitor().visit(parsed)

    # Prepare a restricted globals dict
    safe_globals = {"__builtins__": {k: __builtins__[k] for k in ALLOWED_BUILTINS}}
    # Provide a simple print that writes to stdout
    safe_globals['print'] = print

    # Capture output
    stdout_capture = io.StringIO()
    try:
        original_stdout = sys.stdout
        sys.stdout = stdout_capture
        exec(compile(parsed, filename="<restricted>", mode="exec"), safe_globals, {})
    except Exception as exc:
        raise ValueError(f"Runtime error in user code: {exc}") from exc
    finally:
        sys.stdout = original_stdout

    output = stdout_capture.getvalue()
    return output if output else None