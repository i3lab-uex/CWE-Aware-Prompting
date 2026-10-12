import ast

# A very small whitelist of allowed built‑in names and functions.
ALLOWED_BUILTINS = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "sum": sum,
    "len": len,
}

# Optionally allow a few safe math functions.
try:
    import math
    ALLOWED_BUILTINS.update({k: getattr(math, k) for k in dir(math) if not k.startswith("_")})
except Exception:
    pass


class ProhibitedNodeVisitor(ast.NodeVisitor):
    """
    Walk the AST and raise ValueError if a prohibited node is encountered.
    """

    PROHIBITED_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Call,  # Calls are checked more finely below.
    )

    def visit(self, node):
        if isinstance(node, self.PROHIBITED_NODES):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                raise ValueError(f"Import statements are not allowed: {ast.dump(node)}")
            if isinstance(node, ast.Call):
                self._check_call(node)
        return super().visit(node)

    def _check_call(self, node: ast.Call):
        # Disallow calls to unsafe built‑ins or modules.
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            # Disallow calls to built‑ins that are not in the whitelist.
            if func_name not in ALLOWED_BUILTINS:
                raise ValueError(f"Call to disallowed function '{func_name}'")
        elif isinstance(node.func, ast.Attribute):
            # Disallow any attribute access (e.g., os.system, subprocess.Popen)
            raise ValueError(f"Attribute calls are not allowed: {ast.dump(node)}")
        # Recursively visit arguments to catch nested calls
        for arg in node.args:
            self.visit(arg)
        for kw in node.keywords:
            self.visit(kw.value)


def safe_execute_code(snippet: str):
    """
    Execute a user‑supplied Python snippet in a tightly controlled environment.
    
    Parameters
    ----------
    snippet : str
        The code to execute.

    Returns
    -------
    Any
        Result of the last expression in the snippet, or None if no value.

    Raises
    ------
    ValueError
        If the snippet contains prohibited actions.
    """
    # Parse into an AST to validate it first
    try:
        parsed = ast.parse(snippet, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in snippet: {e}")

    # Validate the AST
    ProhibitedNodeVisitor().visit(parsed)

    # Prepare a restricted global namespace
    globals_dict = {"__builtins__": ALLOWED_BUILTINS}

    # Execute the snippet
    exec(compile(parsed, filename="<safe_exec>", mode="exec"), globals_dict)

    # If the last statement was an expression, return its value
    if parsed.body:
        last = parsed.body[-1]
        if isinstance(last, ast.Expr):
            # Evaluate the expression in the same restricted namespace
            return eval(compile(ast.Expression(last.value), filename="<safe_exec>", mode="eval"),
                         globals_dict)
    return None