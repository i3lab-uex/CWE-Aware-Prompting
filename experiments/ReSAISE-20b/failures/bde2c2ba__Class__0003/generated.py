# -*- coding: utf-8 -*-

"""
Utility for updating product information while enforcing a whitelist of allowed fields.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Global whitelist of fields that can be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def update_item_information(product_info: Dict[str, Any],
                            new_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product's attributes with values from *new_data* only for keys that are
    explicitly allowed in :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    product_info:
        The original product dictionary. It will **not** be modified in place.
    new_data:
        A mapping containing proposed updates.

    Returns
    -------
    dict
        A new dictionary representing the updated product state.

    Raises
    ------
    ValueError
        If *product_info* or *new_data* is not a dictionary.
    """
    if not isinstance(product_info, dict):
        raise ValueError("product_info must be a dictionary")
    if not isinstance(new_data, dict):
        raise ValueError("new_data must be a dictionary")

    # Work on a shallow copy to avoid mutating the caller's data.
    updated_product = copy.deepcopy(product_info)

    for key, value in new_data.items():
        if key in PERMITTED_FIELDS:
            updated_product[key] = value

    return updated_product