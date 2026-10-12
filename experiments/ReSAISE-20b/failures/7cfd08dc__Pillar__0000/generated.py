#!/usr/bin/env python3
"""
Utility module for updating product attributes.

The function `update_product_attributes` takes a product dictionary and an
updates dictionary, applies only the permitted fields to a copy of the product,
and returns the updated product.  The original dictionary is left untouched
to avoid accidental mutation of shared state (CWE‑664 mitigation).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

from typing import Dict, Any, Iterable, List

# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS: List[str] = [
    "price",
    "description",
    "stock",
    "category",
]

def update_product_attributes(item: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with permitted attributes updated.

    Parameters
    ----------
    item : dict
        Original product data.  Must be a mapping from string keys to any values.
    updates : dict
        Desired attribute changes.  Only keys present in `PERMITTED_FIELDS`
        will be applied.

    Returns
    -------
    dict
        A new dictionary containing the original product data with any
        permitted updates applied.

    Raises
    ------
    TypeError
        If either `item` or `updates` is not a mapping.
    """
    if not isinstance(item, dict):
        raise TypeError(f"Expected 'item' to be a dict, got {type(item).__name__}")
    if not isinstance(updates, dict):
        raise TypeError(f"Expected 'updates' to be a dict, got {type(updates).__name__}")

    # Create a shallow copy so that the original item is not mutated.
    updated_item: Dict[str, Any] = dict(item)

    # Apply only permitted fields.
    for key in updates:
        if key in PERMITTED_FIELDS:
            updated_item[key] = updates[key]
    return updated_item

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     product = {"price": 10.99, "description": "Widget", "stock": 100, "category": "Tools"}
#     changes = {"price": 9.99, "stock": 120, "color": "red"}  # 'color' is not permitted
#     print(update_product_attributes(product, changes))