# -*- coding: utf-8 -*-

"""
Utility to safely modify product details.

The module defines a global list of fields that are allowed to be
modified. The `modify_product_details` function will update only those
fields that are present in both the product and the incoming data.
Any other keys in `data` will be ignored.  The function returns a
new dictionary instance, leaving the original product untouched.

Example:
    >>> product = {"price": 10.0, "description": "Old", "stock": 5}
    >>> update = {"price": 12.0, "description": "New", "color": "red"}
    >>> modify_product_details(product, update)
    {'price': 12.0, 'description': 'New', 'stock': 5}
"""

from __future__ import annotations

from typing import Dict, Any, List


# Global list of fields that can be updated
PERMITTED_FIELDS: List[str] = [
    "price",
    "description",
    "stock",
    "category",
    # Add more permitted fields here as needed
]


def modify_product_details(product: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values from `data`, but only for
    fields listed in :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    product :
        Dictionary representing the original product. It must be a mapping.
    data :
        Dictionary containing potential updates. Only keys that are
        present in :data:`PERMITTED_FIELDS` will be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated product data. The input
        dictionaries are not modified.

    Raises
    ------
    TypeError
        If either `product` or `data` is not a dictionary.
    """
    if not isinstance(product, dict):
        raise TypeError(f"Expected product to be a dict, got {type(product).__name__}")
    if not isinstance(data, dict):
        raise TypeError(f"Expected data to be a dict, got {type(data).__name__}")

    # Create a shallow copy so we don't mutate the original product
    updated_product: Dict[str, Any] = product.copy()

    for key in PERMITTED_FIELDS:
        if key in data:
            updated_product[key] = data[key]

    return updated_product