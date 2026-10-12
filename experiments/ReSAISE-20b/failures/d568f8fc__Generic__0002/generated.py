# -*- coding: utf-8 -*-
"""
Utility module for product data adjustment.

The `adjust_product_data` function updates only the fields that are explicitly
allowed by the global `PERMITTED_FIELDS` list.  This protects against accidental
or malicious changes to sensitive or read‑only attributes.
"""

# Define the list of fields that are allowed to be modified.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def adjust_product_data(prod_info: dict, change_vals: dict) -> dict:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    prod_info : dict
        The original product dictionary.  It is modified in place.
    change_vals : dict
        Dictionary containing new values keyed by field names.

    Returns
    -------
    dict
        The updated product dictionary (same object as `prod_info`).

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    """
    if not isinstance(prod_info, dict):
        raise TypeError(f"prod_info must be a dict, got {type(prod_info).__name__}")
    if not isinstance(change_vals, dict):
        raise TypeError(f"change_vals must be a dict, got {type(change_vals).__name__}")

    for key, value in change_vals.items():
        if key in PERMITTED_FIELDS:
            prod_info[key] = value
    return prod_info

# Example usage (commented out to keep module clean):
# if __name__ == "__main__":
#     product = {"price": 19.99, "description": "Old desc", "stock": 10}
#     updates = {"price": 24.99, "category": "Books"}
#     print(adjust_product_data(product, updates))