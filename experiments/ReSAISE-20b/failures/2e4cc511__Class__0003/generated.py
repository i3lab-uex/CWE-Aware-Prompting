# -*- coding: utf-8 -*-
"""
Product inventory update module.

This module defines a single public function, `update_item_details`, which
updates an inventory item dictionary with new values supplied in a second
dictionary.  Only the keys listed in the global `PERMITTED_FIELDS` list are
allowed to be modified; all other keys in `update_data` are ignored.

The function performs basic type validation for the fields that are
permitted to be updated.  It does not execute arbitrary code or use any
dangerous built‑ins, thereby avoiding CWE‑913 (Improper Control of
Dynamically‑Managed Code Resources).

Author: ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration – list of fields that may be updated
# --------------------------------------------------------------------------- #
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

# Optional type hints for each permitted field (used for basic validation)
FIELD_TYPES = {
    "price": (int, float),      # price must be a number
    "description": str,         # description must be a string
    "stock": int,               # stock must be an integer
    "category": str,            # category must be a string
}


def _validate_field(field: str, value) -> bool:
    """
    Validate a single field against its expected type(s).

    Parameters
    ----------
    field : str
        The name of the field to validate.
    value :
        The new value supplied for the field.

    Returns
    -------
    bool
        True if the value is of an allowed type, False otherwise.
    """
    expected = FIELD_TYPES.get(field)
    if expected is None:
        # Unknown field – should never happen because we filter earlier
        return False

    if isinstance(expected, tuple):
        return isinstance(value, expected)
    else:
        return isinstance(value, expected)


def update_item_details(inventory: dict, update_data: dict) -> dict:
    """
    Update an inventory item with new values from `update_data`.

    Only keys listed in ``PERMITTED_FIELDS`` are updated.  All other
    modifications are ignored.

    Parameters
    ----------
    inventory : dict
        The original product dictionary.  It is modified in place and also
        returned for convenience.
    update_data : dict
        A dictionary containing new field values.  Keys that are not in
        ``PERMITTED_FIELDS`` or have values of an incorrect type are ignored.

    Returns
    -------
    dict
        The updated inventory dictionary.

    Raises
    ------
    ValueError
        If ``inventory`` or ``update_data`` is not a dictionary.
    """
    if not isinstance(inventory, dict):
        raise ValueError("inventory must be a dictionary")
    if not isinstance(update_data, dict):
        raise ValueError("update_data must be a dictionary")

    for field, new_value in update_data.items():
        if field not in PERMITTED_FIELDS:
            # Skip any fields that are not allowed to be updated
            continue

        if not _validate_field(field, new_value):
            # Skip or optionally log a warning about type mismatch
            continue

        inventory[field] = new_value

    return inventory


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to run)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Sample inventory item
    product = {
        "price": 19.99,
        "description": "A nice gadget",
        "stock": 100,
        "category": "electronics"
    }

    # Attempt to update the product
    updates = {
        "price": 17.49,
        "stock": 120,
        "color": "red",          # not permitted
        "description": 12345     # wrong type, will be ignored
    }

    updated_product = update_item_details(product, updates)
    print(updated_product)