#!/usr/bin/env python3
"""
Parse a linear transformation string into a 3x3 matrix and an optional numerical vector.

The input format is:
    "row1;row2;row3[,v1,v2,v3]"

Each row is a linear combination of the symbols `a`, `b` and `c`.  The optional vector
is a comma‑separated list of three numeric values that follow the matrix rows.

Examples:
    "a;b;c"                       ->  np.eye(3), []
    "3a+4b;2a+3b;4c"              ->  [[3, 2, 0], [4, 3, 0], [0, 0, 4]], []
    "a+b+c;2b+3c;5a;1,0,-1"       ->  [[1, 1, 1], [0, 2, 3], [5, 0, 0]], [1.0, 0.0, -1.0]
"""

import re
from typing import Tuple, List

import numpy as np
import sympy as sp


def _extract_coeff(expr: str, var: str) -> float:
    """
    Safely evaluate the coefficient of `var` in a symbolic expression.
    Uses sympy to avoid arbitrary code execution.

    Parameters
    ----------
    expr : str
        The expression string (e.g., "3a+4b").
    var : str
        One of 'a', 'b', or 'c'.

    Returns
    -------
    float
        The numeric coefficient of `var` in the expression.
    """
    # Replace variable names with sympy symbols
    a, b, c = sp.symbols("a b c")
    local_dict = {"a": a, "b": b, "c": c}
    try:
        sym_expr = sp.sympify(expr, locals=local_dict)
    except (sp.SympifyError, TypeError) as exc:
        raise ValueError(f"Failed to parse expression '{expr}': {exc}") from exc

    # Evaluate the coefficient by substituting 1 for the variable of interest
    # and 0 for the others.
    subs = {a: 1 if var == "a" else 0,
            b: 1 if var == "b" else 0,
            c: 1 if var == "c" else 0}
    coeff = sym_expr.subs(subs)
    # If the result is still symbolic (e.g., contains other symbols), raise an error
    if coeff.free_symbols:
        raise ValueError(f"Expression '{expr}' contains unsupported symbols: {coeff.free_symbols}")
    return float(coeff)


def parse_transformation_string(transformation_string: str) -> Tuple[np.ndarray, List[float]]:
    """
    Parse a transformation string into a 3x3 matrix and an optional vector.

    Parameters
    ----------
    transformation_string : str
        A string of the form "row1;row2;row3[,v1,v2,v3]".

    Returns
    -------
    tuple(np.ndarray, list[float])
        The 3x3 matrix of floats and a list of three floats representing the vector.
        If no vector is supplied, the second element will be an empty list.

    Raises
    ------
    ValueError
        If the string cannot be parsed or contains invalid expressions.
    """
    if not isinstance(transformation_string, str):
        raise ValueError("Input must be a string")

    # Split off an optional vector part after the last semicolon
    parts = transformation_string.split(";")
    if len(parts) < 3:
        raise ValueError("At least three rows are required for a 3x3 matrix")

    # Detect vector: if the last part contains a comma and more than one element
    vector = []
    last_part = parts[-1]
    if "," in last_part:
        # The last part contains both the last row and vector
        row_str, vec_str = last_part.split(",", 1)
        parts[-1] = row_str
        try:
            vector = [float(v.strip()) for v in vec_str.split(",")]
        except ValueError as exc:
            raise ValueError(f"Vector part contains non‑numeric values: {exc}") from exc
        if len(vector) != 3:
            raise ValueError("Vector must contain exactly three numeric values")
    else:
        # No vector part
        pass

    if len(parts) != 3:
        raise ValueError("Exactly three rows are required for a 3x3 matrix")

    # Build the matrix
    matrix = []
    for row_expr in parts:
        coeffs = [0.0, 0.0, 0.0]  # a, b, c
        for var, idx in zip("abc", range(3)):
            try:
                coeffs[idx] = _extract_coeff(row_expr, var)
            except ValueError as exc:
                raise ValueError(f"Failed to parse row '{row_expr}': {exc}") from exc
        matrix.append(coeffs)

    return np.array(matrix, dtype=float), vector

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     m, v = parse_transformation_string("3a+4b;2a+3b;4c")
#     print(m)
#     print(v)