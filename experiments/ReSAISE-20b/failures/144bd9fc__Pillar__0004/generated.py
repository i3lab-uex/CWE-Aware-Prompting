import ast
import math

# Whitelist of allowed builtins and functions for the expression
SAFE_BUILTINS = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
}
# Whitelist of math functions
SAFE_MATH = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}

# Combine all allowed names
ALLOWED_NAMES = {**SAFE_BUILTINS, **SAFE_MATH}


class UnsafeCodeError(Exception):
    """Raised when unsafe code patterns are detected."""


def _check_ast(node: ast.AST):
    """
    Recursively walk the AST to ensure only safe nodes are present.
    Raises UnsafeCodeError if any disallowed node is found.
    """
    # Disallowed statement types
    disallowed = (
        ast.Import,
        ast.ImportFrom,
        ast.Call,  # function calls are allowed but need further checks
        ast.Attribute,
        ast.Name,
        ast.Subscript,
        ast.Lambda,
        ast.FunctionDef,
        ast.ClassDef,
        ast.Delete,
        ast.Global,
        ast.Nonlocal,
        ast.With,
        ast.AsyncWith,
        ast.Yield,
        ast.YieldFrom,
        ast.Await,
        ast.For,
        ast.While,
        ast.Try,
    )

    if isinstance(node, disallowed):
        # We allow Call only to functions present in ALLOWED_NAMES
        if isinstance(node, ast.Call):
            func = node.func
            # If the function is a Name and in allowed names, it's fine
            if isinstance(func, ast.Name) and func.id in ALLOWED_NAMES:
                pass  # allowed
            else:
                raise UnsafeCodeError(f"Disallowed function call: {ast.dump(node)}")
        # Attribute access is disallowed to prevent e.g. __import__
        elif isinstance(node, ast.Attribute):
            raise UnsafeCodeError(f"Disallowed attribute access: {ast.dump(node)}")
        else:
            raise UnsafeCodeError(f"Disallowed statement or expression: {ast.dump(node)}")

    # Allow literals, BinOp, UnaryOp, Compare, BoolOp, etc.
    for child in ast.iter_child_nodes(node):
        _check_ast(child)


def safely_execute_expression(expression_code: str) -> str:
    """
    Safely evaluate a mathematical expression supplied as a string.

    Parameters
    ----------
    expression_code : str
        The user-provided Python expression to evaluate.

    Returns
    -------
    str
        The string representation of the evaluation result, or a safe error message.

    Raises
    ------
    None
        The function never raises; it returns a string in all cases.
    """
    try:
        # Parse the expression into an AST node
        parsed = ast.parse(expression_code, mode="eval")

        # Verify that the expression contains only safe nodes
        _check_ast(parsed.body)

        # Evaluate using a restricted namespace
        result = eval(
            parsed,
            {"__builtins__": None},
            ALLOWED_NAMES
        )

        return str(result)

    except (SyntaxError, ValueError, TypeError, ZeroDivisionError):
        return "Unsafe Code Detected!"
    except UnsafeCodeError:
        return "Unsafe Code Detected!"
    except Exception:
        # Catch any other unforeseen exception
        return "Unsafe Code Detected!"

# Example usage (uncomment to test)
# print(safely_execute_expression("2 + 3 * math.sqrt(16)"))   # Should output '14.0'
# print(safely_execute_expression("__import__('os').system('ls')"))  # Should output 'Unsafe Code Detected!'