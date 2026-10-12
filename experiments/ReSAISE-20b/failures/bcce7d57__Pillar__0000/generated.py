#!/usr/bin/env python3
"""
Utility to parse a compact textual description of a 3x3 linear transformation
and an optional translation vector.

The input format is::

    row1_expr;row2_expr;row3_expr[;vector_expr]

Each *row*_expr is a linear expression in the symbols ``a``, ``b`` and
``c`` (e.g. ``3a+4b``).  If no vector expression is supplied the
translation vector defaults to ``[0, 0, 0]``.

Examples
--------
>>> parse_transformation_string("a;b;c")
(array([[1., 0., 0.],
        [0., 1., 0.],
        [0., 0., 1.]]), [0., 0., 0.])

>>> parse_transformation_string("3a+4b;2a+3b;4c")
(array([[3., 2., 0.],
        [4., 3., 0.],
        [0., 0., 4.]]), [0., 0., 0.])

>>> parse_transformation_string("a+b+c;2b-3c;a-c;1,0,-1")
(array([[1., 1., 1.],
        [0., 2., -3.],
        [1., 0., -1.]]), [1., 0., -1.])
"""

import re
from typing import List, Tuple

import numpy as np
import sympy as sp


def _coefficients(expr: str) -> Tuple[float, float, float]:
    """
    Parse a linear expression in ``a``, ``b`` and ``c`` and return the
    coefficients (coeff_a, coeff_b, coeff_c) as floats.

    Parameters
    ----------
    expr : str
        The expression string, e.g. ``"3a+4b-2c"`.

    Returns
    -------
    Tuple[float, float, float]
        Coefficients for ``a``, ``b`` and ``c``.

    Raises
    ------
    ValueError
        If the expression cannot be parsed or contains symbols other than
        ``a``, ``b`` and ``c``.
    """
    # Normalise the expression: replace a, b, c with symbols
    try:
        a_sym, b_sym, c_sym = sp.symbols("a b c")
        # Ensure the expression is linear by checking for higher powers
        expr_sym = sp.sympify(expr, evaluate=True)
    except (sp.SympifyError, SyntaxError) as exc:
        raise ValueError(f"Unable to parse expression '{expr}': {exc}") from exc

    # Reject any symbols other than a, b, c
    if not all(sym in {a_sym, b_sym, c_sym} for sym in expr_sym.free_symbols):
        raise ValueError(f"Expression '{expr}' contains unsupported symbols: "
                         f"{expr_sym.free_symbols}")

    # Compute coefficients
    coeff_a = float(expr_sym.coeff(a_sym))
    coeff_b = float(expr_sym.coeff(b_sym))
    coeff_c = float(expr_sym.coeff(c_sym))

    return coeff_a, coeff_b, coeff_c


def _parse_vector(vec_str: str) -> List[float]:
    """
    Parse a comma‑separated numeric vector string into a list of floats.

    Parameters
    ----------
    vec_str : str
        The vector string, e.g. ``"1,-2,3.5"`.

    Returns
    -------
    List[float]
        The numeric vector.

    Raises
    ------
    ValueError
        If the vector cannot be parsed.
    """
    parts = [p.strip() for p in vec_str.split(",")]
    if len(parts) != 3:
        raise ValueError(f"Vector must have exactly three components: '{vec_str}'")
    try:
        return [float(p) for p in parts]
    except ValueError as exc:
        raise ValueError(f"Vector contains non‑numeric values: '{vec_str}'") from exc


def parse_transformation_string(transformation_string: str) -> Tuple[np.ndarray, List[float]]:
    """
    Extract a 3x3 linear transformation matrix and an optional
    translation vector from a compact string description.

    Parameters
    ----------
    transformation_string : str
        String describing the matrix rows and optionally a vector,
        e.g. ``"3a+4b;2a+3b;4c"``
        or ``"a+b+c;2b-3c;a-c;1,0,-1"``
        The separator between rows is a semicolon.  If a vector
        expression follows, it is also separated by a semicolon.

    Returns
    -------
    Tuple[np.ndarray, List[float]]
        A 3×3 NumPy array of floats representing the linear part,
        and a list of three floats representing the translation vector.

    Raises
    ------
    ValueError
        If the input string is malformed or contains unsupported syntax.
    """
    if not isinstance(transformation_string, str):
        raise ValueError("transformation_string must be a string")

    # Split into components
    parts = [p.strip() for p in transformation_string.split(";") if p.strip()]
    if not parts:
        raise ValueError("Empty transformation string")

    # The first three parts are always the matrix rows
    if len(parts) < 3:
        raise ValueError("At least three row expressions are required")
    matrix_rows = parts[:3]
    vector_part: str | None = parts[3] if len(parts) > 3 else None

    # Build matrix
    matrix_vals = []
    for expr in matrix_rows:
        coeffs = _coefficients(expr)
        matrix_vals.append(coeffs)

    matrix_np = np.array(matrix_vals, dtype=float)

    # Parse vector if present
    if vector_part is not None:
        vec = _parse_vector(vector_part)
    else:
        # Default zero vector
        vec = [0.0, 0.0, 0.0]

    return matrix_np, vec