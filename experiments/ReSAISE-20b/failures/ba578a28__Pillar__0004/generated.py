# -*- coding: utf-8 -*-

"""
Product data modifier module.

This module defines a single public function, `modify_product_data`, which updates
fields of a product dictionary only if those fields are present in the global
`PERMITTED_FIELDS` list.  The function is careful to avoid mutating the original
product dictionary and does not perform any operations that could lead to a
resource‑management vulnerability (CWE‑664).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, Any, List


# --------------------------------------------------------------------------- #
# Configuration – only these fields are allowed to be updated.
PERMITTED_FIELDS: List[str] = [
    "price",
    "description",
    "stock",
    "category",
]


# --------------------------------------------------------------------------- #
def modify_product_data(product_details: Dict[str, Any],
                        update_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with permitted fields updated.

    Parameters
    ----------
    product_details : dict
        The original product data.  Must be a mapping of string keys to any values.
    update_info : dict
        Mapping containing the fields and new values that should be applied to the
        product.  Only keys present in :data:`PERMITTED_FIELDS` will be considered.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.  The original
        `product_details` is left untouched.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If `product_details` does not contain all required keys that are being
        updated.  This ensures the product remains consistent.

    Notes
    -----
    * The function performs a shallow copy of the original product to avoid
      accidental mutation.
    * Only top‑level keys are processed – nested dictionaries or lists are not
      recursively updated.
    * The function does **not** interact with external resources; thus it is
      safe from CWE‑664 (improper control of a resource through its lifetime).
    """
    # Validate input types
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a dictionary")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a dictionary")

    # Create a shallow copy to avoid side effects
    updated_product: Dict[str, Any] = deepcopy(product_details)

    for field, new_value in update_info.items():
        if field not in PERMITTED_FIELDS:
            # Ignore or raise? We choose to ignore silently.
            continue

        if field not in product_details:
            # Prevent creation of unexpected keys – maintain consistency.
            raise ValueError(f"Field '{field}' is not a valid product attribute")

        # Apply the update
        updated_product[field] = new_value

    return updated_product


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage
    product = {
        "price": 19.99,
        "description": "A useful widget",
        "stock": 42,
        "category": "Tools",
    }

    updates = {"price": 17.99, "stock": 40, "color": "red"}  # 'color' is ignored

    new_product = modify_product_data(product, updates)
    print("Original:", product)
    print("Updated :", new_product)