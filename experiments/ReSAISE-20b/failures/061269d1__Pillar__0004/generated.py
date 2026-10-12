# -*- coding: utf-8 -*-
"""
Product update utility.

This module provides a single public function, `edit_product_info`, which
updates the attributes of a product dictionary based on supplied details.
Only keys listed in the global `PERMITTED_FIELDS` are allowed to be modified.

The implementation follows defensive programming practices:
* It validates input types.
* It rejects disallowed keys with a clear exception message.
* It updates the product in place and returns the updated dictionary.

The code is intentionally simple to avoid resource‑management pitfalls
(CWE-664). No external resources are allocated or held beyond the scope of
the function call.
"""

from __future__ import annotations

from typing import Dict, Any, Iterable


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Only these fields may be updated.
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def edit_product_info(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with permitted fields.

    Parameters
    ----------
    item : dict
        The original product information. It will be updated in place.
    details : dict
        A dictionary containing the fields and values intended for update.

    Returns
    -------
    dict
        The updated product dictionary (the same object as `item`).

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If `details` contains keys that are not in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    The function performs a shallow update; nested structures are not deeply
    merged.  It is the caller's responsibility to ensure that values are of
    appropriate type for each field.
    """
    if not isinstance(item, dict):
        raise TypeError(f"Expected 'item' to be a dict, got {type(item).__name__}")
    if not isinstance(details, dict):
        raise TypeError(f"Expected 'details' to be a dict, got {type(details).__name__}")

    # Validate keys
    invalid_keys = [k for k in details if k not in PERMITTED_FIELDS]
    if invalid_keys:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(invalid_keys)}"
        )

    # Apply updates
    for key, value in details.items():
        item[key] = value

    return item


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    product = {
        "price": 19.99,
        "description": "A useful gadget",
        "stock": 100,
        "category": "Tools",
    }

    updates = {"price": 17.99, "stock": 95}
    updated_product = edit_product_info(product, updates)
    print(updated_product)   # {'price': 17.99, 'description': 'A useful gadget', 'stock': 95, 'category': 'Tools'}