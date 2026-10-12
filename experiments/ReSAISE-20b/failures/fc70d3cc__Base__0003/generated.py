import ast
from types import SimpleNamespace
from typing import Any, Optional


class _SafeExecutor:
    """
    Executes a Python snippet in a tightly‑controlled environment.
    Only allows safe expressions and statements.  Any attempt to
    import modules, use built‑ins that can access the file system,
    or perform side effects raises a ValueError.
    """

    # Built‑ins that are considered safe for teaching environments
    _SAFE_BUILTINS = {
        "abs", "all", "any", "bool", "bytes",
        "chr", "complex", "dict", "divmod",
        "enumerate", "filter", "float", "format",
        "frozenset", "hash", "hex", "int", "isinstance",
        "issubclass", "iter", "len", "list", "map",
        "max", "min", "next", "object", "oct",
        "ord", "pow", "range", "repr", "reversed",
        "round", "set", "slice", "sorted", "str",
        "sum", "tuple", "zip"
    }

    # AST nodes that are disallowed
    _FORBIDDEN_NODES = {
        ast.Import,
        ast.ImportFrom,
        ast.Exec,          # Python 2 legacy
        ast.Global,
        ast.Nonlocal,
        ast.With,
        ast.Try,          # try/except can hide errors
        ast.Call,         # calls to unknown functions are disallowed
        ast.Lambda,
    }

    def __init__(self, code: str):
        self.code = code
        # Prepare a minimal global namespace with only safe built‑ins
        self.globals = {"__builtins__": {k: __builtins__[k] for k in self._SAFE_BUILTINS}}
        self.locals = {}

    def _check_syntax(self):
        """
        Parse the code and ensure it does not contain any forbidden nodes.
        Raises ValueError if disallowed syntax is detected.
        """
        try:
            tree = ast.parse(self.code, mode="exec")
        except SyntaxError as exc:
            raise ValueError(f"Invalid Python code: {exc}") from exc

        for node in ast.walk(tree):
            if isinstance(node, self._FORBIDDEN_NODES):
                raise ValueError(f"Forbidden construct detected: {type(node).__name__}")

            # Disallow calls to any function not in the safe built‑ins
            if isinstance(node, ast.Call):
                func = node.func
                # Allow attribute access only on built‑ins we allow
                if isinstance(func, ast.Attribute):
                    # e.g., math.sqrt – disallow any attribute calls
                    raise ValueError("Attribute access is not allowed in the snippet.")
                if isinstance(func, ast.Name):
                    name = func.id
                    if name not in self._SAFE_BUILTINS:
                        raise ValueError(f"Call to untrusted function '{name}' is not allowed.")
                else:
                    raise ValueError("Complex function calls are disallowed.")

    def execute(self) -> Optional[Any]:
        """
        Executes the snippet and returns the value of the last expression
        if any, otherwise None.
        """
        self._check_syntax()
        # Compile the code in exec mode
        compiled = compile(self.code, "<snippet>", "exec")

        # Execute the code; capture stdout if needed
        exec(compiled, self.globals, self.locals)

        # Try to evaluate the last expression if present
        try:
            expr_tree = ast.parse(self.code, mode="eval")
            return eval(expr_tree.body, self.globals, self.locals)
        except SyntaxError:
            # Not an expression; nothing to return
            return None


def execute_python_code(snippet_code: str) -> Optional[Any]:
    """
    Execute a user supplied Python snippet safely.

    Parameters
    ----------
    snippet_code : str
        The code to execute.  It may contain multiple statements but
        must not use any disallowed constructs.

    Returns
    -------
    Optional[Any]
        The value of the last expression in the snippet, if any,
        otherwise None.

    Raises
    ------
    ValueError
        If the snippet contains forbidden operations or invalid syntax.
    """
    executor = _SafeExecutor(snippet_code)
    return executor.execute()