#!/usr/bin/env python3
"""
update_item_details module

This module provides a single function `update_item_details` which safely updates
product attributes in an inventory dictionary. Only the keys listed in the
global `PERMITTED_FIELDS` are allowed to be modified.

The implementation follows the principles of CWE‑915 protection by explicitly
controlling which attributes may be altered, rejecting any attempt to modify
unpermitted fields.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# List of attributes that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def update_item_details(inventory: dict, update_data: dict) -> dict:
    """
    Update a product's attributes in the given inventory dictionary.

    Parameters
    ----------
    inventory : dict
        The original product dictionary. Must contain the keys listed in
        `PERMITTED_FIELDS`. Existing values will be overwritten by those
        supplied in ``update_data`` when permitted.
    update_data : dict
        A dictionary of key/value pairs intended for updating the product.

    Returns
    -------
    dict
        The updated inventory dictionary. The function modifies ``inventory``
        in place and also returns it for convenience.

    Raises
    ------
    TypeError
        If ``inventory`` or ``update_data`` is not a dictionary.
    ValueError
        If any key in ``update_data`` is not present in `PERMITTED_FIELDS`.
    """
    if not isinstance(inventory, dict):
        raise TypeError("inventory must be a dictionary")
    if not isinstance(update_data, dict):
        raise TypeError("update_data must be a dictionary")

    # Identify any disallowed keys
    forbidden_keys = [k for k in update_data if k not in PERMITTED_FIELDS]
    if forbidden_keys:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(forbidden_keys)}"
        )

    # Apply permitted updates
    for key, value in update_data.items():
        inventory[key] = value

    return inventory


# --------------------------------------------------------------------------- #
# Example usage (removed when imported as a module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Example product
    product = {
        "price": 19.99,
        "description": "A useful gadget",
        "stock": 50,
        "category": "Tools",
    }

    # Example update data
    new_data = {
        "price": 17.99,
        "stock": 45,
    }

    try:
        updated_product = update_item_details(product, new_data)
        print("Updated product:", updated_product)
    except Exception as exc:
        print(f"Error: {exc}")