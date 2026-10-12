#!/usr/bin/env python3
"""
Utility for updating product details safely.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# List of fields that are allowed to be modified.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def modify_product_details(product: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values from `data`, but only for fields
    that are present in PERMITTED_FIELDS.

    Parameters
    ----------
    product : dict
        The original product dictionary.
    data : dict
        Dictionary containing fields to update and their new values.

    Returns
    -------
    dict
        A new dictionary with the updates applied. The original `product`
        dictionary is left untouched.

    Raises
    ------
    TypeError
        If either `product` or `data` is not a dictionary.
    """
    if not isinstance(product, dict):
        raise TypeError("product must be a dictionary")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    # Create a shallow copy to avoid mutating the original product.
    updated_product = copy.deepcopy(product)

    for key, value in data.items():
        if key in PERMITTED_FIELDS:
            updated_product[key] = value
        else:
            # Disallow updating unpermitted fields.
            # We silently ignore them to avoid leaking internal structure.
            continue

    return updated_product