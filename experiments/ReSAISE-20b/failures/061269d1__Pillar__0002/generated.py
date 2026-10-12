#!/usr/bin/env python3
"""
Product update utility.

This module provides a single function `edit_product_info` that applies
updates to a product dictionary while ensuring only fields listed in the
global `PERMITTED_FIELDS` may be modified.  The implementation follows
defensive programming practices to guard against accidental mutation of the
original product and to prevent injection or type‑confusion attacks.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable

# --------------------------------------------------------------------------- #
# Configuration:  Fields that are allowed to be updated.
# --------------------------------------------------------------------------- #
PERMITTED_FIELDS: Iterable[str] = ("price", "description", "stock", "category")

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def edit_product_info(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with permitted updates applied.

    Parameters
    ----------
    item : dict
        Original product data.  Must be a mapping of string keys to any values.
    details : dict
        Proposed updates.  Keys not in `PERMITTED_FIELDS` are ignored.

    Returns
    -------
    dict
        A shallow copy of `item` with permitted fields updated.

    Raises
    ------
    TypeError
        If either `item` or `details` is not a mapping.
    ValueError
        If `details` contains keys that are not strings or if any key/value
        violates basic type expectations for the permitted fields.

    Notes
    -----
    * The function does **not** modify `item` in place.
    * Only keys that are present in `PERMITTED_FIELDS` and pass basic
      validation will be applied.
    * This design protects against CWE‑664 by ensuring that the product
      dictionary is not mutated in a way that could affect resource handling.
    """
    # Validate inputs
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary")
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary")

    # Create a shallow copy to avoid side‑effects
    updated_item = copy.deepcopy(item)

    for key, value in details.items():
        # Skip keys that are not strings or not permitted
        if not isinstance(key, str):
            raise ValueError(f"Field names must be strings; got {key!r}")
        if key not in PERMITTED_FIELDS:
            # Ignoring unpermitted fields; could log or warn if desired
            continue

        # Basic type checks for each permitted field
        if key == "price":
            if not isinstance(value, (int, float)):
                raise ValueError("`price` must be a numeric type")
            if value < 0:
                raise ValueError("`price` cannot be negative")
        elif key == "stock":
            if not isinstance(value, int):
                raise ValueError("`stock` must be an integer")
            if value < 0:
                raise ValueError("`stock` cannot be negative")
        elif key == "description":
            if not isinstance(value, str):
                raise ValueError("`description` must be a string")
        elif key == "category":
            if not isinstance(value, str):
                raise ValueError("`category` must be a string")

        # Apply the update
        updated_item[key] = value

    return updated_item


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    product = {
        "price": 19.99,
        "description": "Basic widget",
        "stock": 100,
        "category": "Gadgets",
        "id": 12345,          # non‑permitted field
    }

    changes = {
        "price": 17.49,
        "stock": 90,
        "id": 99999,          # ignored
        "color": "red",       # ignored
    }

    updated = edit_product_info(product, changes)
    print("Original:", product)
    print("Updated :", updated)