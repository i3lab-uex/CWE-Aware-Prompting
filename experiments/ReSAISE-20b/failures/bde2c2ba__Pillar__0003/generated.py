#!/usr/bin/env python3
"""
Utility module for updating product information while respecting a whitelist of
permitted fields.  The function ensures that only the allowed keys are modified,
prevents accidental mutation of the original product dictionary, and protects
against common security pitfalls such as arbitrary code execution or resource
leakage.

Author: ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable

# --------------------------------------------------------------------------- #
# Configuration: list of fields that may be updated
# --------------------------------------------------------------------------- #
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _is_permitted(field: str) -> bool:
    """
    Check if a field is allowed to be updated.

    Args:
        field: The key name to check.

    Returns:
        True if the field is in PERMITTED_FIELDS, False otherwise.
    """
    return field in PERMITTED_FIELDS


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #
def update_item_information(product_info: Dict[str, Any], new_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with updates applied only to fields
    specified in the global PERMITTED_FIELDS list.

    The function performs a shallow copy of the original product_info to
    avoid mutating input data.  It also validates that new_data contains only
    permitted keys and raises a ValueError if any disallowed key is present.

    Args:
        product_info: Original product dictionary.  Must be a mapping of
            string keys to any JSON-serializable values.
        new_data: Dictionary containing updates.  Keys must be strings.

    Returns:
        A new dictionary representing the updated product state.

    Raises:
        TypeError: If either argument is not a dict.
        ValueError: If new_data contains keys that are not permitted.
    """
    # Validate input types
    if not isinstance(product_info, dict):
        raise TypeError(f"product_info must be a dict; got {type(product_info).__name__}")
    if not isinstance(new_data, dict):
        raise TypeError(f"new_data must be a dict; got {type(new_data).__name__}")

    # Ensure new_data keys are strings
    for key in new_data:
        if not isinstance(key, str):
            raise TypeError(f"All keys in new_data must be strings; got key of type {type(key).__name__}")

    # Check for disallowed keys
    disallowed = [k for k in new_data if not _is_permitted(k)]
    if disallowed:
        raise ValueError(f"Attempted to update disallowed fields: {disallowed}")

    # Perform a shallow copy of the original product
    updated_product = copy.deepcopy(product_info)

    # Apply updates
    for key, value in new_data.items():
        updated_product[key] = value

    return updated_product


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    original = {
        "price": 19.99,
        "description": "A nice gadget",
        "stock": 100,
        "category": "electronics",
        "supplier_id": 42,   # Not permitted
    }

    updates = {
        "price": 17.99,
        "stock": 120,
    }

    try:
        new_product = update_item_information(original, updates)
        print("Updated product:", new_product)
    except Exception as exc:
        print(f"Error: {exc}")