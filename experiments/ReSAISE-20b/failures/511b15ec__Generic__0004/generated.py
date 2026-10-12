# -*- coding: utf-8 -*-

"""
Utility module for updating product information safely.

The `update_product_info` function modifies only the fields listed in
`PERMITTED_FIELDS`.  Any attempt to change a field not present in that list
raises a ValueError, ensuring that the product dictionary cannot be altered
in an unintended way.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

from typing import Dict, Any

# Define which fields are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_product_info(prod: Dict[str, Any], change_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    prod : dict
        The original product dictionary.  It is modified in place.
    change_data : dict
        A dictionary containing new values for fields that should be updated.

    Returns
    -------
    dict
        The same dictionary instance as ``prod`` after applying the updates.

    Raises
    ------
    ValueError
        If ``change_data`` contains a key that is not in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    - The function performs a shallow copy of values; if a value is itself a
      mutable object, the reference is copied.
    - The function returns the original dictionary for convenience.
    """
    # Validate that all keys in change_data are permitted
    invalid_keys = set(change_data) - set(PERMITTED_FIELDS)
    if invalid_keys:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(sorted(invalid_keys))}"
        )

    # Apply updates
    for key, value in change_data.items():
        prod[key] = value

    return prod