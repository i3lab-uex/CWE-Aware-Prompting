# -*- coding: utf-8 -*-
"""
Utility module for updating product dictionaries with a whitelist of allowed fields.
"""

from copy import deepcopy
from typing import Dict, Any

# Global list of fields that are allowed to be modified.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def modify_item_details(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an item dictionary with values from ``details`` only for fields
    present in :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    item : dict
        Original product dictionary.  This dict is not modified in-place.
    details : dict
        Proposed updates for the product.

    Returns
    -------
    dict
        A new dictionary containing the updated state of the item.
    """
    if not isinstance(item, dict):
        raise TypeError("item must be a dictionary")
    if not isinstance(details, dict):
        raise TypeError("details must be a dictionary")

    # Work on a shallow copy to avoid mutating the caller's data.
    updated_item = deepcopy(item)

    for key, value in details.items():
        if key in PERMITTED_FIELDS:
            updated_item[key] = value

    return updated_item