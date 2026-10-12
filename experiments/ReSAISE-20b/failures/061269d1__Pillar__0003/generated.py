# -*- coding: utf-8 -*-
"""
Utility to update product information while enforcing a whitelist of permitted fields.
"""

from copy import deepcopy
from typing import Dict, Any

# List of product attributes that are allowed to be modified.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def edit_product_info(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with the values provided in ``details``.
    
    Only keys that are present in :data:`PERMITTED_FIELDS` will be applied.  Keys not
    listed in the whitelist are ignored to avoid accidental or malicious changes.
    
    Parameters
    ----------
    item : dict
        The original product dictionary.  This object is **not** modified in place;
        a shallow copy of the relevant data is returned.
    details : dict
        The dictionary containing proposed updates.  Keys that are not in the
        whitelist are silently ignored.
    
    Returns
    -------
    dict
        A new dictionary containing the original product data with permitted
        updates applied.
    
    Raises
    ------
    TypeError
        If either ``item`` or ``details`` is not a mapping.
    """
    if not isinstance(item, dict):
        raise TypeError(f"Expected 'item' to be a dict, got {type(item).__name__}")
    if not isinstance(details, dict):
        raise TypeError(f"Expected 'details' to be a dict, got {type(details).__name__}")

    # Work on a shallow copy to avoid mutating the caller's dictionary.
    updated_item = deepcopy(item)

    # Apply only permitted fields
    for key, value in details.items():
        if key in PERMITTED_FIELDS:
            updated_item[key] = value
    return updated_item