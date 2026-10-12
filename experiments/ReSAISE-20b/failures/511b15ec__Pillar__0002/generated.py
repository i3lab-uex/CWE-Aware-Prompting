# -*- coding: utf-8 -*-

"""
Utility module for updating product information safely.

The module defines a single function, `update_product_info`, which applies
changes to an existing product dictionary.  Only keys that are listed in the
globally defined `PERMITTED_FIELDS` may be modified.  This helps prevent
unintended changes to critical fields and protects against accidental
overwrites.

CWE-664 (Improper Control of a Resource Through its Lifetime) is mitigated by
ensuring that the product dictionary is not modified in place unless it is
explicitly allowed.  A shallow copy of the product is created and returned,
leaving the original object unchanged unless the caller assigns the result
back to it.  This approach avoids side‑effects that could lead to resource
leakage or inconsistent state.
"""

from __future__ import annotations

from typing import Dict, Any

# List of fields that may be updated.  Add or remove entries as needed.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def update_product_info(prod: Dict[str, Any], change_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with the permitted fields updated.

    Parameters
    ----------
    prod : dict
        The original product representation.  It may contain any keys.
    change_data : dict
        A dictionary of fields to be updated.  Only those present in
        ``PERMITTED_FIELDS`` are applied.

    Returns
    -------
    dict
        A new dictionary that contains the updated values.  The original
        ``prod`` is left untouched.

    Raises
    ------
    ValueError
        If `change_data` contains a key that is not in ``PERMITTED_FIELDS``.
    """
    # Validate incoming changes
    for key in change_data:
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Attempt to modify unpermitted field: {key!r}")

    # Create a shallow copy to avoid mutating the original product
    updated_prod = prod.copy()

    # Apply permitted updates
    for key, value in change_data.items():
        updated_prod[key] = value

    return updated_prod