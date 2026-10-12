import ast

class SafeEvalVisitor(ast.NodeVisitor):
    """
    Visitor that ensures the AST contains only safe nodes.
    Allowed nodes:
        - Module, Expr, Expression
        - BinOp (+,-,* ,/, //, %, **)
        - UnaryOp (+,-)
        - BoolOp (and/or)
        - Compare (<, <=, >, >=, ==, !=)
        - Constant (numbers, strings, booleans, None)
    All other nodes are considered unsafe.
    """
    SAFE_NODES = {
        ast.Module,
        ast.Expr,
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.BoolOp,
        ast.Compare,
        ast.Constant,          # Python 3.8+
        ast.Num,               # older versions
        ast.Str,
        ast.NameConstant,
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow,
        ast.UAdd, ast.USub,
        ast.And, ast.Or,
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE,
    }

    def generic_visit(self, node):
        if type(node) not in self.SAFE_NODES:
            raise ValueError(f"Unsafe node detected: {type(node).__name__}")
        super().generic_visit(node)

def run_user_code(python_code: str) -> str:
    """
    Safely evaluate a small user-supplied Python script.
    Only basic arithmetic and boolean operations are allowed.
    Any disallowed construct results in 'Execution Blocked!'.
    """
    try:
        # Parse the code into an AST
        tree = ast.parse(python_code, mode='exec')

        # Ensure the code is safe
        SafeEvalVisitor().visit(tree)

        # Prepare a minimal execution environment
        safe_globals = {}
        safe_locals = {}

        # If the code is a single expression, use eval
        if len(tree.body) == 1 and isinstance(tree.body[0], ast.Expr):
            result = eval(compile(tree, filename="<user>", mode="eval"),
                          safe_globals, safe_locals)
        else:
            # Execute statements; result is None unless explicitly returned
            exec(compile(tree, filename="<user>", mode="exec"),
                 safe_globals, safe_locals)
            result = None

        return str(result) if result is not None else "None"
    except Exception:
        # Any error or detection of unsafe code leads to blocking
        return "Execution Blocked!"