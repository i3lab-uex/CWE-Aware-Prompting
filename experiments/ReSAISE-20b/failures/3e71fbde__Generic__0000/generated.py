import ast
import io
import sys
from types import FunctionType, ModuleType

# ----------------------------------------------------------------------
# 1. Whitelist of safe built‑ins
# ----------------------------------------------------------------------
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "chr": chr,
    "complex": complex,
    "dict": dict,
    "divmod": divmod,
    "enumerate": enumerate,
    "filter": filter,
    "float": float,
    "format": format,
    "hash": hash,
    "hex": hex,
    "int": int,
    "isinstance": isinstance,
    "issubclass": issubclass,
    "iter": iter,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "next": next,
    "oct": oct,
    "ord": ord,
    "pow": pow,
    "range": range,
    "repr": repr,
    "reversed": reversed,
    "round": round,
    "set": set,
    "slice": slice,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "zip": zip,
    # I/O helpers
    "print": print,
}

# ----------------------------------------------------------------------
# 2. AST validation: disallow dangerous nodes
# ----------------------------------------------------------------------
DISALLOWED_NODES = (
    ast.Import,
    ast.ImportFrom,
    ast.Exec,           # Python 2 only
    ast.Call,          # we filter calls to disallowed names below
)

DISALLOWED_NAMES = {
    "open", "eval", "exec", "__import__", "compile",
    # OS and subprocess
    "os", "subprocess", "shutil", "sys",
}

def _validate_ast(node: ast.AST) -> None:
    """
    Recursively walk the AST and raise ValueError if a disallowed
    construct is found.
    """
    for child in ast.iter_child_nodes(node):
        # Disallowed node types
        if isinstance(child, DISALLOWED_NODES):
            raise ValueError(f"Disallowed syntax: {type(child).__name__}")

        # Disallow function calls to dangerous names
        if isinstance(child, ast.Call):
            func = child.func
            # Handle simple name calls like open()
            if isinstance(func, ast.Name) and func.id in DISALLOWED_NAMES:
                raise ValueError(f"Disallowed function call: {func.id}")
            # Handle attribute calls like os.system()
            if isinstance(func, ast.Attribute):
                attr_chain = []
                current = func
                while isinstance(current, ast.Attribute):
                    attr_chain.append(current.attr)
                    current = current.value
                if isinstance(current, ast.Name):
                    attr_chain.append(current.id)
                full_name = ".".join(reversed(attr_chain))
                if any(part in DISALLOWED_NAMES for part in attr_chain):
                    raise ValueError(f"Disallowed attribute call: {full_name}")

        _validate_ast(child)

# ----------------------------------------------------------------------
# 3. Execution helper
# ----------------------------------------------------------------------
def run_code_snippet(snippet: str):
    """
    Execute a small Python code snippet in a restricted environment.
    Returns None if there is no output; otherwise returns the captured
    stdout as a string. If the snippet ends with an expression, its value
    is returned instead of stdout.
    Raises ValueError for disallowed operations.
    """
    # 3.1 Validate the snippet
    try:
        parsed = ast.parse(snippet, mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Syntax error: {e}") from None

    _validate_ast(parsed)

    # 3.2 Separate expression from statements
    if (
        len(parsed.body) == 1 and isinstance(parsed.body[0], ast.Expr)
    ):
        # Single expression – evaluate it
        expr_node = parsed.body[0].value
        compiled_expr = compile(ast.Expression(expr_node), "<snippet>", "eval")
        result = eval(compiled_expr, {"__builtins__": SAFE_BUILTINS}, {})
        return result

    # 3.3 Execute statements
    compiled = compile(parsed, "<snippet>", "exec")

    # Capture stdout
    old_stdout = sys.stdout
    buffer = io.StringIO()
    try:
        sys.stdout = buffer
        exec(compiled, {"__builtins__": SAFE_BUILTINS}, {})
    finally:
        sys.stdout = old_stdout

    output = buffer.getvalue()
    return output if output else None