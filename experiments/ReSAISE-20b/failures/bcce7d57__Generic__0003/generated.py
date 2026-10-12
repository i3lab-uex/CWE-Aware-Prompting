import re
from typing import Tuple, List

import numpy as np
import sympy as sp


def parse_transformation_string(transformation_string: str) -> Tuple[np.ndarray, List[float]]:
    """
    Parse a transformation string describing a 3×3 linear transformation
    expressed in the basis (a, b, c) and return a NumPy matrix of floats
    together with an optional numerical vector.

    Parameters
    ----------
    transformation_string : str
        A string such as:
            "a;b;c"                -> identity matrix
            "3a+4b;2a+3b;4c"      -> [[3, 2, 0], [4, 3, 0], [0, 0, 4]]
            "a,b,c;1,2,3"          -> matrix with rows [1,0,0], [0,1,0], [0,0,1] and vector [1,2,3]
        Rows are separated by semicolons.  Within a row the
        expressions for the coefficients of a, b and c are either:
            * one expression – it is taken as the coefficient for `a`
              and the others are set to zero,
            * three comma‑separated expressions – they correspond
              respectively to the coefficients of a, b and c.

    Returns
    -------
    matrix : np.ndarray
        A 3×3 NumPy array of floats.
    vector : list[float]
        The numerical vector that may follow the matrix part,
        or an empty list if none is provided.

    Raises
    ------
    ValueError
        If the string cannot be parsed or contains invalid expressions.
    """
    try:
        # Split into matrix part and optional vector part
        parts = transformation_string.split(';')
        if not parts:
            raise ValueError("Empty transformation string")

        # Detect whether the last part is a numeric vector (comma separated numbers)
        vector: List[float] = []
        if len(parts) > 3:
            # The last part should contain numbers only
            vector_part = parts[-1]
            if re.fullmatch(r'(\s*-?\d+\.?\d*(e[+-]?\d+)?\s*,)*\s*-?\d+\.?\d*(e[+-]?\d+)?', vector_part):
                vector = [float(x) for x in vector_part.split(',')]
                parts = parts[:-1]  # remove the vector part from matrix rows
            else:
                raise ValueError("Vector part is not a comma‑separated list of numbers")

        if len(parts) != 3:
            raise ValueError("Matrix part must contain exactly three rows")

        # Define symbols for sympy
        a, b, c = sp.symbols('a b c')

        matrix_rows = []
        for row_str in parts:
            # Split the row into expressions
            exprs = [e.strip() for e in row_str.split(',') if e.strip()]
            coeffs: List[float] = []

            # Helper to evaluate an expression safely
            def eval_expr(expr: str) -> sp.Expr:
                return sp.sympify(expr, locals={'a': a, 'b': b, 'c': c})

            if len(exprs) == 1:
                # Single expression -> coefficient for a
                expr = eval_expr(exprs[0])
                coeff_a = float(expr.expand().coeff(a))
                coeff_b = 0.0
                coeff_c = 0.0
                coeffs.extend([coeff_a, coeff_b, coeff_c])
            elif len(exprs) == 3:
                for e in exprs:
                    coeff = float(eval_expr(e).expand().coeff(a) +
                                   eval_expr(e).expand().coeff(b) * 0 +  # placeholder
                                   eval_expr(e).expand().coeff(c) * 0)
                # We actually need coefficients of a, b, c separately
                coeff_a = float(eval_expr(exprs[0]).expand().coeff(a))
                coeff_b = float(eval_expr(exprs[1]).expand().coeff(b))
                coeff_c = float(eval_expr(exprs[2]).expand().coeff(c))
                coeffs.extend([coeff_a, coeff_b, coeff_c])
            else:
                raise ValueError(f"Row '{row_str}' must contain 1 or 3 expressions")

            matrix_rows.append(coeffs)

        matrix = np.array(matrix_rows, dtype=float)
        return matrix, vector

    except Exception as exc:
        raise ValueError(f"Failed to parse transformation string: {exc}") from exc