#!/usr/bin/env python3
"""
Utility module for updating product details in an inventory.

The module defines a global list `PERMITTED_FIELDS` that specifies which
product attributes may be modified.  The function `update_item_details`
accepts an inventory dictionary and a dictionary of updates, applies
only the permitted changes, and returns the updated product.

The implementation avoids any form of dynamic code execution or
unrestricted attribute manipulation, mitigating risks such as CWE‑913.
"""

from __future__ import annotations

# List of fields that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_item_details(inventory: dict, update_data: dict) -> dict:
    """
    Update an inventory item with the provided data.

    Parameters
    ----------
    inventory : dict
        Dictionary representing the product.  It must contain keys for all
        attributes that can be updated.
    update_data : dict
        Dictionary containing the fields to update and their new values.

    Returns
    -------
    dict
        The updated product dictionary.  Only keys present in
        `PERMITTED_FIELDS` are modified; all other keys are ignored.

    Notes
    -----
    - The function does **not** modify the original `inventory` dictionary in place;
      it returns a new dictionary with the applied changes.  This prevents accidental
      side‑effects on caller references.
    - If a field in `update_data` is not in `PERMITTED_FIELDS`, it is silently
      ignored.  This behavior can be changed to raise an exception if stricter
      validation is desired.
    """
    # Create a shallow copy to avoid mutating the original inventory
    updated_item = inventory.copy()

    for key, value in update_data.items():
        if key in PERMITTED_FIELDS:
            updated_item[key] = value

    return updated_item