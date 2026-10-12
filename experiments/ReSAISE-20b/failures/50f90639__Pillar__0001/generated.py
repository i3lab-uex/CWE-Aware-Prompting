#!/usr/bin/env python3
"""
Product detail modification utility.

This module provides a single public function, `modify_product_details`, which
creates an updated copy of a product dictionary based on supplied data. Only
fields listed in the global `PERMITTED_FIELDS` list are allowed to be changed.
Any attempt to modify disallowed fields is silently ignored.

The function performs a shallow copy of the original product to avoid
side‑effects on caller references.  This approach mitigates CWE‑664 (Improper
Control of a Resource Through its Lifetime) by ensuring that the original
product dictionary is not mutated inadvertently.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# List of fields that are allowed to be updated.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
    # Add additional permitted fields here.
]


def modify_product_details(product: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with updated fields.

    Parameters
    ----------
    product : dict
        The original product representation. Must be a mapping of string keys to any values.
    data : dict
        Mapping containing fields to update and their new values.

    Returns
    -------
    dict
        A new dictionary containing the updated product data. The original `product`
        is left untouched.

    Notes
    -----
    - Only keys present in :data:`PERMITTED_FIELDS` are considered for update.
    - If a key is present in both `product` and `data`, the value from `data`
      overrides the one in `product`.
    - Keys not listed in :data:`PERMITTED_FIELDS` are ignored.
    """
    # Validate input types to guard against accidental misuse.
    if not isinstance(product, dict):
        raise TypeError("product must be a dictionary")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    # Create a shallow copy to avoid mutating the original product.
    updated_product = copy.copy(product)

    for key, value in data.items():
        if key in PERMITTED_FIELDS:
            updated_product[key] = value
    return updated_product