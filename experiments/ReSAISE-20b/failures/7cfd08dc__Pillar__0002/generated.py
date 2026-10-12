#!/usr/bin/env python3
"""
update_product_attributes module

This module provides a single function `update_product_attributes` that safely updates
product dictionaries based on an allowed set of fields.  The function performs a deep copy
to avoid mutating the caller's data, validates input types and values, and ensures that
only fields listed in `PERMITTED_FIELDS` are modified.

The implementation is mindful of CWE‑664 (Improper Control of a Resource Through its
Lifetime) by not creating or leaking resources, and by using immutable structures where
possible.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# Fields that are allowed to be updated.  This list can be extended as needed.
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_item(item: Dict[str, Any]) -> None:
    """
    Ensure that the item is a dictionary with string keys.

    Raises:
        TypeError: If `item` is not a dict or contains non-string keys.
    """
    if not isinstance(item, dict):
        raise TypeError("item must be a dictionary")
    for key in item:
        if not isinstance(key, str):
            raise TypeError(f"item contains non-string key: {key!r}")


def _validate_updates(updates: Dict[str, Any]) -> None:
    """
    Ensure that updates is a dictionary with string keys.

    Raises:
        TypeError: If `updates` is not a dict or contains non-string keys.
    """
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")
    for key in updates:
        if not isinstance(key, str):
            raise TypeError(f"updates contains non-string key: {key!r}")


def _is_valid_price(value: Any) -> bool:
    """
    Basic validation for a price field. Accepts int or float > 0.
    """
    return isinstance(value, (int, float)) and value >= 0


def _is_valid_stock(value: Any) -> bool:
    """
    Basic validation for stock. Accepts int >= 0.
    """
    return isinstance(value, int) and value >= 0


def _is_valid_category(value: Any) -> bool:
    """
    Basic validation for category. Accepts non-empty string.
    """
    return isinstance(value, str) and bool(value.strip())


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def update_product_attributes(item: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values from `updates`, but only for
    fields that are in the global PERMITTED_FIELDS list.

    Args:
        item: A dictionary representing a product.  Keys must be strings.
        updates: A dictionary containing key-value pairs for intended updates.

    Returns:
        A new dictionary reflecting the updated product state.  The original `item`
        is not modified.

    Raises:
        TypeError: If either argument is not a dictionary or contains non-string keys.
        ValueError: If an update value fails basic validation for its field.
    """
    # Validate inputs
    _validate_item(item)
    _validate_updates(updates)

    # Create a deep copy to avoid side effects
    updated_item = copy.deepcopy(item)

    for field, new_value in updates.items():
        if field not in PERMITTED_FIELDS:
            # Skip disallowed fields silently; alternatively, raise an error.
            continue

        # Perform basic type/value checks per field
        if field == "price" and not _is_valid_price(new_value):
            raise ValueError(f"Invalid price value: {new_value!r}")
        if field == "stock" and not _is_valid_stock(new_value):
            raise ValueError(f"Invalid stock value: {new_value!r}")
        if field == "category" and not _is_valid_category(new_value):
            raise ValueError(f"Invalid category value: {new_value!r}")

        # Update the field
        updated_item[field] = new_value

    return updated_item


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    sample_item = {
        "id": 123,
        "price": 19.99,
        "description": "A useful gadget",
        "stock": 50,
        "category": "Tools",
    }

    sample_updates = {
        "price": 17.49,
        "stock": 45,
        "category": "Hardware",
        "nonexistent_field": "should be ignored",
    }

    try:
        result = update_product_attributes(sample_item, sample_updates)
        print("Updated product:", result)
    except Exception as e:
        print(f"Error: {e}")