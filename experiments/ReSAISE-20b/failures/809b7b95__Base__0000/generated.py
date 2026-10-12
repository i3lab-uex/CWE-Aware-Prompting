#!/usr/bin/env python3
"""
Safe product detail modifier.

The function `modify_item_details` updates only those keys that are explicitly
allowed in the global list `PERMITTED_FIELDS`.  This prevents a CWE-915 style
attack where an attacker could arbitrarily set any attribute on the product.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Define the set of fields that may be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def modify_item_details(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an item dictionary with values from `details`, but only for
    fields listed in PERMITTED_FIELDS.

    Parameters
    ----------
    item : dict
        The original product dictionary. It will not be modified in place.
    details : dict
        Proposed updates. Only keys present in PERMITTED_FIELDS are applied.

    Returns
    -------
    dict
        A new dictionary representing the updated product.

    Raises
    ------
    TypeError
        If `item` or `details` is not a mapping.
    """
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary")
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary")

    # Create a shallow copy to avoid mutating the original item.
    updated_item = copy.deepcopy(item)

    for key, value in details.items():
        if key in PERMITTED_FIELDS:
            updated_item[key] = value
    return updated_item