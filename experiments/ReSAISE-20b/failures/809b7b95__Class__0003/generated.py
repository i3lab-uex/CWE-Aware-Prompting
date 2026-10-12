#!/usr/bin/env python3
"""
Product detail modification module.

This module defines a single public function, `modify_item_details`, which
updates an existing product dictionary with new values supplied in a second
dictionary.  Only keys that are present in the global `PERMITTED_FIELDS`
set are allowed to be modified; any attempt to change a disallowed field
results in a `ValueError`.  The function returns a new dictionary instance
containing the updated product data, leaving the original `item` unchanged.

The implementation follows safe coding practices to avoid
CWE-913 (Improper Control of Dynamically‑Managed Code Resources) by
explicitly whitelisting the attributes that may be modified.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Global whitelist of fields that may be modified.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def modify_item_details(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing product dictionary with new values.

    Parameters
    ----------
    item : dict
        The original product data.  It must be a dictionary containing at least the keys
        present in `PERMITTED_FIELDS`.  The function does not modify this dictionary.
    details : dict
        A mapping of field names to new values.  Only keys that exist in
        `PERMITTED_FIELDS` are processed; all others cause a ValueError.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.

    Raises
    ------
    ValueError
        If `details` contains a key that is not in `PERMITTED_FIELDS`.

    Examples
    --------
    >>> product = {"price": 10.0, "description": "old", "stock": 5, "category": "books"}
    >>> updates = {"price": 12.0, "stock": 3}
    >>> modify_item_details(product, updates)
    {'price': 12.0, 'description': 'old', 'stock': 3, 'category': 'books'}
    """
    # Validate that all keys in details are permitted.
    disallowed = set(details) - PERMITTED_FIELDS
    if disallowed:
        raise ValueError(f"Attempted to modify disallowed fields: {sorted(disallowed)}")

    # Create a shallow copy of the original item to avoid side effects.
    updated_item = copy.deepcopy(item)

    # Apply each permitted update.
    for key, value in details.items():
        updated_item[key] = value

    return updated_item