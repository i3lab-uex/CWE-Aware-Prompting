# -*- coding: utf-8 -*-
"""
Utility for safely updating product data.

The module defines a single public function `adjust_product_data` that updates only
fields listed in the global `PERMITTED_FIELDS`.  Any attempt to modify
non‑permitted fields is ignored.  The function returns the updated product
dictionary.

The implementation follows best practices for security and data integrity:
* Input dictionaries are shallow‑copied to avoid accidental mutation of caller
  objects.
* The function validates that `change_vals` is a dictionary before proceeding.
* Keys not present in `PERMITTED_FIELDS` are silently ignored – this protects
  against accidental or malicious tampering of sensitive product attributes.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# Only these fields may be updated by `adjust_product_data`.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def adjust_product_data(prod_info: dict, change_vals: dict) -> dict:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    prod_info : dict
        The original product dictionary.  Keys represent product attributes.
    change_vals : dict
        A mapping of field names to new values that should be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.  The original
        `prod_info` is not modified.

    Raises
    ------
    TypeError
        If either `prod_info` or `change_vals` is not a dictionary.
    """
    if not isinstance(prod_info, dict):
        raise TypeError("prod_info must be a dictionary")
    if not isinstance(change_vals, dict):
        raise TypeError("change_vals must be a dictionary")

    # Work on a shallow copy to avoid side effects.
    updated_product = prod_info.copy()

    for key, value in change_vals.items():
        if key in PERMITTED_FIELDS:
            updated_product[key] = value
        else:
            # Ignoring disallowed fields protects against unintended modifications.
            continue

    return updated_product