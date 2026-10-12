# -*- coding: utf-8 -*-

"""
Utility module for updating product information.

The `update_item_information` function accepts a product dictionary and a
dictionary of new data.  Only the keys listed in the global `PERMITTED_FIELDS`
are allowed to be updated.  The function returns a new dictionary containing
the updated product state.
"""

from typing import Dict, Any

# Global list of fields that may be modified
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_item_information(product_info: Dict[str, Any],
                            new_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product's attributes with values from `new_data` only if the
    attribute is listed in PERMITTED_FIELDS.

    Parameters
    ----------
    product_info : dict
        The original product dictionary.
    new_data : dict
        Dictionary containing potential updates.

    Returns
    -------
    dict
        A new dictionary with the updated product state.
    """
    # Create a shallow copy to avoid mutating the original dictionary
    updated_product = product_info.copy()

    for key, value in new_data.items():
        if key in PERMITTED_FIELDS:
            updated_product[key] = value

    return updated_product