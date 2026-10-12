import ast
import operator as op
import math

# Allowed binary operators mapping to Python functions
_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators mapping
_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed names from the math module
_ALLOWED_NAMES = {k for k in dir(math) if not k.startswith('_')}

class SafeEvalVisitor(ast.NodeVisitor):
    """
    Visitor that evaluates a mathematical expression safely.
    Raises ValueError if an unsupported node is encountered.
    """
    def __init__(self):
        self.result = None

    def visit(self, node):
        if isinstance(node, ast.Expression):
            return self.visit(node.body)
        elif isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError("Unsupported constant type")
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            op_type = type(node.op)
            if op_type in _BIN_OPS:
                return _BIN_OPS[op_type](left, right)
            else:
                raise ValueError("Unsupported binary operator")
        elif isinstance(node, ast.UnaryOp):
            operand = self.visit(node.operand)
            op_type = type(node.op)
            if op_type in _UNARY_OPS:
                return _UNARY_OPS[op_type](operand)
            else:
                raise ValueError("Unsupported unary operator")
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Only simple function calls allowed")
            func_name = node.func.id
            if func_name not in _ALLOWED_NAMES:
                raise ValueError(f"Function {func_name} is not allowed")
            func = getattr(math, func_name)
            args = [self.visit(arg) for arg in node.args]
            if node.keywords:
                raise ValueError("Keyword arguments not allowed")
            return func(*args)
        elif isinstance(node, ast.Name):
            if node.id in _ALLOWED_NAMES:
                return getattr(math, node.id)
            else:
                raise ValueError(f"Name {node.id} is not allowed")
        elif isinstance(node, ast.Expr):
            return self.visit(node.value)
        else:
            raise ValueError(f"Unsupported expression type: {type(node).__name__}")

def evaluate_expression_safely(expression: str) -> str:
    """
    Safely evaluates a mathematical expression written in Python syntax.
    
    Parameters
    ----------
    expression : str
        The mathematical expression to evaluate.

    Returns
    -------
    str
        The result of the evaluation converted to string, or
        'Unsafe Code Detected!' if the expression is unsafe or an error occurs.
    """
    try:
        # Parse into an AST
        parsed = ast.parse(expression, mode='eval')
        
        # Verify that the tree contains only allowed nodes
        for node in ast.walk(parsed):
            if not isinstance(node, (
                ast.Expression,
                ast.Constant,
                ast.Num,
                ast.BinOp,
                ast.UnaryOp,
                ast.Call,
                ast.Name,
                ast.Load,
                ast.Expr,
            )):
                raise ValueError(f"Disallowed node: {type(node).__name__}")

        visitor = SafeEvalVisitor()
        result = visitor.visit(parsed)
        return str(result)
    except Exception:
        # Any exception is treated as unsafe
        return 'Unsafe Code Detected!'