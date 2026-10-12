import re
from typing import Tuple, List, Union

import numpy as np
import sympy as sp


def parse_transformation_string(
    transformation_string: str,
) -> Tuple[Union[np.ndarray, List[List[float]]], List[float]]:
    """
    Parse a string that defines a linear transformation in terms of the basis
    symbols ``a``, ``b`` and ``c``.  Each row of the transformation matrix is
    separated by a semicolon.

    Parameters
    ----------
    transformation_string : str
        A string such as ``"a;b;c"``, ``"3a+4b;2a+3b;4c"``, or any other
        combination of linear expressions involving ``a``, ``b`` and ``c``.

    Returns
    -------
    tuple
        * A 2‑D NumPy array (or a nested list) containing the matrix of
          coefficients for ``a``, ``b`` and ``c``.
        * A list of floats representing the numerical vector that may appear
          after a semicolon.  In most examples this list is empty.

    Raises
    ------
    ValueError
        If the string cannot be parsed or contains invalid expressions.
    """
    if not isinstance(transformation_string, str):
        raise ValueError("transformation_string must be a string")

    # Strip whitespace and split rows by semicolon
    rows = [row.strip() for row in transformation_string.split(";") if row.strip()]
    if not rows:
        raise ValueError("transformation_string contains no valid rows")

    # Prepare symbols for sympy
    a, b, c = sp.symbols("a b c")

    matrix_rows: List[List[float]] = []
    numeric_vector: List[float] = []

    # Regular expression to capture a possible trailing numeric vector
    vector_pattern = re.compile(r"^\s*(-?\d+(?:\.\d+)?(?:e[+-]?\d+)?)\s*$")

    for row in rows:
        # Check if the row is a numeric vector
        vec_match = vector_pattern.match(row)
        if vec_match:
            numeric_vector.append(float(vec_match.group(1)))
            continue

        # Safely parse the linear expression
        try:
            expr = sp.sympify(row, evaluate=False)
        except (sp.SympifyError, SyntaxError) as exc:
            raise ValueError(f"Could not parse expression '{row}': {exc}") from exc

        # Ensure the expression is linear in a, b, c
        if not all(expr.has(sym) or expr == 0 for sym in (a, b, c)):
            # If expression is a constant or contains other symbols
            if expr.is_Number:
                coeffs = [0.0, 0.0, 0.0]
            else:
                raise ValueError(f"Expression '{row}' contains unsupported symbols")
        else:
            coeffs = [
                float(expr.coeff(a)),
                float(expr.coeff(b)),
                float(expr.coeff(c)),
            ]

        matrix_rows.append(coeffs)

    if not matrix_rows:
        raise ValueError("No valid transformation rows found")

    matrix = np.array(matrix_rows, dtype=float)

    return matrix, numeric_vector