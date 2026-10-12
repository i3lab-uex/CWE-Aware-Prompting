import ast
from typing import Any

class SafeEvalVisitor(ast.NodeVisitor):
    """
    Visitor that verifies an AST contains only safe nodes.
    Allowed:
        - Literals: numbers, strings
        - Binary operations: +, -, *, /, //, %, **, <<, >>, |, &, ^ (only numeric or string ops)
        - Unary operations: +, -, ~
        - Comparisons: ==, !=, <, <=, >, >=
        - Boolean ops: and, or, not
        - Subscripts for strings/lists (e.g., s[0])
        - Attribute access only on literals (no objects)
    Disallowed:
        - Import, exec, eval, function definitions, class defs, etc.
        - Names (variables) except built-in constants like True/False/None
    """
    SAFE_BINOPS = {
        ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv,
        ast.Mod, ast.Pow, ast.LShift, ast.RShift, ast.BitOr,
        ast.BitAnd, ast.BitXor
    }
    SAFE_UNARYOPS = {ast.UAdd, ast.USub, ast.Not, ast.Invert}
    SAFE_COMPARISONS = {
        ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE
    }
    SAFE_BOOLOPS = {ast.And, ast.Or}

    def visit(self, node: ast.AST) -> Any:
        method = f'visit_{node.__class__.__name__}'
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def visit_Module(self, node: ast.Module):
        for stmt in node.body:
            self.visit(stmt)

    def visit_Expr(self, node: ast.Expr):
        self.visit(node.value)

    def visit_BinOp(self, node: ast.BinOp):
        if type(node.op) not in self.SAFE_BINOPS:
            raise ValueError("Unsafe binary operator")
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node: ast.UnaryOp):
        if type(node.op) not in self.SAFE_UNARYOPS:
            raise ValueError("Unsafe unary operator")
        self.visit(node.operand)

    def visit_BoolOp(self, node: ast.BoolOp):
        if type(node.op) not in self.SAFE_BOOLOPS:
            raise ValueError("Unsafe boolean operator")
        for value in node.values:
            self.visit(value)

    def visit_Compare(self, node: ast.Compare):
        for op in node.ops:
            if type(op) not in self.SAFE_COMPARISONS:
                raise ValueError("Unsafe comparison operator")
        self.visit(node.left)
        for comparator in node.comparators:
            self.visit(comparator)

    def visit_Name(self, node: ast.Name):
        if node.id not in {'True', 'False', 'None'}:
            raise ValueError("Use of undefined names is not allowed")

    def visit_Constant(self, node: ast.Constant):
        if isinstance(node.value, (int, float, str, bool)) or node.value is None:
            return
        raise ValueError("Unsupported constant type")

    def visit_Subscript(self, node: ast.Subscript):
        self.visit(node.value)
        self.visit(node.slice)

    def visit_Index(self, node: ast.Index):
        self.visit(node.value)

    def visit_Slice(self, node: ast.Slice):
        if node.lower:
            self.visit(node.lower)
        if node.upper:
            self.visit(node.upper)
        if node.step:
            self.visit(node.step)

    def visit_Attribute(self, node: ast.Attribute):
        # Disallow any attribute access except on constants
        if not isinstance(node.value, ast.Constant):
            raise ValueError("Attribute access is disallowed")
        # Even if constant, attribute might be dangerous (e.g., '__class__')
        raise ValueError("Attribute access is disallowed")

    # Disallow all other nodes by default
    def generic_visit(self, node: ast.AST):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef,
                            ast.ClassDef, ast.Lambda, ast.Call, ast.Exec)):
            raise ValueError("Disallowed node type")
        super().generic_visit(node)

def execute_user_code(script_code: str) -> str:
    """
    Safely evaluate a user supplied script containing only arithmetic
    and string operations. Returns the result as a string or
    'Execution Blocked!' if unsafe.
    """
    try:
        # Parse the code into an AST
        tree = ast.parse(script_code, mode='exec')
        # Validate safety of the AST
        SafeEvalVisitor().visit(tree)
        # Compile and evaluate with no globals/locals
        compiled = compile(tree, filename="<user_script>", mode="exec")
        local_vars: dict[str, Any] = {}
        exec(compiled, {}, local_vars)
        # If the script produced a value via an expression, capture it
        # The last expression's result can be found in the local_vars if named 'result'
        # For simplicity, we return any variable defined as result or the first expr
        if 'result' in local_vars:
            return str(local_vars['result'])
        # Try to get the last expression value from local_vars
        if local_vars:
            return str(next(iter(local_vars.values())))
        # If nothing was produced, return empty string
        return ""
    except Exception:
        return "Execution Blocked!"