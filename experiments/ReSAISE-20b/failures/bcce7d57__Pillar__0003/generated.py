#!/usr/bin/env python3
"""
Utility to parse a string representation of a 3x3 linear transformation matrix
and an optional numeric vector.

The input format is a semicolon-separated list of rows.  Each row can be
either:

* an algebraic expression involving the symbols `a`, `b`, and `c` (e.g.
  "3a+4b" or "a"), which represents a row of the transformation matrix, or
* a comma‑separated list of numbers (e.g. "0,0,0") which represents a numeric
  vector to be returned alongside the matrix.

Examples
--------
>>> parse_transformation_string("a;b;c")
(array([[1., 0., 0.],
       [0., 1., 0.],
       [0., 0., 1.]]), None)

>>> parse_transformation_string("3a+4b;2a+3b;4c")
(array([[ 3.,  4.,  0.],
       [ 2.,  3.,  0.],
       [ 0.,  0.,  4.]]), None)

>>> parse_transformation_string("a,b,c;0,0,0")
(array([[1., 0., 0.],
       [0., 1., 0.],
       [0., 0., 1.]]), [0., 0., 0.])

"""

import re
from typing import List, Tuple, Optional

import numpy as np
import sympy as sp


def _extract_coefficients(expr: str) -> List[float]:
    """
    Extract the coefficients of a, b, c from an algebraic expression.
    The expression may contain integers, floats, addition/subtraction,
    and multiplication by the symbols a, b, c.  No division or other
    operations are allowed.

    Parameters
    ----------
    expr : str
        The expression to parse, e.g. "3a+4b-5c".

    Returns
    -------
    List[float]
        A list [coeff_a, coeff_b, coeff_c].
    """
    # Define symbols
    a_sym, b_sym, c_sym = sp.symbols("a b c")

    # Sympy parsing: replace implicit multiplication (e.g. "3a") with explicit "*"
    # sympy can handle implicit multiplication by default, but we explicitly
    # enforce it to avoid accidental parsing of unknown tokens.
    try:
        parsed = sp.sympify(expr, evaluate=False)
    except (sp.SympifyError, TypeError) as exc:
        raise ValueError(f"Failed to parse expression '{expr}': {exc}") from exc

    # Expand and collect terms
    expanded = sp.expand(parsed)
    coeff_a = float(expanded.coeff(a_sym))
    coeff_b = float(expanded.coeff(b_sym))
    coeff_c = float(expanded.coeff(c_sym))

    # Ensure no other symbols are present
    if expanded.free_symbols - {a_sym, b_sym, c_sym}:
        raise ValueError(f"Expression '{expr}' contains unsupported symbols: "
                         f"{expanded.free_symbols - {a_sym, b_sym, c_sym}}")

    return [coeff_a, coeff_b, coeff_c]


def _is_numeric_row(row: str) -> bool:
    """
    Determine if a row string represents numeric values.
    Accepts numbers separated by commas, possibly with whitespace.
    """
    # A numeric row must contain at least one digit and no alphabetic letters
    return bool(re.search(r"\d", row)) and not re.search(r"[a-zA-Z]", row)


def parse_transformation_string(
    transformation_string: str
) -> Tuple[np.ndarray, Optional[List[float]]]:
    """
    Parse a transformation string into a 3x3 matrix and an optional numeric vector.

    Parameters
    ----------
    transformation_string : str
        A semicolon-separated list of rows.  Each row can be an algebraic
        expression involving `a`, `b`, and `c` or a comma-separated list of
        numbers.

    Returns
    -------
    Tuple[np.ndarray, Optional[List[float]]]
        The first element is a 3x3 NumPy array of floats representing the
        transformation matrix.  The second element is a list of floats
        representing the numeric vector, or ``None`` if no vector was provided.

    Raises
    ------
    ValueError
        If the input string cannot be parsed or contains invalid data.
    """
    if not isinstance(transformation_string, str):
        raise ValueError("Input must be a string")

    # Normalise whitespace and split into rows
    rows = [row.strip() for row in transformation_string.strip().split(";") if row.strip()]
    if not rows:
        raise ValueError("Input string contains no data")

    matrix_rows: List[List[float]] = []
    vector: Optional[List[float]] = None

    for row in rows:
        if _is_numeric_row(row):
            if vector is not None:
                raise ValueError("Multiple numeric vectors found")
            try:
                # Parse comma separated numbers
                vector = [float(num.strip()) for num in row.split(",") if num.strip()]
            except ValueError as exc:
                raise ValueError(f"Failed to parse numeric vector '{row}': {exc}") from exc
        else:
            # Treat as algebraic expression row
            coeffs = _extract_coefficients(row)
            matrix_rows.append(coeffs)

    if len(matrix_rows) != 3:
        raise ValueError(f"Expected exactly 3 matrix rows, got {len(matrix_rows)}")

    matrix = np.array(matrix_rows, dtype=float)

    return matrix, vector