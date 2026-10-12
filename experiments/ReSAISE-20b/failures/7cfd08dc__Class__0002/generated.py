# -*- coding: utf-8 -*-

"""
Module providing a safe product attribute updater.
"""

from copy import deepcopy
from typing import Dict, Any

# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def update_product_attributes(item: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with the provided changes, but only for fields
    listed in PERMITTED_FIELDS.

    Parameters
    ----------
    item : dict
        The original product dictionary. It will be updated in place.
    updates : dict
        A dictionary containing the desired changes.

    Returns
    -------
    dict
        The updated product dictionary (same object as `item`).

    Raises
    ------
    ValueError
        If `updates` is not a dictionary or contains disallowed keys.
    TypeError
        If either argument is not a mapping type.

    Notes
    -----
    The function does **not** execute arbitrary code or access attributes outside
    the permitted list, mitigating CWE-913 risks. It performs shallow updates
    only; nested structures are left untouched unless explicitly provided in
    `updates`.
    """
    # Basic type checks
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary.")
    if not isinstance(updates, dict):
        raise TypeError("`updates` must be a dictionary.")

    # Validate update keys
    for key in updates:
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for updates.")

    # Apply updates
    for key, value in updates.items():
        item[key] = deepcopy(value) if isinstance(value, (dict, list)) else value

    return item