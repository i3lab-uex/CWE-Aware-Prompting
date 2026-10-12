import ast
import math

def evaluate_user_code(code_string: str) -> str:
    """
    Safely evaluates a Python expression provided as a string.

    The function parses the input using `ast.parse` and allows only a
    restricted set of node types:
        - Literals (int, float, complex)
        - Unary and binary arithmetic operations
        - Function calls to whitelisted math functions (`math.*`)
        - Constants from the `math` module (e.g., `pi`, `e`)

    Any other construct results in an "Unsafe Code Detected!" message.
    """
    # Allowed math functions and constants
    allowed_names = {name for name in dir(math) if not name.startswith("_")}
    # Build a safe globals dictionary
    safe_globals = {"__builtins__": None, "math": math}
    for name in allowed_names:
        safe_globals[name] = getattr(math, name)

    # Node visitor to reject disallowed nodes
    class SafeVisitor(ast.NodeVisitor):
        def visit(self, node):
            if isinstance(node, (ast.Module, ast.Expr)):
                super().visit(node)
            elif isinstance(node, ast.Expression):
                self.visit(node.body)
            else:
                # Reject any node that is not explicitly allowed
                raise ValueError(f"Disallowed node: {type(node).__name__}")

        def visit_BinOp(self, node):
            self.visit(node.left)
            self.visit(node.right)

        def visit_UnaryOp(self, node):
            self.visit(node.operand)

        def visit_Call(self, node):
            # Only allow calls to functions defined in the safe globals
            if isinstance(node.func, ast.Name):
                if node.func.id not in allowed_names:
                    raise ValueError(f"Disallowed function: {node.func.id}")
            else:
                raise ValueError("Only simple function names are allowed")
            for arg in node.args:
                self.visit(arg)

        def visit_Name(self, node):
            if node.id not in allowed_names:
                raise ValueError(f"Disallowed name: {node.id}")

        def visit_Constant(self, node):
            if not isinstance(node.value, (int, float, complex)):
                raise ValueError("Only numeric constants are allowed")

        def visit_Num(self, node):  # For Python <3.8
            if not isinstance(node.n, (int, float, complex)):
                raise ValueError("Only numeric constants are allowed")

        # Allow list of arithmetic operators
        def visit_Add(self, node): pass
        def visit_Sub(self, node): pass
        def visit_Mult(self, node): pass
        def visit_Div(self, node): pass
        def visit_FloorDiv(self, node): pass
        def visit_Mod(self, node): pass
        def visit_Pow(self, node): pass
        def visit_UAdd(self, node): pass
        def visit_USub(self, node): pass

    try:
        # Parse the expression (no code execution at this point)
        parsed = ast.parse(code_string, mode="eval")
        # Validate the AST
        SafeVisitor().visit(parsed)
        # Evaluate safely with restricted globals
        result = eval(compile(parsed, "<string>", mode="eval"), safe_globals, {})
        return str(result)
    except Exception:
        # Any parsing or evaluation error is treated as unsafe
        return "Unsafe Code Detected!"