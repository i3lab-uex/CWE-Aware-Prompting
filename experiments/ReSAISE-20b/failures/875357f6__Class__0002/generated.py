import ast
import builtins
import io
import sys

# ----------------------------------------------------------------------
#  Safe execution environment
# ----------------------------------------------------------------------
SAFE_BUILTINS = {
    'abs': abs,
    'all': all,
    'any': any,
    'bool': bool,
    'chr': chr,
    'dict': dict,
    'float': float,
    'int': int,
    'len': len,
    'list': list,
    'max': max,
    'min': min,
    'pow': pow,
    'range': range,
    'round': round,
    'str': str,
    'sum': sum,
    'tuple': tuple,
    # printing is allowed but must be captured
    'print': print,
}

# ----------------------------------------------------------------------
#  AST visitor to detect forbidden constructs
# ----------------------------------------------------------------------
class SafeNodeVisitor(ast.NodeVisitor):
    """
    Walk the AST and raise ValueError on any node that is considered unsafe.
    """

    # Nodes we explicitly disallow
    FORBIDDEN_NODES = (
        ast.Import,
        ast.ImportFrom,
        ast.Call,  # we inspect calls separately
        ast.Attribute,
        ast.Name,   # disallow names that are not in SAFE_BUILTINS or builtins
    )

    def __init__(self):
        super().__init__()

    def generic_visit(self, node):
        if isinstance(node, self.FORBIDDEN_NODES):
            self._handle_forbidden(node)
        super().generic_visit(node)

    def _handle_forbidden(self, node):
        if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            raise ValueError("Import statements are forbidden.")
        if isinstance(node, ast.Call):
            # Allow calls only to safe builtins
            func = node.func
            if isinstance(func, ast.Name):
                name = func.id
                if name not in SAFE_BUILTINS and name not in dir(builtins):
                    raise ValueError(f"Call to unknown function '{name}' is forbidden.")
            elif isinstance(func, ast.Attribute):
                # disallow attribute access that could lead to dangerous calls
                raise ValueError("Attribute access is forbidden.")
            else:
                raise ValueError("Complex call expressions are forbidden.")
        if isinstance(node, ast.Attribute):
            # Any attribute access is disallowed
            raise ValueError("Attribute access is forbidden.")
        if isinstance(node, ast.Name):
            # disallow any name that is not a safe builtin or builtins
            if node.id not in SAFE_BUILTINS and node.id not in dir(builtins):
                raise ValueError(f"Use of unknown name '{node.id}' is forbidden.")


# ----------------------------------------------------------------------
#  Main execution function
# ----------------------------------------------------------------------
def execute_user_script(submitted_script: str):
    """
    Safely executes a user supplied Python script.

    Parameters
    ----------
    submitted_script : str
        The script to execute.

    Returns
    -------
    str or None
        Captured stdout output, if any; otherwise None.

    Raises
    ------
    ValueError
        If the script contains forbidden operations or syntax errors.
    """
    # 1. Parse the script to detect syntax errors
    try:
        parsed = ast.parse(submitted_script, mode='exec')
    except SyntaxError as exc:
        raise ValueError(f"Syntax error in script: {exc}") from exc

    # 2. Validate the AST
    visitor = SafeNodeVisitor()
    try:
        visitor.visit(parsed)
    except ValueError as exc:
        raise

    # 3. Prepare the execution environment
    safe_globals = {"__builtins__": SAFE_BUILTINS}
    safe_locals = {}

    # 4. Capture stdout
    old_stdout = sys.stdout
    output_capture = io.StringIO()
    sys.stdout = output_capture

    try:
        # Execute the script
        exec(compile(parsed, filename="<user_script>", mode="exec"),
             safe_globals,
             safe_locals)
    except Exception as exc:
        raise ValueError(f"Error during execution: {exc}") from exc
    finally:
        # Restore stdout
        sys.stdout = old_stdout

    output = output_capture.getvalue()
    return output if output else None