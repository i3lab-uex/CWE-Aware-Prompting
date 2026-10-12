import re
from typing import Tuple, List, Union

import numpy as np
import sympy as sp


def parse_transformation_string(
    transformation_string: str,
) -> Tuple[np.ndarray, List[float]]:
    """
    Parse a string that describes a 3×3 linear transformation matrix and an optional
    numerical vector.

    The input string is expected to contain one or two parts separated by a semicolon.
    * Part 1 – the matrix: three rows of linear expressions involving the symbols
      ``a``, ``b`` and ``c``.  Rows are separated by commas.
    * Part 2 – the vector: three comma‑separated numeric values.

    Examples
    --------
    >>> parse_transformation_string("a;b;c")
    (array([[1., 0., 0.],
            [0., 1., 0.],
            [0., 0., 1.]]), [])

    >>> parse_transformation_string("3a+4b;2a+3b;4c")
    (array([[3., 2., 0.],
            [4., 3., 0.],
            [0., 0., 4.]]), [])

    Parameters
    ----------
    transformation_string : str
        The string to parse.

    Returns
    -------
    tuple[np.ndarray, list[float]]
        The first element is a 3×3 NumPy array of floats.
        The second element is a list containing the numerical vector
        (empty if not provided).

    Raises
    ------
    ValueError
        If the input string cannot be parsed or contains invalid expressions.
    """
    # ---------- Helper functions ----------
    _a, _b, _c = sp.symbols("a b c")

    def _parse_row(row: str) -> List[float]:
        """
        Parse a single row expression (e.g. "3a+4b-2c") into
        a list of coefficients [coeff_a, coeff_b, coeff_c].
        """
        # Ensure only allowed characters appear
        if not re.fullmatch(r"[0-9\.\+\-\*\/aAbBc\s]+", row):
            raise ValueError(f"Invalid characters in expression: {row!r}")

        # Replace commas with spaces and remove whitespace
        expr = row.replace(",", " ").replace(" ", "")
        # sympify with predefined symbols
        try:
            sym_expr = sp.sympify(expr, locals={"a": _a, "b": _b, "c": _c})
        except (sp.SympifyError, TypeError) as exc:
            raise ValueError(f"Failed to parse expression {row!r}") from exc

        # Linear expressions only
        if not sym_expr.is_Add and not sym_expr.is_Mul and sym_expr != 0:
            # could be a single symbol or constant
            pass

        coeffs = [sp.N(sym_expr.coeff(_a)), sp.N(sym_expr.coeff(_b)),
                  sp.N(sym_expr.coeff(_c))]
        return [float(c) for c in coeffs]

    def _parse_vector(vec_str: str) -> List[float]:
        """Parse a comma‑separated list of numbers into floats."""
        if not vec_str.strip():
            return []
        parts = [p.strip() for p in vec_str.split(",")]
        if len(parts) != 3:
            raise ValueError("Vector must contain exactly three numbers.")
        vec = []
        for part in parts:
            try:
                vec.append(float(part))
            except ValueError as exc:
                raise ValueError(f"Invalid numeric value in vector: {part!r}") from exc
        return vec

    # ---------- Main parsing ----------
    try:
        parts = [p.strip() for p in transformation_string.split(";")]
        if not parts or len(parts) > 2:
            raise ValueError("Transformation string must contain one or two parts separated by a single ';'.")

        # Parse matrix rows
        matrix_rows = []
        for row_str in parts[0].split(","):
            if not row_str:
                continue
            matrix_rows.append(_parse_row(row_str))

        # Validate shape: must be 3x3
        if len(matrix_rows) != 3 or any(len(r) != 3 for r in matrix_rows):
            raise ValueError("Matrix must be 3×3 linear expressions.")

        matrix = np.array(matrix_rows, dtype=float)

        # Parse optional vector
        vector = []
        if len(parts) == 2:
            vector = _parse_vector(parts[1])

    except Exception as exc:
        raise ValueError(f"Failed to parse transformation string: {transformation_string!r}") from exc

    return matrix, vector