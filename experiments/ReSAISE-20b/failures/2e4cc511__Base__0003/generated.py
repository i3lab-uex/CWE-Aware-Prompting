# -*- coding: utf-8 -*-

"""
Product update module

This module defines a single public function `update_item_details` that safely updates
product attributes. Only fields listed in the global `PERMITTED_FIELDS` list are allowed to be modified.
"""

from __future__ import annotations

# Global list of fields that can be updated. Extend this list as necessary.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def update_item_details(inventory: dict, update_data: dict) -> dict:
    """
    Update a product's attributes based on `update_data`, but only allow changes to
    fields specified in the global `PERMITTED_FIELDS` list.

    Parameters
    ----------
    inventory : dict
        Dictionary representing the product. It must contain keys that match
        those in `PERMITTED_FIELDS`. The function mutates this dictionary in place.
    update_data : dict
        Dictionary containing the attributes to be updated. Only keys present in
        `PERMITTED_FIELDS` are considered; all others are ignored.

    Returns
    -------
    dict
        The updated inventory dictionary (same object as the input).

    Raises
    ------
    TypeError
        If `inventory` or `update_data` is not a dictionary.
    ValueError
        If any permitted field in `update_data` has an invalid type (e.g., non‑numeric
        value for 'price' or 'stock').

    Notes
    -----
    - This function intentionally does not modify the dictionary if a field's value
      is of an incorrect type to prevent silent corruption.
    - Fields not listed in `PERMITTED_FIELDS` are ignored, mitigating CWE‑915 risks.
    """

    if not isinstance(inventory, dict):
        raise TypeError(f"inventory must be a dict, got {type(inventory).__name__}")
    if not isinstance(update_data, dict):
        raise TypeError(f"update_data must be a dict, got {type(update_data).__name__}")

    for key, value in update_data.items():
        if key not in PERMITTED_FIELDS:
            # Skip any field that is not permitted to be updated.
            continue

        # Basic type validation for known fields
        if key == "price":
            if not isinstance(value, (int, float)):
                raise ValueError(f"Invalid type for price: {type(value).__name__}")
        elif key == "stock":
            if not isinstance(value, int):
                raise ValueError(f"Invalid type for stock: {type(value).__name__}")
        elif key in {"description", "category"}:
            if not isinstance(value, str):
                raise ValueError(f"Invalid type for {key}: {type(value).__name__}")

        # Perform the update
        inventory[key] = value

    return inventory