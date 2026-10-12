#!/usr/bin/env python3
"""
Safe product detail updater.

The module defines a global list of permitted fields that may be updated on
product dictionaries.  The `modify_product_details` function applies only
those updates that are explicitly allowed, preventing unintended or malicious
changes to the product object.

The implementation follows CWE‑915 guidelines by tightly controlling which
attributes may be modified and avoiding dynamic attribute assignment that
could otherwise expose the system to injection or accidental corruption.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, List

# --------------------------------------------------------------------------- #
#  Configuration
# --------------------------------------------------------------------------- #

# List of fields that are allowed to be updated.
PERMITTED_FIELDS: List[str] = [
    "price",
    "description",
    "stock",
    "category",
    # Add more fields as needed
]

# --------------------------------------------------------------------------- #
#  Core functionality
# --------------------------------------------------------------------------- #

def modify_product_details(product: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with permitted fields updated.

    Parameters
    ----------
    product : dict
        Original product data.  Keys are expected to be strings.
    data : dict
        Dictionary containing proposed updates.  Only keys that are present in
        :data:`PERMITTED_FIELDS` will be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.  The original
        `product` argument is left untouched.

    Raises
    ------
    TypeError
        If either `product` or `data` is not a dictionary.
    ValueError
        If any key in `product` or `data` is not a string.  This protects
        against accidental injection of non-string keys that could be used to
        manipulate internal state.
    """
    # Basic type validation
    if not isinstance(product, dict):
        raise TypeError(f"Expected product to be a dict, got {type(product).__name__}")
    if not isinstance(data, dict):
        raise TypeError(f"Expected data to be a dict, got {type(data).__name__}")

    # Ensure all keys are strings
    for key in product:
        if not isinstance(key, str):
            raise ValueError(f"Product contains non-string key: {key!r}")
    for key in data:
        if not isinstance(key, str):
            raise ValueError(f"Data contains non-string key: {key!r}")

    # Create a shallow copy to avoid mutating the original product
    updated_product = copy.deepcopy(product)

    # Apply only permitted updates
    for key, value in data.items():
        if key in PERMITTED_FIELDS:
            updated_product[key] = value

    return updated_product

# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    sample_product = {
        "id": 123,
        "price": 19.99,
        "description": "A nice gadget",
        "stock": 50,
        "category": "electronics",
    }

    updates = {
        "price": 17.99,
        "description": "A discounted gadget",
        "stock": 45,
        "id": 999,          # Should be ignored
        "__class__": str,   # Also ignored
    }

    new_product = modify_product_details(sample_product, updates)
    print("Original:", sample_product)
    print("Updated :", new_product)