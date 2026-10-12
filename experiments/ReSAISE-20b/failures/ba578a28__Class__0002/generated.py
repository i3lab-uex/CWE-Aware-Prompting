# -*- coding: utf-8 -*-

"""
Product data modification utility.

This module defines a single function `modify_product_data` that safely updates
a product dictionary with values from an update dictionary. Only fields listed in
the global `PERMITTED_FIELDS` list are allowed to be changed, preventing
unintended or malicious modifications.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# List of fields that are allowed to be modified.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category"
]


def modify_product_data(
    product_details: Dict[str, Any],
    update_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update product details with permitted fields.

    Parameters
    ----------
    product_details : dict
        Original product data. The dictionary is not modified in-place.
    update_info : dict
        Fields and values intended for update. Only keys present in
        `PERMITTED_FIELDS` are applied.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.
    """
    # Work on a shallow copy to avoid side‑effects
    updated_product = copy.deepcopy(product_details)

    for field, value in update_info.items():
        if field not in PERMITTED_FIELDS:
            # Skip any non‑permitted fields silently
            continue

        # Optional: basic type validation can be added here if needed.
        updated_product[field] = value

    return updated_product