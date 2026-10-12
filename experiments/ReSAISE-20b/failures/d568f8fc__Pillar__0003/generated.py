# -*- coding: utf-8 -*-
"""
Product data updater.

This module provides a single function `adjust_product_data` that updates
selected fields of a product dictionary. Only the keys listed in
`PERMITTED_FIELDS` may be modified; attempting to change any other key raises a
ValueError.  The function operates in‑place and also returns the modified
dictionary for convenience.

The implementation is deliberately straightforward but includes defensive checks
to avoid accidental modification of disallowed fields, which could otherwise
lead to subtle bugs or security issues (CWE‑664).
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration: list of fields that are allowed to be updated
# --------------------------------------------------------------------------- #
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def adjust_product_data(prod_info: dict, change_vals: dict) -> dict:
    """
    Update a product dictionary with new values.

    Parameters
    ----------
    prod_info : dict
        The original product data.  It is modified in place.
    change_vals : dict
        Mapping of field names to new values.  Only keys that appear in
        ``PERMITTED_FIELDS`` are applied.

    Returns
    -------
    dict
        The updated product dictionary (the same object as ``prod_info``).

    Raises
    ------
    ValueError
        If any key in ``change_vals`` is not present in
        ``PERMITTED_FIELDS``.

    Notes
    -----
    * The function is intentionally simple to keep the control flow clear,
      which reduces the risk of resource mismanagement (CWE‑664).
    * No external libraries are required.
    """
    # Validate input types
    if not isinstance(prod_info, dict):
        raise TypeError("prod_info must be a dictionary")
    if not isinstance(change_vals, dict):
        raise TypeError("change_vals must be a dictionary")

    # Identify disallowed keys
    disallowed = set(change_vals) - set(PERMITTED_FIELDS)
    if disallowed:
        raise ValueError(
            f"Attempted to modify disallowed fields: {sorted(disallowed)}"
        )

    # Apply the allowed changes
    for key, value in change_vals.items():
        prod_info[key] = value

    return prod_info