import re
from typing import Tuple, List, Union

import numpy as np
import sympy as sp


def parse_transformation_string(
    transformation_string: str,
) -> Tuple[np.ndarray, List[float]]:
    """
    Parse a linear transformation string into a 3×3 matrix and an optional
    numeric vector.

    Parameters
    ----------
    transformation_string : str
        A string describing a linear transformation.  The matrix part is made of
        three rows separated by semicolons, each row being a linear expression in
        the basis symbols ``a``, ``b`` and ``c`` (e.g. ``3a+4b``).  An optional
        numeric vector can follow the matrix part, separated by a second semicolon,
        with its components comma‑separated (e.g. ``0,0,0``).

    Returns
    -------
    tuple
        (matrix, vector)
        * matrix : np.ndarray of shape (3, 3) containing the coefficients
          of ``a``, ``b`` and ``c`` in each row.
        * vector : list of floats.  If the string contains no explicit
          numeric vector, an empty list is returned.

    Raises
    ------
    ValueError
        If the input string cannot be parsed or if any expression contains
        symbols other than ``a``, ``b`` and ``c``.
    """
    # ------------------------------------------------------------------
    # 1. Basic sanity checks
    # ------------------------------------------------------------------
    if not isinstance(transformation_string, str):
        raise ValueError("transformation_string must be a string")

    # Strip whitespace and normalise separators
    s = transformation_string.strip()

    if not s:
        raise ValueError("transformation_string is empty")

    # ------------------------------------------------------------------
    # 2. Split into matrix part and optional vector part
    # ------------------------------------------------------------------
    parts = [p.strip() for p in s.split(";") if p.strip()]
    if not (2 <= len(parts) <= 3):
        raise ValueError(
            "transformation_string must contain a matrix part and "
            "(optionally) a numeric vector, separated by semicolons"
        )

    matrix_part = parts[0]
    # If there are 3 parts, the middle part is actually a second row of the matrix
    # and the last part is the vector.  If there are only 2 parts, the second part
    # is the vector.
    if len(parts) == 3:
        matrix_rows = [matrix_part, parts[1]]
        vector_str = parts[2]
    else:  # len(parts) == 2
        matrix_rows = [matrix_part]
        vector_str = parts[1]

    # ------------------------------------------------------------------
    # 3. Parse each matrix row
    # ------------------------------------------------------------------
    a, b, c = sp.symbols("a b c")
    coeff_matrix: List[List[float]] = []

    for row_expr in matrix_rows:
        # Ensure the expression contains only a,b,c and +,-,*,/,^, numbers
        if not re.fullmatch(r"[0-9a-zA-Z+\-\*/\s\^(),.]+", row_expr):
            raise ValueError(f"Invalid characters in matrix expression: '{row_expr}'")

        try:
            expr = sp.sympify(row_expr, evaluate=False)
        except Exception as exc:  # pragma: no cover
            raise ValueError(f"Failed to parse expression '{row_expr}': {exc}") from exc

        # Expand and extract coefficients
        expr = sp.expand(expr)
        coeffs = [
            float(expr.coeff(a)),
            float(expr.coeff(b)),
            float(expr.coeff(c)),
        ]
        coeff_matrix.append(coeffs)

    if len(coeff_matrix) != 3:
        raise ValueError("Matrix must have exactly three rows")

    matrix = np.array(coeff_matrix, dtype=float)

    # ------------------------------------------------------------------
    # 4. Parse numeric vector (if present)
    # ------------------------------------------------------------------
    if vector_str:
        vec_components = [comp.strip() for comp in vector_str.split(",") if comp.strip()]
        try:
            numeric_vector = [float(comp) for comp in vec_components]
        except ValueError as exc:  # pragma: no cover
            raise ValueError(f"Failed to convert numeric vector components to float: {exc}") from exc
    else:
        numeric_vector = []

    return matrix, numeric_vector