# -*- coding: utf-8 -*-

"""
Utility module for updating product data with a strict whitelist of
permitted fields.

Author: Your Name
"""

from __future__ import annotations

# Only these keys are allowed to be modified.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def modify_product_data(product_details: dict, update_info: dict) -> dict:
    """
    Update a product dictionary with new values while enforcing a whitelist
    of permitted fields.

    Parameters
    ----------
    product_details : dict
        The original product data.
    update_info : dict
        Dictionary containing fields to be updated.

    Returns
    -------
    dict
        A new dictionary with the updates applied.

    Raises
    ------
    ValueError
        If `update_info` contains a key that is not in :data:`PERMITTED_FIELDS`.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    * The function does **not** modify the original `product_details`
      dictionary; it returns a new updated copy.
    * Keys not present in the original product are ignored unless they
      belong to the permitted set. This allows adding new fields if needed.
    """
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a dictionary")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a dictionary")

    # Create a shallow copy to avoid mutating the original
    updated = product_details.copy()

    for key, value in update_info.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update")
        updated[key] = value

    return updated