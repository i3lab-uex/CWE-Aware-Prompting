#!/usr/bin/env python3
"""
A small utility that safely updates a product dictionary with new values.
Only fields listed in the global PERMITTED_FIELDS are allowed to be modified.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, List

# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS: List[str] = [
    "price",
    "description",
    "stock",
    "category",
]


def update_item_information(
    product_info: Dict[str, Any], new_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update product information with new data.

    Parameters
    ----------
    product_info : dict
        The original product dictionary.
    new_data : dict
        A dictionary of fields to update.

    Returns
    -------
    dict
        A new dictionary containing the updated product information.

    Raises
    ------
    ValueError
        If `new_data` contains keys that are not in PERMITTED_FIELDS.
    TypeError
        If either argument is not a dictionary.
    """
    if not isinstance(product_info, dict):
        raise TypeError("product_info must be a dictionary")
    if not isinstance(new_data, dict):
        raise TypeError("new_data must be a dictionary")

    # Create a shallow copy to avoid mutating the original
    updated_product = copy.deepcopy(product_info)

    # Validate and apply updates
    for key, value in new_data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update")
        updated_product[key] = value

    return updated_product