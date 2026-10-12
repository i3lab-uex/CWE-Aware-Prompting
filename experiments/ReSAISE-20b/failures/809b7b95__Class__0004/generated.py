# -*- coding: utf-8 -*-
"""
Utility module for updating product dictionaries safely.
"""

from copy import deepcopy
from typing import Dict, Any

# Global list of fields that are allowed to be modified.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def modify_item_details(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values from ``details`` only for fields
    that are listed in :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    item :
        A dictionary representing a product.  The function does not modify the
        original ``item`` but returns a new dictionary containing the updates.
    details :
        A mapping of keys to values that should be applied to ``item``.  Keys
        not in :data:`PERMITTED_FIELDS` are ignored.

    Returns
    -------
    dict
        A new dictionary representing the updated product.

    Raises
    ------
    TypeError
        If ``item`` or ``details`` is not a dictionary.
    ValueError
        If any key in ``details`` is not present in :data:`PERMITTED_FIELDS`.
    """
    if not isinstance(item, dict):
        raise TypeError(f"item must be a dict, got {type(item).__name__}")
    if not isinstance(details, dict):
        raise TypeError(f"details must be a dict, got {type(details).__name__}")

    # Create a shallow copy to avoid mutating the original item
    updated_item = deepcopy(item)

    for key, value in details.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update.")
        updated_item[key] = value

    return updated_item