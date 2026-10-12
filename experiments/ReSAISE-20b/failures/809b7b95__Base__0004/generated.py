#!/usr/bin/env python3
"""
Utility module for safely updating product dictionaries.

The function `modify_item_details` updates only a predefined set of
fields that are allowed to be modified. This protects against
CWE-915 (Improperly Controlled Modification of Dynamically-Determined Object Attributes)
by ensuring that no unexpected or malicious keys can be added to the product
dictionary.
"""

from __future__ import annotations

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
# Helper functions
# --------------------------------------------------------------------------- #
def _validate_field_name(field: str) -> bool:
    """
    Check if a field name is in the whitelist of permitted fields.
    """
    return field in PERMITTED_FIELDS


def _validate_field_value(field: str, value: Any) -> bool:
    """
    Basic type validation for known fields. This can be extended as needed.
    Returns True if the value passes validation, False otherwise.
    """
    # Example type checks; modify or extend as per business rules
    if field == "price":
        return isinstance(value, (int, float)) and value >= 0
    if field == "stock":
        return isinstance(value, int) and value >= 0
    # For string fields we just check the type
    if field in ("description", "category"):
        return isinstance(value, str)
    # Default: allow any value
    return True


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #
def modify_item_details(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Safely modify product attributes based on the provided `details` dictionary.

    Parameters
    ----------
    item : dict
        The original product dictionary.
    details : dict
        Dictionary containing key-value pairs to update the product.

    Returns
    -------
    dict
        A new dictionary representing the updated product state. The original
        `item` is not mutated.

    Raises
    ------
    ValueError
        If a field in `details` is not permitted or if the value fails validation.
    """
    # Work on a shallow copy to avoid mutating the input
    updated_item = item.copy()

    for key, new_value in details.items():
        if not _validate_field_name(key):
            raise ValueError(f"Field '{key}' is not permitted for modification.")

        if not _validate_field_value(key, new_value):
            raise ValueError(f"Invalid value for field '{key}': {new_value!r}")

        # Apply the update
        updated_item[key] = new_value

    return updated_item


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    sample_item = {
        "price": 19.99,
        "description": "A great product",
        "stock": 100,
        "category": "gadgets",
    }

    updates = {
        "price": 17.49,
        "stock": 90,
    }

    try:
        new_item = modify_item_details(sample_item, updates)
        print("Updated product:", new_item)
    except ValueError as exc:
        print(f"Update failed: {exc}")