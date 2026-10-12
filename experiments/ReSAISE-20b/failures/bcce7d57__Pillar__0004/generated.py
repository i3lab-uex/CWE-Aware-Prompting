import re
from typing import Tuple, List

import numpy as np
import sympy as sp


def parse_transformation_string(
    transformation_string: str,
) -> Tuple[np.ndarray, List[float]]:
    """
    Parse a string describing a 3×3 linear transformation matrix and an optional
    numeric vector.

    Parameters
    ----------
    transformation_string : str
        A string in the format ``"<expr1>;<expr2>;<expr3>[;v1,v2,v3]"`` where
        ``expri`` is a linear expression in the symbols ``a``, ``b`` and
        ``c`` (e.g. ``"3*a+4*b"``, ``"a"``, ``"0"``, etc.).  The optional part
        after the final semicolon contains a comma‑separated list of three floats.

    Returns
    -------
    matrix : numpy.ndarray
        A 3×3 array of floats representing the linear transformation.
    vector : list[float]
        The numeric vector supplied after the final semicolon, or an empty list
        if no vector is provided.

    Raises
    ------
    ValueError
        If the string cannot be parsed, contains invalid expressions,
        or if there are not exactly three linear expressions.
    """
    # ------------------------------------------------------------------
    # 1. Split the string into parts separated by ';'
    # ------------------------------------------------------------------
    if not isinstance(transformation_string, str):
        raise ValueError("Input must be a string.")

    parts = transformation_string.strip().split(";")
    if len(parts) < 3:
        raise ValueError(
            "Input must contain at least three linear expressions separated by ';'."
        )

    # The first three parts are the matrix rows
    row_exprs = parts[:3]

    # Optional vector part (if any)
    vec_part = None
    if len(parts) > 3:
        # Everything after the third semicolon is considered part of the vector
        vec_part = ";".join(parts[3:]).strip()

    # ------------------------------------------------------------------
    # 2. Prepare sympy symbols and a helper to extract coefficients
    # ------------------------------------------------------------------
    a_sym, b_sym, c_sym = sp.symbols("a b c")

    def _coefficients(expr: str) -> List[float]:
        """
        Return the coefficients [coef_a, coef_b, coef_c] for a linear
        expression in symbols a, b, c.
        """
        try:
            sym_expr = sp.sympify(expr)
        except (sp.SympifyError, TypeError) as exc:
            raise ValueError(f"Invalid expression: '{expr}'.") from exc

        # Expand and collect terms
        sym_expr = sp.expand(sym_expr)
        coeffs = [
            float(sp.collect(sym_expr, a_sym).coeff(a_sym)),
            float(sp.collect(sym_expr, b_sym).coeff(b_sym)),
            float(sp.collect(sym_expr, c_sym).coeff(c_sym)),
        ]
        return coeffs

    # ------------------------------------------------------------------
    # 3. Build the matrix
    # ------------------------------------------------------------------
    matrix_rows = []
    for expr in row_exprs:
        coeffs = _coefficients(expr)
        if len(coeffs) != 3:
            raise ValueError(f"Expression '{expr}' does not produce three coefficients.")
        matrix_rows.append(coeffs)

    matrix = np.array(matrix_rows, dtype=float)

    # ------------------------------------------------------------------
    # 4. Parse the optional vector
    # ------------------------------------------------------------------
    vector: List[float] = []
    if vec_part:
        # Remove any surrounding whitespace and split by commas
        raw_values = [v.strip() for v in vec_part.split(",")]
        if len(raw_values) != 3:
            raise ValueError(
                "Vector part must contain exactly three comma-separated numbers."
            )
        try:
            vector = [float(v) for v in raw_values]
        except ValueError as exc:
            raise ValueError("Vector contains non‑numeric values.") from exc

    return matrix, vector