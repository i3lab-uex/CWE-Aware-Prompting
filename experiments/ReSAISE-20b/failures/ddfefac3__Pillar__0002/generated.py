import ast
import builtins
import io
import sys
from types import SimpleNamespace

# --------------------------------------------------------------------------- #
# Safe execution environment for teaching code snippets
# --------------------------------------------------------------------------- #

def _is_safe_node(node: ast.AST) -> bool:
    """
    Recursively check if a node is allowed.  Raises ValueError if forbidden.
    """
    # Disallowed statement types
    disallowed = (
        ast.Import,          # import foo
        ast.ImportFrom,      # from foo import bar
        ast.Exec,            # exec() in Python 2 (just for completeness)
    )
    if isinstance(node, disallowed):
        raise ValueError(f"Disallowed import statement: {ast.dump(node)}")

    # Disallow calls to dangerous builtins
    if isinstance(node, ast.Call):
        # Function name resolution
        func = node.func
        if isinstance(func, ast.Name) and func.id in {"open", "eval", "exec", "__import__"}:
            raise ValueError(f"Disallowed function call: {func.id}")
        if isinstance(func, ast.Attribute):
            # e.g., os.system, subprocess.Popen
            attr_chain = []
            cur = func
            while isinstance(cur, ast.Attribute):
                attr_chain.append(cur.attr)
                cur = cur.value
            if isinstance(cur, ast.Name):
                attr_chain.append(cur.id)
                chain = ".".join(reversed(attr_chain))
                if any(chain.startswith(x) for x in {"os.", "subprocess.", "sys."}):
                    raise ValueError(f"Disallowed attribute call: {chain}")

    # Disallow accessing __dict__ or arbitrary attributes
    if isinstance(node, ast.Attribute):
        if node.attr in {"__dict__", "__class__", "__globals__", "__code__"}:
            raise ValueError(f"Disallowed attribute access: {node.attr}")

    # Recurse into child nodes
    for child in ast.iter_child_nodes(node):
        _is_safe_node(child)

def process_python_code(code_str: str):
    """
    Execute a user‑supplied Python snippet in a sandboxed environment.

    Parameters
    ----------
    code_str : str
        The Python source to run.

    Returns
    -------
    Any
        Result of the last expression if present, otherwise None.

    Raises
    ------
    ValueError
        If the code contains forbidden operations or is syntactically invalid.
    """
    # Parse and perform static safety checks
    try:
        parsed = ast.parse(code_str, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from exc

    _is_safe_node(parsed)

    # Prepare a minimal set of safe builtins
    SAFE_BUILTINS = {
        "abs": abs,
        "all": all,
        "any": any,
        "bool": bool,
        "dict": dict,
        "float": float,
        "int": int,
        "len": len,
        "list": list,
        "max": max,
        "min": min,
        "pow": pow,
        "range": range,
        "repr": repr,
        "round": round,
        "str": str,
        "sum": sum,
        "tuple": tuple,
        # I/O
        "print": print,
    }

    # Capture stdout/stderr to avoid leaking output during tests
    old_stdout, old_stderr = sys.stdout, sys.stderr
    fake_out = io.StringIO()
    try:
        sys.stdout = sys.stderr = fake_out
        exec(compile(parsed, filename="<user_snippet>", mode="exec"),
             {"__builtins__": SAFE_BUILTINS}, {})
    finally:
        sys.stdout, sys.stderr = old_stdout, old_stderr

    # Try to evaluate the last expression if it exists
    last_expr = None
    for node in reversed(parsed.body):
        if isinstance(node, ast.Expr):
            last_expr = node.value
            break

    if last_expr is not None:
        try:
            return eval(compile(ast.Expression(last_expr), filename="<user_snippet>", mode="eval"),
                        {"__builtins__": SAFE_BUILTINS}, {})
        except Exception:
            # If evaluation fails, fall back to None
            return None

    return None