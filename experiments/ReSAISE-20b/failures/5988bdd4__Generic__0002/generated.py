import ast
import sys
from io import StringIO
from types import ModuleType

# --- helper functions -------------------------------------------------------

def _is_forbidden(node: ast.AST) -> bool:
    """
    Return True if the AST node represents a potentially dangerous operation.
    """
    forbidden_types = (
        ast.Import,          # import statements
        ast.ImportFrom,      # from ... import ...
        ast.Exec,            # exec statement (Python 2 only, but kept for completeness)
        ast.Call,
    )
    if isinstance(node, forbidden_types):
        # Further checks for dangerous calls
        if isinstance(node, ast.Call):
            # disallow built-in functions that could access the filesystem or execute code
            if isinstance(node.func, ast.Name):
                if node.func.id in {"exec", "eval", "__import__", "open"}:
                    return True
            # disallow attribute calls like os.system, subprocess.Popen, etc.
            if isinstance(node.func, ast.Attribute):
                attr_chain = []
                cur = node.func
                while isinstance(cur, ast.Attribute):
                    attr_chain.append(cur.attr)
                    cur = cur.value
                if isinstance(cur, ast.Name):
                    attr_chain.append(cur.id)
                # reverse to get call chain e.g., os.system -> ['os', 'system']
                attr_chain.reverse()
                if "os" in attr_chain or "subprocess" in attr_chain:
                    return True
        return False
    return False


def _check_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if forbidden nodes are found.
    """
    for child in ast.walk(node):
        if _is_forbidden(child):
            raise ValueError("Snippet contains forbidden operations.")


def _safe_builtins() -> dict:
    """
    Return a minimal set of safe built-in functions.
    """
    allowed = {
        "abs": abs,
        "all": all,
        "any": any,
        "bool": bool,
        "chr": chr,
        "dict": dict,
        "enumerate": enumerate,
        "float": float,
        "int": int,
        "len": len,
        "list": list,
        "max": max,
        "min": min,
        "pow": pow,
        "range": range,
        "round": round,
        "str": str,
        "sum": sum,
        "tuple": tuple,
        # Add more safe functions as needed
    }
    return allowed


# --- main function ----------------------------------------------------------

def run_python_snippet(snippet_string: str):
    """
    Execute a user-provided Python snippet in a restricted environment.

    Parameters
    ----------
    snippet_string : str
        The code to execute.

    Returns
    -------
    Any
        The value produced by the snippet if it is an expression; otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or is syntactically invalid.
    """
    # Parse the code and validate
    try:
        parsed = ast.parse(snippet_string, mode="exec")
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in snippet: {exc}") from None

    _check_ast(parsed)

    # Prepare restricted globals and locals
    safe_globals = {"__builtins__": _safe_builtins()}
    safe_locals = {}

    # Capture stdout
    old_stdout = sys.stdout
    stdout_capture = StringIO()
    sys.stdout = stdout_capture

    try:
        # If the snippet is a single expression, evaluate and return its value
        if len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr):
            expr = parsed.body[0].value
            code_obj = compile(ast.Expression(expr), filename="<snippet>", mode="eval")
            result = eval(code_obj, safe_globals, safe_locals)
        else:
            # Execute the snippet; any printed output is captured but not returned
            exec(compile(parsed, filename="<snippet>", mode="exec"), safe_globals, safe_locals)
            result = None
    except Exception as exc:
        raise ValueError(f"Error during snippet execution: {exc}") from None
    finally:
        sys.stdout = old_stdout

    return result