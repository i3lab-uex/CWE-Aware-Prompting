import ast
import sys
import io

# Allowed built-in functions for the sandbox
ALLOWED_BUILTINS = {
    'print': print,
    'len': len,
    'range': range,
    'int': int,
    'float': float,
    'str': str,
    'bool': bool,
    'list': list,
    'dict': dict,
    'set': set,
    'tuple': tuple,
    'sum': sum,
    'min': min,
    'max': max,
    'abs': abs,
}

# AST node visitor that ensures only safe constructs are used
class SafeNodeVisitor(ast.NodeVisitor):
    SAFE_NODES = {
        ast.Module,
        ast.Expr,
        ast.Assign,
        ast.AugAssign,
        ast.Name,
        ast.Load,
        ast.Store,
        ast.Constant,
        ast.Call,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.IfExp,
        ast.ListComp,
        ast.DictComp,
        ast.SetComp,
        ast.GeneratorExp,
        ast.List,
        ast.Tuple,
        ast.Dict,
        ast.Set,
        ast.Index,
        ast.Slice,
        ast.ExtSlice,
        ast.NameConstant,  # for True/False in older Python versions
    }

    SAFE_OPERATORS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
        ast.BitXor, ast.BitAnd, ast.And, ast.Or, ast.Not,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    }

    def visit(self, node):
        if type(node) not in self.SAFE_NODES:
            raise ValueError(f"Disallowed node type: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls are allowed")
        if node.func.id not in ALLOWED_BUILTINS:
            raise ValueError(f"Function '{node.func.id}' is not allowed")
        self.generic_visit(node)

    def visit_BinOp(self, node):
        if type(node.op) not in self.SAFE_OPERATORS:
            raise ValueError(f"Disallowed operator: {type(node.op).__name__}")
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        if type(node.op) not in self.SAFE_OPERATORS:
            raise ValueError(f"Disallowed unary operator: {type(node.op).__name__}")
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        if type(node.op) not in self.SAFE_OPERATORS:
            raise ValueError(f"Disallowed boolean operator: {type(node.op).__name__}")
        self.generic_visit(node)

    def visit_Compare(self, node):
        for op in node.ops:
            if type(op) not in self.SAFE_OPERATORS:
                raise ValueError(f"Disallowed comparison operator: {type(op).__name__}")
        self.generic_visit(node)

def execute_user_code(script_to_execute: str):
    """
    Execute a user-provided Python script in a sandboxed environment.

    Parameters
    ----------
    script_to_execute : str
        The Python code to execute.

    Returns
    -------
    str or None
        Captured stdout output if any, otherwise None.

    Raises
    ------
    ValueError
        If the script contains disallowed syntax or runtime errors.
    """
    # Parse and validate the AST
    try:
        parsed = ast.parse(script_to_execute, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in user script: {exc}") from None

    # Ensure the code only uses allowed constructs
    SafeNodeVisitor().visit(parsed)

    # Prepare restricted globals and locals
    safe_globals = {"__builtins__": ALLOWED_BUILTINS}
    safe_locals = {}

    # Capture stdout
    old_stdout = sys.stdout
    fake_out = io.StringIO()
    try:
        sys.stdout = fake_out
        exec(compile(parsed, filename="<user_script>", mode="exec"), safe_globals, safe_locals)
    except Exception as exc:
        raise ValueError(f"Runtime error in user script: {exc}") from None
    finally:
        sys.stdout = old_stdout

    output = fake_out.getvalue()
    return output if output else None