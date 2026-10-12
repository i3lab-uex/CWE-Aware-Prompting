# -*- coding: utf-8 -*-
"""
Utility module for updating product information with controlled field modification.
"""

from copy import deepcopy
from typing import Dict, Any

# List of fields that are allowed to be updated.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def update_item_information(product_info: Dict[str, Any], new_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with values from ``new_data`` only for
    fields listed in :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    product_info:
        The original product dictionary.  This dict is not modified in place.
    new_data:
        A mapping containing the desired updates.

    Returns
    -------
    dict
        A new dictionary with the permitted updates applied.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If ``new_data`` contains keys that are not in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    - The function performs a shallow copy of ``product_info`` before applying updates.
      Nested mutable objects are not deep‑cloned; callers should be aware of this.
    - This function protects against CWE-915 by restricting updates to a
      predefined whitelist of field names.
    """
    if not isinstance(product_info, dict):
        raise TypeError("product_info must be a dictionary")
    if not isinstance(new_data, dict):
        raise TypeError("new_data must be a dictionary")

    # Create a shallow copy to avoid mutating the original
    updated_product = deepcopy(product_info)

    for key, value in new_data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Attempted to update disallowed field: {key!r}")
        updated_product[key] = value

    return updated_product