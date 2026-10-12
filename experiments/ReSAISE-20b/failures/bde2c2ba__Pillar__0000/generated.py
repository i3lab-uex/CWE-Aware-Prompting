# -*- coding: utf-8 -*-

"""
Utility for safely updating product information.

The function `update_item_information` accepts a product dictionary and a
dictionary of new values. Only keys that are listed in the global
`PERMITTED_FIELDS` list will be updated, protecting the product from
unintended modifications. The original product dictionary is left
untouched; a new, updated dictionary is returned.

The implementation guards against type errors and preserves the
original data structure by creating a shallow copy before applying
updates.
"""

from __future__ import annotations

# List of fields that are allowed to be updated
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_item_information(
    product_info: dict,
    new_data: dict
) -> dict:
    """
    Update allowed fields of a product dictionary with values from new_data.

    Parameters
    ----------
    product_info : dict
        The original product data.
    new_data : dict
        Key-value pairs representing the intended updates.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    """
    if not isinstance(product_info, dict):
        raise TypeError("product_info must be a dictionary")
    if not isinstance(new_data, dict):
        raise TypeError("new_data must be a dictionary")

    # Work on a shallow copy to avoid side effects
    updated_product = product_info.copy()

    for key, value in new_data.items():
        if key in PERMITTED_FIELDS:
            updated_product[key] = value

    return updated_product