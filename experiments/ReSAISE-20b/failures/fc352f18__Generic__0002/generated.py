#!/usr/bin/env python3
"""
Utility to safely amend product features.

Only keys listed in `PERMITTED_FIELDS` are allowed to be updated.
Any other keys in the payload are ignored.

Author: ChatGPT
"""

from typing import Dict, Any

# Define which product fields are allowed to be modified.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def amend_product_features(item: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the given product dictionary with values from `payload` only for
    permitted fields.

    Parameters
    ----------
    item : dict
        The original product dictionary. It will be modified in place.
    payload : dict
        Dictionary containing new values for the product fields.

    Returns
    -------
    dict
        The updated product dictionary (the same object as `item`).

    Raises
    ------
    TypeError
        If either `item` or `payload` is not a dictionary.
    """
    if not isinstance(item, dict):
        raise TypeError(f"'item' must be a dict, got {type(item).__name__}")
    if not isinstance(payload, dict):
        raise TypeError(f"'payload' must be a dict, got {type(payload).__name__}")

    for key, value in payload.items():
        if key in PERMITTED_FIELDS:
            item[key] = value
    return item


# Example usage (uncomment to test)
if __name__ == "__main__":
    product = {
        "price": 19.99,
        "description": "A great widget",
        "stock": 42,
        "category": "gadgets",
        "supplier_id": 7,          # not permitted
    }

    updates = {
        "price": 17.99,
        "stock": 50,
        "supplier_id": 8,          # ignored
    }

    amended = amend_product_features(product, updates)
    print(amended)