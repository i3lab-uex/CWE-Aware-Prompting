import re
from typing import Tuple, List, Union

import numpy as np
import sympy as sp


def parse_transformation_string(
    transformation_string: str,
) -> Tuple[Union[List[List[float]], np.ndarray], List[float]]:
    """
    Parse a string describing a linear transformation expressed in the
    basis `{a, b, c}`.

    Parameters
    ----------
    transformation_string : str
        The string to parse. It may contain one or more linear expressions
        separated by semicolons.  Each expression is a linear combination of
        `a`, `b` and/or `c`.  Example: `"3a+4b;2a+3b;4c"`.
        Optionally a numeric vector may follow the matrix, e.g.
        `"3a+4b;2a+3b;4c;1,0,-1"`.

    Returns
    -------
    matrix : np.ndarray or list[list[float]]
        The 3×3 transformation matrix.  Each row corresponds to one
        expression in the input string.
    vector : list[float]
        The numeric vector that follows the matrix (empty if none).

    Raises
    ------
    ValueError
        If the string cannot be parsed or contains malformed expressions.
    """
    # Helper: create sympy symbols
    a, b, c = sp.symbols("a b c")

    # Split the string into semicolon separated parts
    parts = [p.strip() for p in transformation_string.split(";") if p.strip()]
    if not parts:
        raise ValueError("Empty transformation string")

    matrix_rows: List[List[float]] = []
    vector_part: List[float] = []

    # Regular expression to detect numeric-only parts
    num_only_re = re.compile(r"^[\d\s.,-]+$")

    for part in parts:
        # Determine if the part is a numeric vector (no letters)
        if not re.search(r"[abc]", part):
            # Attempt to parse numeric vector
            try:
                nums = [
                    float(x.strip())
                    for x in part.replace(",", " ").split()
                    if x.strip() != ""
                ]
            except ValueError as exc:
                raise ValueError(f"Cannot parse numeric vector: '{part}'") from exc
            if not nums:
                raise ValueError(f"Empty numeric vector: '{part}'")
            vector_part.extend(nums)
        else:
            # Parse the linear expression
            try:
                expr = sp.sympify(part, locals={"a": a, "b": b, "c": c})
            except (sp.SympifyError, TypeError) as exc:
                raise ValueError(f"Cannot parse expression: '{part}'") from exc

            # Expand to ensure linearity
            expr = sp.expand(expr)

            # Extract coefficients for a, b, c
            coeffs = [
                float(sp.expand(expr).coeff(sym)) for sym in (a, b, c)
            ]
            matrix_rows.append(coeffs)

    if not matrix_rows:
        raise ValueError("No matrix rows found in the transformation string")

    # Convert to numpy array
    matrix = np.array(matrix_rows, dtype=float)

    return matrix, vector_part