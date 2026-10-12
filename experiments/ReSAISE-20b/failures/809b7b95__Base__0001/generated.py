# -*- coding: utf-8 -*-

"""
Utility module for safely updating product dictionaries.

The module exposes a single public function, `modify_item_details`, which updates
a product dictionary only for attributes that are explicitly permitted.
"""

from __future__ import annotations

from typing import Dict, Any, Iterable


# Global list of attributes that are allowed to be modified.
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)

def _validate_input(item: Dict[str, Any], details: Dict[str, Any]) -> None:
    """
    Internal helper that validates the types of `item` and `details`.

    Raises:
        TypeError: If either argument is not a dictionary.
    """
    if not isinstance(item, dict):
        raise TypeError(f"Expected 'item' to be a dict, got {type(item).__name__}")
    if not isinstance(details, dict):
        raise TypeError(f"Expected 'details' to be a dict, got {type(details).__name__}")


def modify_item_details(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Safely modify product attributes.

    Only keys present in the global `PERMITTED_FIELDS` list are updated.
    Other keys are ignored to prevent unintended modifications.

    Args:
        item: A dictionary representing the product.
        details: A dictionary containing desired updates.

    Returns:
        A new dictionary with the updated product state.
        The original `item` is not modified.

    Raises:
        TypeError: If `item` or `details` are not dictionaries.
    """
    _validate_input(item, details)

    # Create a shallow copy to avoid mutating the original product.
    updated_item: Dict[str, Any] = dict(item)

    for key, value in details.items():
        if key in PERMITTED_FIELDS:
            updated_item[key] = value
        else:
            # Optionally, log a warning or silently ignore.
            pass

    return updated_item