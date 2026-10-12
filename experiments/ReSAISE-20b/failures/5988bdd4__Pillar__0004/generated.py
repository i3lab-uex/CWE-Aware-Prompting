import ast
from typing import Any, Optional


# --------------------------------------------------------------------------- #
#  Safe snippet execution with strict AST validation
# --------------------------------------------------------------------------- #

class _SafeVisitor(ast.NodeVisitor):
    """
    Walk the AST and raise ValueError if forbidden nodes are found.
    Only a very small subset of Python is allowed:
        - literals, arithmetic/boolean ops
        - names referring to safe built‑ins (currently none)
        - simple assignments and return statements
    """
    SAFE_NODES = (
        ast.Module,
        ast.Expr,
        ast.Assign,
        ast.Return,
        ast.Name,
        ast.Constant,
        ast.Num,  # Python <3.8
        ast.Str,  # Python <3.8
        ast.Bytes,
        ast.Tuple,
        ast.List,
        ast.Dict,
        ast.Set,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.IfExp,
        ast.Lambda,
        ast.Call,  # but only for allowed functions
    )

    SAFE_FUNCS = {
        'abs', 'round', 'len',
        # add more if desired
    }

    def visit(self, node: ast.AST):
        if not isinstance(node, self.SAFE_NODES):
            raise ValueError(f"Forbidden syntax: {type(node).__name__}")
        super().visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            if node.func.id not in self.SAFE_FUNCS:
                raise ValueError(f"Call to forbidden function: {node.func.id}")
        else:
            # disallow attribute calls (e.g., os.system)
            raise ValueError("Attribute calls are forbidden")
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        raise ValueError("Imports are forbidden")

    def visit_ImportFrom(self, node: ast.ImportFrom):
        raise ValueError("Imports are forbidden")

    def visit_Exec(self, node: ast.Exec):
        raise ValueError("exec is forbidden")

    def visit_Global(self, node: ast.Global):
        raise ValueError("global statement is forbidden")

    def visit_Nonlocal(self, node: ast.Nonlocal):
        raise ValueError("nonlocal statement is forbidden")


def run_python_snippet(snippet_string: str) -> Optional[Any]:
    """
    Safely execute a short Python snippet.

    Parameters
    ----------
    snippet_string : str
        The user supplied code to run.  It may contain a single expression
        (e.g., "1+2") or simple statements.  Imports, function calls to
        disallowed functions, and any form of dynamic execution are not
        permitted.

    Returns
    -------
    Optional[Any]
        The value of the last expression if the snippet is an expression,
        otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains forbidden syntax or semantics.
    """
    if not isinstance(snippet_string, str):
        raise ValueError("Snippet must be a string")

    # Parse the code and validate
    try:
        tree = ast.parse(snippet_string, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Invalid Python code: {exc}") from None

    _SafeVisitor().visit(tree)

    # Prepare a very restricted global namespace
    safe_globals = {"__builtins__": {}}

    # If the snippet is a single expression, evaluate and return its value
    if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr):
        expr_node = tree.body[0].value
        try:
            code_obj = compile(ast.Expression(expr_node), '<string>', 'eval')
            return eval(code_obj, safe_globals)
        except Exception as exc:
            raise ValueError(f"Execution error: {exc}") from None

    # Otherwise, execute the statements (no return value)
    try:
        exec(compile(tree, '<string>', 'exec'), safe_globals)
    except Exception as exc:
        raise ValueError(f"Execution error: {exc}") from None

    return None