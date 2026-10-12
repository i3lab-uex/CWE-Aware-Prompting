# -*- coding: utf-8 -*-
"""
Module: product_modifier

Provides a single public function `modify_product_data` that safely updates
product attributes. Only keys listed in the global `PERMITTED_FIELDS`
are allowed to be modified.

Security considerations:
- The function performs a whitelist check to avoid unintended
  modifications (CWE‑664).
- It returns the updated dictionary but does not expose any internal
  state that could be misused.
"""

from __future__ import annotations

# Whitelisted fields that may be updated
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def modify_product_data(
    product_details: dict[str, any],
    update_info: dict[str, any]
) -> dict[str, any]:
    """
    Update product details with allowed fields.

    Parameters
    ----------
    product_details : dict[str, any]
        Original product data. The dictionary is modified in place.
    update_info : dict[str, any]
        Proposed updates; only keys present in PERMITTED_FIELDS
        will be applied.

    Returns
    -------
    dict[str, any]
        The updated product dictionary.

    Notes
    -----
    - Keys not in PERMITTED_FIELDS are silently ignored.
    - The function does **not** create a copy; it mutates the input dict
      and returns the same reference for convenience.
    """
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a dictionary")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a dictionary")

    for key, value in update_info.items():
        if key in PERMITTED_FIELDS:
            product_details[key] = value
    return product_details

# Example usage (for demonstration purposes only)
if __name__ == "__main__":
    prod = {"price": 19.99, "description": "Old", "stock": 10, "category": "Books"}
    updates = {"price": 17.99, "stock": 15, "color": "red"}  # 'color' is ignored
    print(modify_product_data(prod, updates))