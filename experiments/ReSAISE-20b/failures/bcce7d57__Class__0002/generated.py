import re
from typing import Tuple, List, Union

import numpy as np
import sympy as sp


def parse_transformation_string(
    transformation_string: str,
) -> Tuple[Union[np.ndarray, List[List[float]]], List[float]]:
    """
    Parse a transformation string describing a 3x3 linear map and an optional
    numerical vector.

    The string is expected to have the following form::

        row1;row2;row3[;v1,v2,v3]

    * Each ``row`` is a linear expression in the symbols ``a``, ``b`` and ``c``
      (e.g. ``3*a + 4*b``, ``2*a - b`` or simply ``a``).  The expression may
      contain arbitrary whitespace and the symbols may appear in any order.
    * Rows are separated by semicolons.  The resulting matrix has the
      coefficients of ``a``, ``b`` and ``c`` in that order as its columns.
    * Optionally a numerical vector can be appended after an additional
      semicolon.  The components of this vector are separated by commas.

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

    >>> parse_transformation_string("a+2b;3c;5a-4b;1,0,2")
    (array([[1., 2., 0.],
            [0., 0., 3.],
            [5., -4., 0.]]), [1.0, 0.0, 2.0])

    Parameters
    ----------
    transformation_string : str
        The string describing the transformation.

    Returns
    -------
    tuple
        A tuple containing:
            - a 3×3 NumPy array of floats representing the linear transformation,
            - a list of floats representing the optional numerical vector.

    Raises
    ------
    ValueError
        If parsing fails or if the expression cannot be interpreted.
    """
    # Strip leading/trailing whitespace
    s = transformation_string.strip()
    if not s:
        raise ValueError("Empty transformation string")

    # Split into matrix part and optional vector part
    parts = s.split(";")
    if len(parts) < 3:
        raise ValueError("Transformation string must contain at least three rows")

    matrix_rows = parts[:3]
    vector_part: Union[str, None] = parts[3] if len(parts) > 3 else None

    # Prepare sympy symbols
    a_sym, b_sym, c_sym = sp.symbols("a b c")

    matrix_data: List[List[float]] = []

    for idx, row_expr in enumerate(matrix_rows):
        expr_str = row_expr.strip()
        if not expr_str:
            raise ValueError(f"Row {idx+1} is empty")

        try:
            expr = sp.sympify(expr_str, locals={"a": a_sym, "b": b_sym, "c": c_sym})
        except (sp.SympifyError, SyntaxError) as e:
            raise ValueError(f"Failed to parse expression '{expr_str}': {e}") from e

        # Ensure the expression is linear in a, b, c
        if not expr.is_Add and not expr.is_Mul:
            # Constant expression: treat as 0*a + 0*b + constant
            coeff_a = sp.Integer(0)
            coeff_b = sp.Integer(0)
            coeff_c = expr
        else:
            coeff_a = expr.coeff(a_sym, 1)
            coeff_b = expr.coeff(b_sym, 1)
            coeff_c = expr.coeff(c_sym, 1)

        # Convert to float
        try:
            row = [float(coeff_a), float(coeff_b), float(coeff_c)]
        except (TypeError, ValueError) as e:
            raise ValueError(
                f"Non-numeric coefficient in row {idx+1} expression '{expr_str}'"
            ) from e

        matrix_data.append(row)

    # Convert to NumPy array
    matrix = np.array(matrix_data, dtype=float)

    # Parse optional vector part
    vector: List[float] = []
    if vector_part is not None:
        vec_str = vector_part.strip()
        if vec_str:
            try:
                vector = [float(v) for v in re.split(r",\s*", vec_str)]
            except ValueError as e:
                raise ValueError(
                    f"Failed to parse vector part '{vec_str}': {e}"
                ) from e

    return matrix, vector