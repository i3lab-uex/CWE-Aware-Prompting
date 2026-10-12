# -*- coding: utf-8 -*-
"""
Product inventory update module.

This module provides a single function, :func:`update_item_details`,
which updates product attributes in an inventory dictionary. Only
attributes listed in the global ``PERMITTED_FIELDS`` are allowed to be
modified.  The implementation protects against CWE‑915 by explicitly
checking each key before assignment and rejecting any disallowed keys.
"""

from typing import Dict, Any

# Define the list of attributes that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_item_details(inventory: Dict[str, Any], update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an inventory item's attributes with values from ``update_data``.

    Parameters
    ----------
    inventory : dict
        The original product dictionary.  It is modified in place and also returned.
    update_data : dict
        Dictionary containing fields to be updated.

    Returns
    -------
    dict
        The same dictionary object, now containing the applied updates.

    Raises
    ------
    ValueError
        If ``update_data`` contains any keys that are not in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    - The function performs a shallow update; nested dictionaries are not deep‑merged.
    - No external libraries are used, ensuring minimal attack surface.

    Example
    -------
    >>> product = {"price": 10.0, "description": "Old", "stock": 5}
    >>> update_item_details(product, {"price": 12.0, "stock": 3})
    {'price': 12.0, 'description': 'Old', 'stock': 3}
    """
    # Identify disallowed keys
    invalid_keys = [key for key in update_data if key not in PERMITTED_FIELDS]
    if invalid_keys:
        raise ValueError(f"Attempted to update disallowed fields: {invalid_keys}")

    # Apply permitted updates
    for key in PERMITTED_FIELDS:
        if key in update_data:
            inventory[key] = update_data[key]

    return inventory