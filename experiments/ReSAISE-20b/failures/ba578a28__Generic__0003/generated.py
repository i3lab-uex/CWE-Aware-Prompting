# -*- coding: utf-8 -*-
"""
Utility module for updating product data with strict field validation.
"""

from typing import Dict, Any

# Fields that are allowed to be modified.  Add or remove fields here as needed.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def modify_product_data(
    product_details: Dict[str, Any], update_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update `product_details` with values from `update_info`, but only for keys listed
    in :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    product_details : dict
        Dictionary containing the current product attributes.
    update_info : dict
        Dictionary with keys and values intended for update.

    Returns
    -------
    dict
        The updated product dictionary (the same object as `product_details`).

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If `update_info` contains keys that are not in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    The function modifies the original `product_details` dictionary in place.
    """
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a dictionary")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a dictionary")

    # Identify any disallowed keys
    invalid_keys = [k for k in update_info if k not in PERMITTED_FIELDS]
    if invalid_keys:
        raise ValueError(
            f"The following fields are not permitted for update: {', '.join(invalid_keys)}"
        )

    # Apply allowed updates
    for key, value in update_info.items():
        product_details[key] = value

    return product_details