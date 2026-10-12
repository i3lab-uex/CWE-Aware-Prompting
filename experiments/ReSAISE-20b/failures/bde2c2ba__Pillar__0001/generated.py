#!/usr/bin/env python3
"""
Module: product_update

This module provides a single function `update_item_information` that safely updates
attributes of a product dictionary. Only fields listed in the global `PERMITTED_FIELDS`
are allowed to be modified.

Security considerations:
* A deep copy of the original product is created to avoid side‑effects on the caller.
* Attempts to modify disallowed fields raise a `ValueError` immediately.
* The function is defensive against missing keys and type mismatches.

CWE-664 (Improper Control of a Resource Through its Lifetime) is mitigated by
ensuring that the product dictionary is never modified in place, thus preventing
unexpected resource state changes.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Only these fields may be updated by `update_item_information`.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def update_item_information(product_info: Dict[str, Any],
                            new_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with permitted fields updated.

    Parameters
    ----------
    product_info : dict
        The original product data. Must be a mapping of string keys to any values.
    new_data : dict
        Dictionary containing updates. Only keys in PERMITTED_FIELDS are applied.

    Returns
    -------
    dict
        A new dictionary representing the updated product state.

    Raises
    ------
    ValueError
        If `new_data` contains a key not present in PERMITTED_FIELDS.
    TypeError
        If either argument is not a dictionary.

    Examples
    --------
    >>> original = {'price': 10, 'description': 'Old', 'stock': 5}
    >>> updates = {'price': 12, 'category': 'Books'}
    >>> update_item_information(original, updates)
    {'price': 12, 'description': 'Old', 'stock': 5, 'category': 'Books'}
    """
    if not isinstance(product_info, dict):
        raise TypeError("product_info must be a dictionary")
    if not isinstance(new_data, dict):
        raise TypeError("new_data must be a dictionary")

    # Create a deep copy to avoid mutating the original input
    updated_product = copy.deepcopy(product_info)

    for key, value in new_data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update")
        updated_product[key] = value

    return updated_product