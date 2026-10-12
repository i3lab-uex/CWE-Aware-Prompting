# -*- coding: utf-8 -*-
"""
Product data modification utility.

The module defines a single public function `modify_product_data` that
updates a product dictionary only for fields explicitly allowed in the
global PERMITTED_FIELDS list.  This prevents unintended or malicious
attribute changes (CWE‑915).
"""

from typing import Dict, Any

# Define the list of fields that are allowed to be modified.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def modify_product_data(
    product_details: Dict[str, Any],
    update_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a product dictionary with values from `update_info` but only
    for keys that are present in the global PERMITTED_FIELDS list.

    Parameters
    ----------
    product_details : dict
        The original product data.  This dictionary is modified in place.
    update_info : dict
        A dictionary containing proposed updates.  Keys not in
        PERMITTED_FIELDS are ignored.

    Returns
    -------
    dict
        The updated product dictionary (the same object as `product_details`).

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    """
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a dictionary")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a dictionary")

    for key, value in update_info.items():
        if key in PERMITTED_FIELDS:
            product_details[key] = value

    return product_details