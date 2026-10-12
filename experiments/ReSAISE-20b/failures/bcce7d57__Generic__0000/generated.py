import re
from typing import Tuple, List

import numpy as np
import sympy


def parse_transformation_string(
    transformation_string: str,
) -> Tuple[np.ndarray, List[float]]:
    """
    Parse a string describing a linear transformation in the basis
    (a, b, c) and an optional numeric vector.

    Parameters
    ----------
    transformation_string : str
        A string of the form "expr1;expr2;...;vector" where each `expri`
        is a linear expression involving the symbols a, b and c.
        The optional `vector` part contains comma separated numbers
        and is placed after a semicolon.

    Returns
    -------
    matrix : np.ndarray
        A 2‑D NumPy array of shape (3, n) where each column corresponds
        to the coefficients of a, b and c in the corresponding expression.
    vector : list[float]
        A numeric vector parsed from the optional part of the string.

    Raises
    ------
    ValueError
        If the input cannot be parsed or contains invalid syntax.
    """
    if not isinstance(transformation_string, str):
        raise ValueError("transformation_string must be a string")

    # Split the input into expression part and optional vector part
    parts = transformation_string.strip().split(";")
    if len(parts) == 0:
        raise ValueError("Empty transformation string")

    expr_part = parts[0]
    vector_part = None
    if len(parts) > 1:
        # If there are more than one semicolon, everything after the first
        # is considered part of the vector (comma separated)
        vector_part = ";".join(parts[1:]).strip()

    # Parse expressions into columns
    exprs = [e.strip() for e in parts[0].split(";") if e.strip()]
    if not exprs:
        raise ValueError("No expressions found")

    # Regular expression to match terms like "3a", "-b", "+4c"
    term_pattern = re.compile(r"([+-]?\s*\d*\.?\d*)\s*([abc])")

    columns = []
    for expr in exprs:
        coeffs = {"a": 0.0, "b": 0.0, "c": 0.0}
        # Find all terms
        for coeff_str, var in term_pattern.findall(expr):
            coeff_str = coeff_str.replace(" ", "")
            if coeff_str in ("", "+"):
                coeff_val = 1.0
            elif coeff_str == "-":
                coeff_val = -1.0
            else:
                try:
                    # Use sympy for safe evaluation of numeric constants
                    coeff_val = float(sympy.sympify(coeff_str))
                except Exception as exc:
                    raise ValueError(f"Invalid coefficient '{coeff_str}' in expression '{expr}'.") from exc
            coeffs[var] += coeff_val

        # Build column vector (a,b,c)
        columns.append([coeffs["a"], coeffs["b"], coeffs["c"]])

    matrix = np.array(columns, dtype=float).T  # shape (3, n)

    # Parse optional vector
    vector = []
    if vector_part is not None:
        try:
            for num_str in vector_part.split(","):
                num_str = num_str.strip()
                if not num_str:
                    continue
                vector.append(float(sympy.sympify(num_str)))
        except Exception as exc:
            raise ValueError(f"Invalid vector part '{vector_part}'.") from exc

    return matrix, vector