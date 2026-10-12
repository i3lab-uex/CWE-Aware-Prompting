#!/usr/bin/env python3
"""
Secure product data updater.

The function `modify_product_data` updates only the fields listed in
the global `PERMITTED_FIELDS`. Any attempt to modify a non‑permitted
field will raise a ValueError, protecting against CWE‑915.

Author: OpenAI ChatGPT
"""

from typing import Dict, Any

# List of fields that are allowed to be modified.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def modify_product_data(
    product_details: Dict[str, Any], update_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a product dictionary with allowed fields.

    Parameters
    ----------
    product_details : dict
        The original product data.
    update_info : dict
        Dictionary containing fields to be updated.

    Returns
    -------
    dict
        The product dictionary after applying permitted updates.

    Raises
    ------
    ValueError
        If `update_info` contains a field not in PERMITTED_FIELDS.
    """
    # Validate update keys
    for key in update_info:
        if key not in PERMITTED_FIELDS:
            raise ValueError(
                f"Field '{key}' is not permitted for update. "
                f"Allowed fields: {sorted(PERMITTED_FIELDS)}"
            )

    # Apply permitted updates
    for key, value in update_info.items():
        product_details[key] = value

    return product_details