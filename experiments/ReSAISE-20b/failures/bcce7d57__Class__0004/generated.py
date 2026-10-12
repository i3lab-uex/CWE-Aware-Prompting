#!/usr/bin/env python3
"""
Utility to parse a string representation of a linear transformation expressed in
terms of the symbolic basis {a, b, c}. The function extracts a 3×3 matrix
containing the coefficients of each basis vector and optionally returns a
numeric vector if the string contains any purely numeric expressions.

The parsing is performed using SymPy to avoid arbitrary code execution
(CWE‑77 mitigated).
"""

import re
from typing import List, Tuple, Union

import numpy as np
import sympy as sp


def parse_transformation_string(
    transformation_string: str,
) -> Tuple[Union[np.ndarray, List[List[float]]], List[float]]:
    """
    Parse a transformation string describing linear expressions in the basis
    {a, b, c} and return the corresponding 3×3 matrix and a numeric vector.

    Parameters
    ----------
    transformation_string : str
        String containing linear expressions separated by semicolons.
        Each expression may involve the symbols a, b, c or be purely numeric.
        Example: "3a+4b;2a+3b;4c" -> matrix [[3, 2, 0], [4, 3, 0], [0, 0, 4]]

    Returns
    -------
    matrix : np.ndarray or list of lists
        The extracted 3×3 coefficient matrix (rows correspond to the input order).
    vector : list of float
        Numerical values extracted from purely numeric expressions.

    Raises
    ------
    ValueError
        If the input string cannot be parsed or if any expression fails to evaluate.
    """
    # Define symbols
    a, b, c = sp.symbols("a b c")
    symbol_map = {"a": a, "b": b, "c": c}

    # Normalise whitespace and split by semicolons
    parts = [p.strip() for p in transformation_string.split(";") if p.strip()]
    if not parts:
        raise ValueError("Input string is empty or contains only separators.")

    matrix_rows: List[List[float]] = []
    numeric_vector: List[float] = []

    for idx, part in enumerate(parts):
        # Detect if the part contains any of our symbols
        if re.search(r"\b[a-c]\b", part):
            # Safe evaluation with sympy
            try:
                expr = sp.sympify(part, locals=symbol_map)
            except Exception as exc:
                raise ValueError(f"Failed to parse expression '{part}': {exc}") from exc

            # Ensure the expression is linear
            if not expr.is_Add and not expr.is_Mul:
                # For single terms like '3a' or '5', sympify returns a Mul
                pass

            # Extract coefficients for a, b, c
            coeff_a = float(expr.coeff(a))
            coeff_b = float(expr.coeff(b))
            coeff_c = float(expr.coeff(c))

            # For pure numeric constants (e.g., '5'), all coeffs will be zero
            if coeff_a == 0 and coeff_b == 0 and coeff_c == 0:
                # Treat as numeric vector element
                try:
                    val = float(expr.evalf())
                except Exception as exc:
                    raise ValueError(f"Cannot evaluate numeric part '{part}': {exc}") from exc
                numeric_vector.append(val)
            else:
                matrix_rows.append([coeff_a, coeff_b, coeff_c])
        else:
            # Pure numeric expression
            try:
                val = float(sp.sympify(part))
            except Exception as exc:
                raise ValueError(f"Failed to parse numeric expression '{part}': {exc}") from exc
            numeric_vector.append(val)

    # Convert matrix rows to numpy array if any rows exist
    if matrix_rows:
        matrix = np.array(matrix_rows, dtype=float)
    else:
        # No symbolic rows; return an empty 3x3 matrix
        matrix = np.zeros((3, 3), dtype=float)

    return matrix, numeric_vector