# -*- coding: utf-8 -*-
"""
Utility module for updating product information safely.

The function `update_item_information` copies the original product
dictionary and applies updates only for fields listed in
the global `PERMITTED_FIELDS` sequence. This prevents accidental or
malicious modification of non‑permitted attributes.

The implementation is intentionally minimal and free from dynamic
code execution or other security risks such as CWE‑913.
"""

from __future__ import annotations

# Define the list of fields that are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def update_item_information(
    product_info: dict,
    new_data: dict
) -> dict:
    """
    Return a new product dictionary with updates applied only to
    permitted fields.

    Parameters
    ----------
    product_info : dict
        Original product data.  Must be a mapping of keys to values.
    new_data : dict
        Proposed updates.  Only keys present in `PERMITTED_FIELDS` are
        applied.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.
    """
    if not isinstance(product_info, dict):
        raise TypeError("product_info must be a dictionary")
    if not isinstance(new_data, dict):
        raise TypeError("new_data must be a dictionary")

    # Create a shallow copy to avoid mutating the original.
    updated = product_info.copy()

    for key, value in new_data.items():
        if key in PERMITTED_FIELDS:
            updated[key] = value

    return updated