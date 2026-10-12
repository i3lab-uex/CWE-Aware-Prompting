# -*- coding: utf-8 -*-
"""
Product data modification module.

This module provides a single function `modify_product_data` that updates
selected fields of a product dictionary. Only the keys listed in
`PERMITTED_FIELDS` are allowed to be modified.

The function performs basic type checks and silently ignores any keys that
are not in the permitted list.
"""

from typing import Dict, Any

# List of fields that are allowed to be modified
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def modify_product_data(product_details: Dict[str, Any],
                        update_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    product_details : dict
        The original product information.
    update_info : dict
        A dictionary containing fields to be updated.

    Returns
    -------
    dict
        The product dictionary after applying the permitted updates.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    """
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a dictionary")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a dictionary")

    # Create a copy to avoid mutating the original
    updated_product = product_details.copy()

    for key, value in update_info.items():
        if key in PERMITTED_FIELDS:
            updated_product[key] = value
    return updated_product