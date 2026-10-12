import ast

# Define the set of AST node types that are considered unsafe.
UNSAFE_NODES = {
    ast.Import,
    ast.ImportFrom,
    ast.Exec,               # exec() is a statement in Python 2 only
    ast.Call,
}

# Functions that are explicitly disallowed even if they appear in a Call node.
DISALLOWED_FUNCTIONS = {
    "open",
    "eval",
    "exec",
    "compile",
    "input",
    "__import__",
}

# Allowed built‑in functions (you can extend this list as needed).
ALLOWED_BUILTINS = {
    "abs",
    "all",
    "any",
    "bool",
    "chr",
    "complex",
    "dict",
    "divmod",
    "float",
    "format",
    "hash",
    "hex",
    "int",
    "isinstance",
    "len",
    "list",
    "max",
    "min",
    "pow",
    "range",
    "repr",
    "round",
    "str",
    "sum",
    "tuple",
}


def _check_safety(node: ast.AST):
    """
    Recursively walk the AST and raise ValueError if a disallowed node or function
    is found.
    """
    # Check for disallowed node types directly.
    if type(node) in UNSAFE_NODES:
        raise ValueError(f"Disallowed operation: {type(node).__name__}")

    # If the node is a Call, ensure that it does not call a disallowed function.
    if isinstance(node, ast.Call):
        # Function can be Name or Attribute; we only disallow direct calls to
        # builtins that are not in ALLOWED_BUILTINS.
        func = node.func
        if isinstance(func, ast.Name):
            if func.id in DISALLOWED_FUNCTIONS:
                raise ValueError(f"Disallowed function call: {func.id}")
        elif isinstance(func, ast.Attribute):
            # Prevent calls like os.system or subprocess.Popen
            raise ValueError(f"Disallowed attribute call: {ast.unparse(func)}")

    # Recursively check all child nodes.
    for child in ast.iter_child_nodes(node):
        _check_safety(child)


def execute_code_snippet(code_snippet: str):
    """
    Execute a small piece of Python code safely.

    Parameters
    ----------
    code_snippet : str
        The user supplied code to execute. It may contain expressions, statements,
        or a combination of both.

    Returns
    -------
    result : object | None
        The value of the last expression evaluated in the snippet, or None if
        there is no expression.

    Raises
    ------
    ValueError
        If the snippet contains disallowed operations or syntax errors.
    """
    try:
        # Parse into an AST; mode='exec' allows statements and expressions.
        tree = ast.parse(code_snippet, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in code snippet: {exc}") from None

    # Perform safety checks.
    _check_safety(tree)

    # Prepare a minimal execution environment.
    safe_globals = {"__builtins__": {name: __builtins__[name] for name in ALLOWED_BUILTINS}}
    safe_locals = {}

    # Compile the AST into a code object.
    compiled_code = compile(tree, filename="<safe_exec>", mode="exec")

    # Execute the code. We capture the value of the last expression by
    # inspecting the AST for a trailing Expr node.
    exec(compiled_code, safe_globals, safe_locals)

    # Find the last expression node (if any) and evaluate it again to get its value.
    expr_value = None
    for node in reversed(tree.body):
        if isinstance(node, ast.Expr):
            # Evaluate the expression in the same context.
            expr_value = eval(compile(ast.Expression(node.value), filename="<expr>", mode="eval"),
                              safe_globals, safe_locals)
            break

    return expr_value