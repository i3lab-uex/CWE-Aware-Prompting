# -*- coding: utf-8 -*-

"""
Product data modifier.

This module defines a function that safely updates only the
attributes listed in `PERMITTED_FIELDS`.  It avoids any
dynamic code execution and validates input types to mitigate
CWE-913 (Improper Control of Dynamically‑Managed Code Resources).
"""

from __future__ import annotations

from typing import Dict, Any, Iterable


# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS: tuple[str, ...] = (
    "price",
    "description",
    "stock",
    "category",
)


def _is_valid_field(field: str) -> bool:
    """
    Check whether a field is permitted for update.
    """
    return field in PERMITTED_FIELDS


def modify_product_data(
    product_details: Dict[str, Any],
    update_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a product dictionary with values from `update_info`
    but only for keys listed in `PERMITTED_FIELDS`.

    Parameters
    ----------
    product_details : dict
        Existing product data.  The dictionary is modified in place.
    update_info : dict
        Proposed updates; keys that are not permitted are ignored.

    Returns
    -------
    dict
        The same dictionary instance as `product_details`, now updated.

    Notes
    -----
    * No new keys outside of ``PERMITTED_FIELDS`` are added.
    * The function does not perform type validation on the values; callers
      should ensure they provide appropriate data types.
    * No evaluation or execution of code is performed, preventing
      CWE‑913 vulnerabilities.
    """
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a dictionary")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a dictionary")

    for key, value in update_info.items():
        if _is_valid_field(key):
            product_details[key] = value
    return product_details


# Example usage (for testing purposes only; remove or comment out in production)
if __name__ == "__main__":
    prod = {"price": 19.99, "description": "A nice item", "stock": 10}
    updates = {"price": 17.99, "category": "Sale", "unknown_field": 123}
    modified = modify_product_data(prod, updates)
    print(modified)  # {'price': 17.99, 'description': 'A nice item', 'stock': 10, 'category': 'Sale'}