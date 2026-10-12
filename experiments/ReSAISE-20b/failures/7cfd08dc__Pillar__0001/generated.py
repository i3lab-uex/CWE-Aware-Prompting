#!/usr/bin/env python3
"""
Product attribute updater

This module provides a single public function `update_product_attributes` that updates
a product dictionary only for fields listed in the global `PERMITTED_FIELDS`
constant. The original product dictionary is left untouched; a new dictionary
containing the updated values is returned.

The implementation guards against accidental modification of the input data,
enforces field‑level permission, and performs basic type validation to
prevent malformed updates.

Author: ChatGPT
"""

from __future__ import annotations

import copy
from typing import Any, Dict, Mapping

# --------------------------------------------------------------------------- #
# Global constants
# --------------------------------------------------------------------------- #

# Fields that are allowed to be updated. Add or remove fields as needed.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_update_field(field: str, value: Any) -> None:
    """
    Perform basic validation for an update. This function can be extended to
    include more sophisticated checks (e.g., type, range) as the application
    grows.

    Parameters:
        field: The product attribute being updated.
        value: The new value for the attribute.

    Raises:
        ValueError: If the value does not meet expected criteria.
    """
    if field == "price":
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a numeric value.")
        if value < 0:
            raise ValueError("Price cannot be negative.")
    elif field == "stock":
        if not isinstance(value, int):
            raise ValueError("Stock must be an integer.")
        if value < 0:
            raise ValueError("Stock cannot be negative.")
    elif field == "description":
        if not isinstance(value, str):
            raise ValueError("Description must be a string.")
    elif field == "category":
        if not isinstance(value, str):
            raise ValueError("Category must be a string.")


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def update_product_attributes(
    item: Mapping[str, Any], updates: Mapping[str, Any]
) -> Dict[str, Any]:
    """
    Return a new product dictionary with updates applied to permitted fields.

    Parameters:
        item: A mapping representing the current state of a product.
        updates: A mapping containing key-value pairs to update in the product.

    Returns:
        A new dictionary reflecting the updated product state. The original
        `item` remains unchanged.

    Raises:
        KeyError: If an update attempts to modify a field not in
                  `PERMITTED_FIELDS`.
        ValueError: If an update value fails basic validation.
    """
    # Create a shallow copy to avoid mutating the original dictionary
    updated_product = dict(item)

    for field, new_value in updates.items():
        if field not in PERMITTED_FIELDS:
            raise KeyError(
                f"Field '{field}' is not permitted for update. "
                f"Allowed fields: {sorted(PERMITTED_FIELDS)}"
            )

        _validate_update_field(field, new_value)

        # Apply the update
        updated_product[field] = copy.deepcopy(new_value)

    return updated_product


# --------------------------------------------------------------------------- #
# Example usage (for testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample product
    product = {
        "id": 101,
        "price": 19.99,
        "description": "A useful gadget",
        "stock": 42,
        "category": "Electronics",
    }

    # Desired updates
    changes = {"price": 17.49, "stock": 38}

    # Apply updates
    try:
        new_product = update_product_attributes(product, changes)
        print("Original:", product)
        print("Updated :", new_product)
    except Exception as exc:
        print(f"Update failed: {exc}")