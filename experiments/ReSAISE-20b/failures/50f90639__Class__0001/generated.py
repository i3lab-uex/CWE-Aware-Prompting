#!/usr/bin/env python3
"""
Utility for safely updating product details.
"""

from copy import deepcopy
from typing import Dict, List

# Global list of fields that are allowed to be modified.
PERMITTED_FIELDS: List[str] = [
    "price",
    "description",
    "stock",
    "category",
    # Add more allowed fields here as needed.
]


def modify_product_details(product: Dict, data: Dict) -> Dict:
    """
    Update a product dictionary with new values from `data` while
    restricting updates to fields defined in PERMITTED_FIELDS.

    Parameters
    ----------
    product : dict
        The original product data.
    data : dict
        Dictionary containing fields to update and their new values.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.

    Raises
    ------
    TypeError
        If either `product` or `data` is not a dictionary.
    ValueError
        If any key in `data` is not present in PERMITTED_FIELDS.
    """
    if not isinstance(product, dict):
        raise TypeError("product must be a dictionary")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    # Work on a copy to avoid mutating the original product.
    updated_product = deepcopy(product)

    for key, value in data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update.")
        # Update the value in the copied product.
        updated_product[key] = value

    return updated_product