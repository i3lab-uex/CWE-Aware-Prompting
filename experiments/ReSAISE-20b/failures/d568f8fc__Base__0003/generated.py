#!/usr/bin/env python3
"""
Utility for safely updating product dictionaries.

This module defines a single function `adjust_product_data` that updates
only whitelisted fields of a product dictionary.  The list of permitted
fields is provided by the global `PERMITTED_FIELDS` constant.

The function guards against CWE‑915 (Improperly Controlled Modification of
Dynamically-Determined Object Attributes) by ensuring that only keys in
`PERMITTED_FIELDS` are applied to the product dictionary.
"""

from __future__ import annotations

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# List of fields that are allowed to be modified.  This list can be extended
# as new product attributes become safe for external updates.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def adjust_product_data(prod_info: Dict[str, Any], change_vals: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    prod_info : dict
        The original product dictionary.  This dictionary will be modified in
        place and also returned for convenience.
    change_vals : dict
        Dictionary of field names to new values that should be applied to
        ``prod_info``.

    Returns
    -------
    dict
        The updated product dictionary.

    Raises
    ------
    ValueError
        If ``change_vals`` contains a key that is not in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    The function performs a shallow update.  If the values themselves are
    mutable objects, callers should ensure they are safely handled.
    """
    # Validate that all keys in change_vals are permitted
    for key in change_vals:
        if key not in PERMITTED_FIELDS:
            raise ValueError(
                f"Attempted to modify disallowed field '{key}'. "
                "Only the following fields are permitted: "
                f"{PERMITTED_FIELDS}"
            )

    # Apply the changes
    prod_info.update(change_vals)

    return prod_info

# --------------------------------------------------------------------------- #
# Example usage (uncomment to run)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    product = {
        "id": 123,
        "price": 19.99,
        "description": "A great widget",
        "stock": 50,
        "category": "gadgets",
    }

    updates = {
        "price": 17.99,
        "stock": 45,
    }

    try:
        updated_product = adjust_product_data(product, updates)
        print("Updated product:", updated_product)
    except ValueError as e:
        print("Error:", e)