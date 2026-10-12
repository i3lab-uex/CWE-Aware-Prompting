#!/usr/bin/env python3
"""
Utility module for updating product details securely.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable

# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)

def _is_safe_key(key: str) -> bool:
    """
    Determine whether a key is safe to be used in updates.
    Avoid keys that could potentially manipulate the object's class or
    internal state (e.g., '__class__', '__dict__', etc.).
    """
    # Disallow any key that starts with double underscores.
    if key.startswith("__") and key.endswith("__"):
        return False
    # Disallow keys that could be used to access internal attributes.
    if key in {"__dict__", "__weakref__", "__module__", "__doc__"}:
        return False
    return True


def modify_product_details(product: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with values from *data* if the keys are
    present in :data:`PERMITTED_FIELDS` and considered safe.

    Parameters
    ----------
    product :
        The original product dictionary.  It will not be mutated; a new
        dictionary containing the updated values is returned.
    data :
        Dictionary of fields to update.  Only keys that are in
        :data:`PERMITTED_FIELDS` and pass the safety check will be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.

    Raises
    ------
    ValueError
        If any key in *data* is not permitted or considered unsafe.
    TypeError
        If either *product* or *data* is not a dictionary.
    """
    if not isinstance(product, dict):
        raise TypeError(f"Expected product to be a dict, got {type(product).__name__}")
    if not isinstance(data, dict):
        raise TypeError(f"Expected data to be a dict, got {type(data).__name__}")

    # Create a shallow copy so that the original product is not mutated.
    updated_product = copy.deepcopy(product)

    for key, value in data.items():
        # Validate that the key is permitted and safe.
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")
        if not _is_safe_key(key):
            raise ValueError(f"Field '{key}' is considered unsafe and cannot be updated.")

        # Apply the update.
        updated_product[key] = value

    return updated_product