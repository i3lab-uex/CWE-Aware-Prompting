#!/usr/bin/env python3
"""
Utility to update product details while respecting a whitelist of fields.

The module defines a global list `PERMITTED_FIELDS` that enumerates the
product attributes which are allowed to be modified.  The main function,
`modify_product_details`, accepts a product dictionary and a data
dictionary containing updates.  Only keys that are present in the whitelist
are applied; all other keys are silently ignored.

The function returns a new dictionary representing the updated product,
leaving the original `product` unchanged to avoid accidental side‑effects.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, List

# --------------------------------------------------------------------------- #
# Public constants
# --------------------------------------------------------------------------- #

# Whitelist of fields that can be updated.  Extend this list as the
# product schema evolves.
PERMITTED_FIELDS: List[str] = [
    "price",
    "description",
    "stock",
    "category",
    # Add other mutable fields here
]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_update_key(key: str) -> None:
    """
    Validate that a key is in the PERMITTED_FIELDS list.

    Raises:
        ValueError: If the key is not permitted.
    """
    if key not in PERMITTED_FIELDS:
        raise ValueError(f"Attempted to update forbidden field '{key}'")

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def modify_product_details(product: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with permitted fields updated.

    Parameters
    ----------
    product :
        Original product data.  Must be a mapping of field names to values.
    data :
        Proposed updates.  Only keys present in ``PERMITTED_FIELDS`` will be
        applied; others are ignored.

    Returns
    -------
    Dict[str, Any]
        A new dictionary containing the merged data.  The original ``product``
        is left untouched.

    Raises
    ------
    ValueError
        If ``data`` contains a key that is not in the whitelist.
    """
    # Work on a shallow copy to preserve immutability of input
    updated_product = copy.deepcopy(product)

    for key, value in data.items():
        _validate_update_key(key)
        updated_product[key] = value

    return updated_product

# --------------------------------------------------------------------------- #
# Example usage (uncomment for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    original = {
        "id": 101,
        "price": 19.99,
        "description": "A useful widget",
        "stock": 150,
        "category": "Gadgets",
    }

    updates = {
        "price": 17.99,
        "stock": 140,
        "category": "Tools",
        # "id": 999,          # Uncommenting this line would raise ValueError
    }

    try:
        new_product = modify_product_details(original, updates)
        print("Original:", original)
        print("Updated :", new_product)
    except ValueError as exc:
        print(f"Update failed: {exc}")