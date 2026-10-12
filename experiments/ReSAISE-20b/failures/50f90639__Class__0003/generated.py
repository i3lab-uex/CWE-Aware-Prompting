# -*- coding: utf-8 -*-
"""
Utility module for updating product details safely.
"""

from typing import Dict, Any

# Define the list of fields that are allowed to be updated.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
    "name",
    "sku",
]

def modify_product_details(product: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values from `data` only for fields
    that are explicitly permitted. This function ensures that no arbitrary
    code execution or malicious data can be injected.

    Parameters:
        product (dict): The original product dictionary.
        data (dict): Dictionary containing fields to update and their new values.

    Returns:
        dict: The updated product dictionary.

    Raises:
        TypeError: If `product` or `data` is not a dict.
        ValueError: If any key in `data` is not in PERMITTED_FIELDS.
    """
    if not isinstance(product, dict):
        raise TypeError("product must be a dictionary")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    # Create a shallow copy to avoid mutating the original product unintentionally
    updated_product = product.copy()

    for key, value in data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update")

        # Prevent execution of arbitrary code by rejecting callables
        if callable(value):
            raise ValueError(f"Value for field '{key}' cannot be a callable")

        # Optional: Basic type checks could be added here if desired
        updated_product[key] = value

    return updated_product