# -*- coding: utf-8 -*-
"""
Utility module for safely updating product data.
"""

from __future__ import annotations

# Global list of fields that are allowed to be modified
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def modify_product_data(product_details: dict, update_info: dict) -> dict:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    product_details : dict
        The original product data. Keys represent attribute names.
    update_info : dict
        A dictionary containing field-value pairs to be applied.

    Returns
    -------
    dict
        A new dictionary that contains the updated product data.
        Only keys present in ``PERMITTED_FIELDS`` are modified; all other
        keys remain unchanged.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If ``update_info`` contains keys that are not permitted.
    """
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a dictionary")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a dictionary")

    # Create a shallow copy to avoid mutating the original
    updated_product = product_details.copy()

    for field, new_value in update_info.items():
        if field not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{field}' is not permitted for modification")
        # Assign the new value; this does not execute any code
        updated_product[field] = new_value

    return updated_product