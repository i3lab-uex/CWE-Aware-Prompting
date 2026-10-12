import numpy as np
import re
from sympy import sympify, Symbol

def parse_transformation_string(transformation_string: str):
    """
    Parse a string describing a 3x3 linear transformation matrix and an optional
    numeric vector. The matrix is expressed as three rows of linear expressions in
    the symbols ``a``, ``b`` and ``c``. Rows are separated by semicolons (`;`).
    If a numeric vector is supplied it follows the matrix rows and its entries
    are separated by commas.

    Parameters
    ----------
    transformation_string : str
        String in the form:
            "a;b;c"                           -> identity matrix
            "3a+4b;2a+3b;4c"                  -> [[3, 2, 0],[4, 3, 0],[0,0,4]]
            "a;b;c;1,2,3"                     -> matrix + vector

    Returns
    -------
    tuple (np.ndarray, list[float])
        - The 3×3 transformation matrix as a NumPy array of floats.
        - A list of floats representing the numeric vector (empty if not provided).

    Raises
    ------
    ValueError
        If the string cannot be parsed or contains invalid expressions.
    """
    # Remove whitespace and standardise separator
    s = transformation_string.strip().replace(" ", "")
    if not s:
        raise ValueError("Input string is empty")

    # Split into rows
    parts = s.split(';')
    if len(parts) < 3:
        raise ValueError("At least three rows are required for a 3x3 matrix")

    # First three parts are the matrix rows
    matrix_rows = parts[:3]
    vector_part = None
    if len(parts) > 3:
        vector_part = parts[3]

    # Helper: parse a single linear expression into coeffs of a,b,c
    def _parse_expr(expr):
        # Define symbols
        a, b, c = Symbol('a'), Symbol('b'), Symbol('c')
        try:
            sym_expr = sympify(expr, evaluate=False)
        except Exception as exc:
            raise ValueError(f"Failed to parse expression '{expr}': {exc}") from exc

        # Ensure it's linear
        if not sym_expr.is_Add and not sym_expr.is_Mul and not sym_expr.is_Symbol:
            # Could be a number
            coeffs = {a:0, b:0, c:0}
        else:
            coeffs = {a:0, b:0, c:0}
            # Expand to sum of terms
            for term in sym_expr.as_ordered_terms():
                coeff = 1
                if isinstance(term, Symbol):
                    # pure symbol term
                    pass
                elif term.is_Number:
                    coeff = float(term)
                    continue
                else:
                    # product
                    muls = term.as_ordered_factors()
                    coeff_val = 1
                    for f in muls:
                        if f.is_Number:
                            coeff_val *= float(f)
                        elif f == a or f == b or f == c:
                            # keep variable
                            pass
                        else:
                            raise ValueError(f"Unsupported factor '{f}' in term '{term}'")
                    coeff = coeff_val
                # Determine variable part
                vars_in_term = [v for v in (a, b, c) if v in term.free_symbols]
                if not vars_in_term:
                    # constant term, ignore
                    continue
                var = vars_in_term[0]
                coeffs[var] += float(coeff)
        return [float(coeffs[a]), float(coeffs[b]), float(coeffs[c])]

    matrix = []
    for row_expr in matrix_rows:
        coeffs = _parse_expr(row_expr)
        if len(coeffs) != 3:
            raise ValueError(f"Expression '{row_expr}' did not yield three coefficients")
        matrix.append(coeffs)

    mat_np = np.array(matrix, dtype=float)

    # Parse numeric vector if present
    vec = []
    if vector_part is not None:
        try:
            vec = [float(v) for v in vector_part.split(',') if v]
        except Exception as exc:
            raise ValueError(f"Failed to parse numeric vector '{vector_part}': {exc}") from exc

    return mat_np, vec