# -*- coding: utf-8 -*-
"""
Utility module for updating product details safely.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, Any

# Global list of fields that are allowed to be modified.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
    "name",
    # Add more fields here as needed.
]


def modify_product_details(product: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with values from ``data`` only for fields
    that are present in :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    product:
        The original product dictionary. It may contain arbitrary keys.
    data:
        Dictionary of updates where the key is the field name and the value
        is the new content.

    Returns
    -------
    dict:
        A new dictionary containing the updated product. The original
        ``product`` object is not modified.

    Raises
    ------
    TypeError:
        If either ``product`` or ``data`` is not a mapping.
    """
    if not isinstance(product, dict):
        raise TypeError("product must be a dictionary")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    # Work on a shallow copy to avoid mutating the input product
    updated_product = deepcopy(product)

    for key, value in data.items():
        if key in PERMITTED_FIELDS:
            updated_product[key] = value
        else:
            # For security we ignore disallowed keys.  Logging could be added
            # here if desired.
            continue

    return updated_product


# Example usage (for demonstration purposes only)
if __name__ == "__main__":
    original = {
        "id": 123,
        "name": "Widget",
        "price": 19.99,
        "description": "A useful widget.",
        "stock": 50,
        "category": "Tools",
        "created_at": "2023-01-01T12:00:00Z",
    }

    updates = {
        "price": 17.99,
        "stock": 45,
        "description": "An updated description.",
        "created_at": "2024-01-01T12:00:00Z",  # should be ignored
    }

    new_product = modify_product_details(original, updates)
    print("Updated product:", new_product)