# -*- coding: utf-8 -*-

"""
Utility to safely modify product data.

The function `modify_product_data` updates only the fields listed in
the global `PERMITTED_FIELDS`.  It performs defensive checks to avoid
unintended modifications or security issues such as arbitrary code
execution.

Author: OpenAI ChatGPT
"""

# List of fields that are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def modify_product_data(product_details: dict, update_info: dict) -> dict:
    """
    Update a product's attributes with the provided values, but only
    for fields that are explicitly permitted.

    Args:
        product_details: A dictionary containing the current
            product information. It is not modified in place; a new
            dictionary is returned.
        update_info: A dictionary containing key/value pairs to be
            merged into `product_details`. Only keys present in
            PERMITTED_FIELDS are considered.

    Returns:
        A new dictionary containing the updated product data.

    Raises:
        TypeError: If either argument is not a dict.
    """
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a dictionary")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a dictionary")

    # Create a shallow copy to avoid mutating the original
    updated_product = product_details.copy()

    for field, value in update_info.items():
        if field in PERMITTED_FIELDS:
            # Basic type validation could be added here if needed
            updated_product[field] = value

    return updated_product