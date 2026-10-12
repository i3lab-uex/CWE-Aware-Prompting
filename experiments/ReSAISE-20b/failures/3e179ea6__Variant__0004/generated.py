import ast
import operator as op
import math

# Allowed binary operators mapping to actual functions
_ALLOWED_BINOPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# Allowed unary operators
_ALLOWED_UNOPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}

# Allowed functions from the math module
_ALLOWED_FUNCS = {
    name for name in dir(math) if not name.startswith("_")
}

# Allowed constants from the math module
_ALLOWED_CONSTS = {
    name for name in dir(math) if isinstance(getattr(math, name), (int, float))
}


def evaluate_expression_safely(expression: str) -> str:
    """
    Safely evaluates a mathematical expression represented as a string.
    Only numeric literals, basic arithmetic operators and functions/constants
    from the math module are allowed.

    Parameters:
        expression (str): The expression to evaluate.

    Returns:
        str: Result of the evaluation or 'Unsafe Code Detected!' if
             disallowed constructs are found or an error occurs.
    """
    try:
        # Parse the expression into an AST
        tree = ast.parse(expression, mode="eval")

        # Walk the AST and ensure only allowed nodes are present
        for node in ast.walk(tree):
            if isinstance(node, ast.Module):
                continue
            elif isinstance(node, (ast.Expression,)):
                continue
            elif isinstance(node, ast.Num):  # Python <3.8
                continue
            elif isinstance(node, ast.Constant):  # Python >=3.8
                if not isinstance(node.value, (int, float)):
                    return "Unsafe Code Detected!"
            elif isinstance(node, ast.BinOp):
                if type(node.op) not in _ALLOWED_BINOPS:
                    return "Unsafe Code Detected!"
            elif isinstance(node, ast.UnaryOp):
                if type(node.op) not in _ALLOWED_UNOPS:
                    return "Unsafe Code Detected!"
            elif isinstance(node, ast.Call):
                # Only allow function calls to whitelisted math functions
                if not isinstance(node.func, ast.Name):
                    return "Unsafe Code Detected!"
                if node.func.id not in _ALLOWED_FUNCS:
                    return "Unsafe Code Detected!"
                # Ensure no arguments are themselves calls or attribute accesses
                for arg in node.args:
                    if isinstance(arg, (ast.Call, ast.Attribute)):
                        return "Unsafe Code Detected!"
            elif isinstance(node, ast.Name):
                # Only allow whitelisted constants
                if node.id not in _ALLOWED_CONSTS:
                    return "Unsafe Code Detected!"
            elif isinstance(node, ast.Attribute):
                # Disallow any attribute access
                return "Unsafe Code Detected!"
            elif isinstance(node, (ast.Lambda, ast.FunctionDef,
                                  ast.Import, ast.ImportFrom,
                                  ast.Global, ast.Nonlocal,
                                  ast.With, ast.Try, ast.Assert,
                                  ast.Delete, ast.For, ast.While,
                                  ast.If, ast.Return, ast.Yield)):
                return "Unsafe Code Detected!"
            else:
                # Any other node type is disallowed
                return "Unsafe Code Detected!"

        # Prepare a safe namespace containing only math functions and constants
        safe_globals = {name: getattr(math, name) for name in _ALLOWED_FUNCS}
        safe_globals.update({name: getattr(math, name) for name in _ALLOWED_CONSTS})

        # Evaluate the expression
        result = eval(compile(tree, filename="<ast>", mode="eval"),
                      {"__builtins__": {}}, safe_globals)

        return str(result)
    except Exception:
        # Any error results in the unsafe message
        return "Unsafe Code Detected!"