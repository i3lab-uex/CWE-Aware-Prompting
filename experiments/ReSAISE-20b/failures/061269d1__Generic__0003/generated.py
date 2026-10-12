# -*- coding: utf-8 -*-
"""
Utility for updating product dictionaries with a whitelist of editable fields.
"""

from typing import Dict, Any

# Fields that are allowed to be modified
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def edit_product_info(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    item : dict
        The original product data.
    details : dict
        A dictionary of fields and new values to apply.

    Returns
    -------
    dict
        The updated product dictionary.  The original `item` is modified in place.

    Raises
    ------
    ValueError
        If any key in `details` is not listed in :data:`PERMITTED_FIELDS`.
    TypeError
        If either `item` or `details` is not a dictionary.
    """
    if not isinstance(item, dict):
        raise TypeError(f"Expected 'item' to be a dict, got {type(item).__name__}")
    if not isinstance(details, dict):
        raise TypeError(f"Expected 'details' to be a dict, got {type(details).__name__}")

    # Identify disallowed keys
    disallowed = set(details) - PERMITTED_FIELDS
    if disallowed:
        raise ValueError(f"Attempted to modify forbidden fields: {', '.join(disallowed)}")

    # Apply permitted updates
    for key, value in details.items():
        item[key] = value

    return item