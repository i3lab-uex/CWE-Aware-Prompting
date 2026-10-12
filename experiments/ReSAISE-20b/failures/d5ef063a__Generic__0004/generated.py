import ast
import sys
import io

# List of AST node types that are considered safe
SAFE_NODES = {
    ast.Module,
    ast.Expr,
    ast.Assign,
    ast.AugAssign,
    ast.Return,
    ast.BinOp,
    ast.UnaryOp,
    ast.BoolOp,
    ast.Compare,
    ast.If,
    ast.For,
    ast.While,
    ast.With,
    ast.FunctionDef,
    ast.Return,
    ast.Pass,
    ast.Break,
    ast.Continue,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Call,
    ast.Constant,
    ast.List,
    ast.Tuple,
    ast.Dict,
    ast.Set,
    ast.Subscript,
    ast.Index,
    ast.Slice,
    ast.Attribute,
}

# List of functions that are explicitly allowed
ALLOWED_FUNCS = {
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

class SafeVisitor(ast.NodeVisitor):
    def visit(self, node):
        if type(node) not in SAFE_NODES:
            raise ValueError(f"Prohibited node: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        # Ensure the function being called is allowed
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name not in ALLOWED_FUNCS:
                raise ValueError(f"Calling unapproved function '{func_name}'")
        elif isinstance(node.func, ast.Attribute):
            # e.g., obj.method() – disallow any attribute calls
            raise ValueError("Attribute calls are not allowed")
        else:
            raise ValueError(f"Unsupported call type: {type(node.func).__name__}")
        self.generic_visit(node)

    def visit_Import(self, node):
        raise ValueError("Import statements are not allowed")

    def visit_ImportFrom(self, node):
        raise ValueError("Import statements are not allowed")

    def visit_Exec(self, node):  # pragma: no cover
        raise ValueError("exec is not allowed")

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
        Captured standard output from the script, or None if nothing was printed.

    Raises
    ------
    ValueError
        If the script contains prohibited syntax or attempts disallowed operations.
    """
    # Syntax check and safety validation
    try:
        parsed = ast.parse(run_code, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user code: {exc}") from exc

    # Walk the AST to ensure only safe nodes are used
    SafeVisitor().visit(parsed)

    # Prepare a restricted execution environment
    safe_globals = {
        '__builtins__': None,  # Disable all built-ins
    }
    # Inject only the allowed functions
    for name in ALLOWED_FUNCS:
        safe_globals[name] = __builtins__[name]

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    try:
        sys.stdout = fake_out
        exec(compile(parsed, filename="<restricted>", mode="exec"), safe_globals, {})
    except Exception as exc:
        raise ValueError(f"Error during execution: {exc}") from exc
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None