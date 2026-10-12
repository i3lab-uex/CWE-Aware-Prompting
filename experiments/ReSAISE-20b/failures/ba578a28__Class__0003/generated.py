#!/usr/bin/env python3
"""
Utility to safely modify product data.

The function `modify_product_data` updates only the fields that are
explicitly allowed by the global `PERMITTED_FIELDS` list. Any attempt to
modify a non‑permitted field results in a `ValueError`.  This protects
against unintended modifications and mitigates CWE‑913 by ensuring that
only the intended attributes are written.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

from typing import Dict, Any, Iterable


# Define which fields can be updated.  Add or remove names here as needed.
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)


def modify_product_data(
    product_details: Dict[str, Any],
    update_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    product_details : dict
        The original product data.  Must be a mutable mapping.
    update_info : dict
        Keys are field names to change; values are the new data.

    Returns
    -------
    dict
        The product dictionary after applying permitted updates.

    Raises
    ------
    ValueError
        If `update_info` contains a key that is not in `PERMITTED_FIELDS`.

    Notes
    -----
    * The function modifies the input dictionary in place and also returns it.
      If you need an untouched copy, pass a shallow copy of the original dict.
    * No type conversion is performed; callers must supply values of correct
      types for each field.
    """
    # Validate that all requested keys are permitted
    invalid_keys = [k for k in update_info if k not in PERMITTED_FIELDS]
    if invalid_keys:
        raise ValueError(
            f"Attempted to update non‑permitted fields: {', '.join(invalid_keys)}"
        )

    # Apply updates
    for key, value in update_info.items():
        product_details[key] = value

    return product_details


# Example usage (uncomment to test)
if __name__ == "__main__":
    product = {
        "price": 19.99,
        "description": "A useful gadget",
        "stock": 100,
        "category": "Tools",
    }

    updates = {"price": 17.99, "stock": 120}
    updated_product = modify_product_data(product, updates)
    print(updated_product)