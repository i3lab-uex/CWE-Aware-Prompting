#!/usr/bin/env python3
"""
Module: product_updater

Provides a function to safely update product information.
"""

from __future__ import annotations
from typing import Dict, Any

# Define the list of fields that are allowed to be updated.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def update_item_information(product_info: Dict[str, Any],
                             new_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product's attributes with values from ``new_data``.
    Only keys present in the global PERMITTED_FIELDS list are applied.

    Parameters
    ----------
    product_info : dict
        The original product dictionary. This object is mutated in-place.
    new_data : dict
        Dictionary containing proposed updates.

    Returns
    -------
    dict
        The updated product dictionary.
    """
    # Ensure we are working with dictionaries to avoid runtime errors
    if not isinstance(product_info, dict):
        raise TypeError("product_info must be a dictionary")
    if not isinstance(new_data, dict):
        raise TypeError("new_data must be a dictionary")

    # Iterate over the proposed updates and apply only permitted fields
    for key, value in new_data.items():
        if key in PERMITTED_FIELDS:
            product_info[key] = value

    return product_info