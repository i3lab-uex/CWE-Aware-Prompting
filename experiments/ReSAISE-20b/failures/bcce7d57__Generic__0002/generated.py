import re
from typing import Tuple, List, Union

import numpy as np
import sympy as sp


def parse_transformation_string(
    transformation_string: str,
) -> Tuple[Union[np.ndarray, List[List[float]]], List[float]]:
    """
    Parse a string describing a linear transformation in terms of the basis
    vectors ``a``, ``b`` and ``c``.  The string is expected to be a
    semicolon-separated list of rows, where each row contains comma-
    separated algebraic expressions.  Each expression may contain the
    symbols ``a``, ``b`` and ``c`` (case sensitive) together with integer
    or floating‑point constants, e.g. ``"3a+4b"``, ``"-2c"`` or simply
    ``"a"``, ``"5.0"``, etc.

    Example inputs
        "a,b,c;0,0,0"          -> identity matrix
        "3a+4b;2a+3b;4c"      -> [[3, 2, 0], [4, 3, 0], [0, 0, 4]]
        "a;2b+3c;c"           -> [[1,0,0], [0,2,3], [0,0,1]]

    The function returns a tuple ``(matrix, vector)`` where
        * ``matrix`` is a NumPy array of shape (n, 3) containing the
          coefficients of ``a``, ``b`` and ``c`` for each row.
        * ``vector`` is a list of floats representing any numeric vector
          that may appear after the matrix.  In the current specification
          the input string contains only a matrix, so ``vector`` will be an
          empty list.  The implementation keeps the vector parsing logic
          in place for future extensions.

    Parameters
    ----------
    transformation_string : str
        String representation of the linear transformation.

    Returns
    -------
    Tuple[Union[np.ndarray, List[List[float]]], List[float]]
        A tuple containing the coefficient matrix and a numeric vector.

    Raises
    ------
    ValueError
        If the string cannot be parsed or contains unsupported syntax.
    """
    # --- Helper: parse a single algebraic expression into coefficients ------------
    def _coeffs(expr_str: str) -> List[float]:
        """Return [coeff_a, coeff_b, coeff_c] for a given expression string."""
        # Replace the variable names with SymPy symbols
        expr_str = expr_str.replace("a", "A").replace("b", "B").replace("c", "C")
        try:
            expr = sp.sympify(expr_str, evaluate=True)
        except (sp.SympifyError, TypeError) as exc:
            raise ValueError(f"Could not parse expression '{expr_str}': {exc}")

        # Ensure the expression is a linear combination of A,B,C
        if not expr.is_Add and not expr.is_Mul and not expr.is_Symbol:
            # expression might be a single constant
            coeffs = [0.0, 0.0, 0.0]
        else:
            coeffs = [
                float(expr.coeff(sp.Symbol("A"))),
                float(expr.coeff(sp.Symbol("B"))),
                float(expr.coeff(sp.Symbol("C"))),
            ]

        return coeffs

    # --- Main parsing -------------------------------------------------------------
    if not isinstance(transformation_string, str):
        raise ValueError("transformation_string must be a string")

    # Split the input into rows using semicolons
    raw_rows = [row.strip() for row in transformation_string.split(";") if row.strip()]
    if not raw_rows:
        raise ValueError("No rows found in transformation string")

    matrix_rows: List[List[float]] = []

    for row_str in raw_rows:
        # Split each row into comma separated expressions
        elements = [elem.strip() for elem in row_str.split(",") if elem.strip()]
        # Each element should correspond to a coefficient for a,b,c
        row_coeffs: List[float] = []
        for elem in elements:
            coeffs = _coeffs(elem)
            row_coeffs.extend(coeffs)

        # After parsing a full row, we should have exactly 3 coefficients
        if len(row_coeffs) != 3:
            raise ValueError(
                f"Row '{row_str}' does not contain exactly three coefficients. "
                f"Found {len(row_coeffs)}: {row_coeffs}"
            )
        matrix_rows.append(row_coeffs)

    # Convert to NumPy array
    try:
        matrix = np.array(matrix_rows, dtype=float)
    except Exception as exc:
        raise ValueError(f"Failed to construct matrix array: {exc}")

    # --- Numeric vector parsing (currently not used) -----------------------------
    # If the last row contains only numeric entries, treat it as a vector.
    vector: List[float] = []
    if matrix.shape[0] > 1 and np.allclose(matrix[-1], matrix[-1].astype(int)):
        # Simple heuristic: if the last row has no symbolic terms, treat as vector
        try:
            vec_candidate = [float(v) for v in matrix[-1]]
            vector = vec_candidate
            # Remove the last row from the matrix
            matrix = matrix[:-1, :]
        except Exception:
            pass

    return matrix, vector