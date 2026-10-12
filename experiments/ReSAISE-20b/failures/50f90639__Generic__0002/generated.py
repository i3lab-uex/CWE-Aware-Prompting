# -*- coding: utf-8 -*-

"""
Utility module for product data manipulation.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global configuration: fields that are allowed to be modified
# --------------------------------------------------------------------------- #
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
    "name",
    "sku",
]

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #
def modify_product_details(product: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values from ``data`` while ensuring that
    only fields listed in :data:`PERMITTED_FIELDS` are modified.

    Parameters
    ----------
    product:
        The original product dictionary. It will not be mutated; a new dictionary
        containing the updated values is returned.
    data:
        Dictionary of fields to be updated. Keys that are not present in
        :data:`PERMITTED_FIELDS` will be ignored.

    Returns
    -------
    Dict[str, Any]
        A new dictionary containing the merged product data.

    Raises
    ------
    TypeError
        If either ``product`` or ``data`` is not a mapping.
    """
    if not isinstance(product, dict):
        raise TypeError(f"product must be a mapping, got {type(product)!r}")
    if not isinstance(data, dict):
        raise TypeError(f"data must be a mapping, got {type(data)!r}")

    # Work on a shallow copy to avoid side effects
    updated_product = copy.deepcopy(product)

    for key, value in data.items():
        if key not in PERMITTED_FIELDS:
            # Skip any field that is not permitted to be modified
            continue

        # Optional: basic type validation can be added here.
        # For example, ensure price is numeric and non‑negative:
        if key == "price":
            try:
                float_value = float(value)
                if float_value < 0:
                    raise ValueError("price cannot be negative")
                value = float_value
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid price value: {value!r}") from exc

        # For stock, ensure integer and non‑negative
        if key == "stock":
            try:
                int_value = int(value)
                if int_value < 0:
                    raise ValueError("stock cannot be negative")
                value = int_value
            except (TypeError, ValueError) as exc:
                raise ValueError(f"Invalid stock value: {value!r}") from exc

        # Assign the validated value
        updated_product[key] = value

    return updated_product


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    original = {
        "id": 101,
        "name": "Wireless Mouse",
        "price": 25.99,
        "description": "Ergonomic wireless mouse",
        "stock": 120,
        "category": "Electronics",
    }

    changes = {
        "price": 22.5,
        "stock": 115,
        "description": "Updated ergonomic wireless mouse",
        "color": "black",          # not permitted, will be ignored
    }

    updated = modify_product_details(original, changes)
    print("Original:", original)
    print("Updated :", updated)