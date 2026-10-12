import re
from typing import Tuple, List, Union

import numpy as np
import sympy as sp


def parse_transformation_string(
    transformation_string: str,
) -> Tuple[Union[np.ndarray, List[List[float]]], List[float]]:
    """
    Parse a string that describes a 3x3 linear transformation matrix and an optional
    numerical vector.

    Parameters
    ----------
    transformation_string : str
        A string describing the transformation. The string is split into two parts by a
        semicolon `;`. The first part contains up to three linear expressions in the
        variables ``a``, ``b`` and ``c`` (each expression corresponds to a column of the
        matrix). The second part, if present, is a comma-separated list of floats that
        represent the numerical vector.

    Returns
    -------
    matrix : np.ndarray or list[list[float]]
        A 3x3 matrix whose columns are the coefficients of ``a``, ``b`` and ``c`` in
        each expression. Missing variables are treated as coefficient zero.
    vector : list[float]
        Numerical vector parsed from the second part of the input string (empty if
        omitted).

    Raises
    ------
    ValueError
        If the input string cannot be parsed, if there are not exactly three columns,
        or if any expression contains unsupported syntax.
    """
    if not isinstance(transformation_string, str):
        raise ValueError("transformation_string must be a string")

    # Split into matrix part and optional vector part
    parts = transformation_string.split(";")
    if len(parts) > 2:
        raise ValueError("Too many semicolons in transformation string")

    matrix_part = parts[0].strip()
    vector_str = parts[1].strip() if len(parts) == 2 else ""

    # Parse optional vector
    vector: List[float] = []
    if vector_str:
        try:
            vector = [float(v.strip()) for v in re.split(r",\s*", vector_str) if v]
        except Exception as exc:
            raise ValueError(f"Unable to parse numerical vector: {exc}") from exc

    # Prepare sympy symbols
    a, b, c = sp.symbols("a b c")

    # Split the matrix part into expressions (each expression is a column)
    expr_strs = [e.strip() for e in re.split(r",\s*", matrix_part) if e]
    # If the expressions were separated by commas inside a single string, we need to
    # treat each as separate column. If the user used semicolons instead, we can also
    # split on them.
    if len(expr_strs) == 1:
        expr_strs = [e.strip() for e in re.split(r";\s*", matrix_part) if e]

    if len(expr_strs) != 3:
        raise ValueError("Exactly three linear expressions are required for a 3x3 matrix")

    # Parse each expression safely with sympy
    coeffs: List[List[float]] = []
    for expr_str in expr_strs:
        try:
            # Replace caret with ** for exponentiation
            expr_str = expr_str.replace("^", "**")
            expr_sympy = sp.sympify(expr_str, locals={"a": a, "b": b, "c": c})
        except Exception as exc:
            raise ValueError(f"Unable to parse expression '{expr_str}': {exc}") from exc

        # Ensure the expression is linear in a,b,c
        if not all(
            expr_sympy.coeff(var).is_number for var in (a, b, c)
        ) or expr_sympy.as_poly([a, b, c]).total_degree() > 1:
            raise ValueError(f"Expression '{expr_str}' is not linear in a, b, c")

        coeff_a = float(expr_sympy.coeff(a))
        coeff_b = float(expr_sympy.coeff(b))
        coeff_c = float(expr_sympy.coeff(c))

        coeffs.append([coeff_a, coeff_b, coeff_c])

    # Build matrix: each expression is a column
    matrix = np.array(coeffs, dtype=float).T  # shape (3,3)

    return matrix, vector