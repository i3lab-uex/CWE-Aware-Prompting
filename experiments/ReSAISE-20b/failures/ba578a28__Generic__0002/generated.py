# -*- coding: utf-8 -*-

"""
Product data modifier.

The module defines a single public function `modify_product_data` that updates
a product dictionary only for fields listed in the global PERMITTED_FIELDS list.
"""

from __future__ import annotations

from typing import Dict, Any, Iterable


# --------------------------------------------------------------------------- #
# Configuration: list of fields that are allowed to be modified
# --------------------------------------------------------------------------- #
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def modify_product_data(
    product_details: Dict[str, Any],
    update_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a product dictionary with permitted fields.

    Parameters
    ----------
    product_details : dict
        The original product data. It will be updated in place.
    update_info : dict
        Mapping of field names to new values.

    Returns
    -------
    dict
        The updated product dictionary (the same object that was passed in).

    Raises
    ------
    ValueError
        If any key in `update_info` is not present in ``PERMITTED_FIELDS``.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    * The function modifies ``product_details`` in place and returns the same
      dictionary for convenience.
    * The function performs a shallow update; nested structures are not deep‑copied
      or merged.
    """
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a dictionary")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a dictionary")

    permitted_set = set(PERMITTED_FIELDS)

    # Check for disallowed fields
    invalid_keys = [k for k in update_info if k not in permitted_set]
    if invalid_keys:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(invalid_keys)}"
        )

    # Apply updates
    product_details.update(update_info)

    return product_details


# --------------------------------------------------------------------------- #
# Example usage (commented out to keep module import side‑effect free)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    sample_product = {
        "price": 19.99,
        "description": "A great gadget",
        "stock": 50,
        "category": "electronics",
    }

    updates = {"price": 17.99, "stock": 45}

    try:
        updated_product = modify_product_data(sample_product, updates)
        print("Updated product:", updated_product)
    except Exception as exc:
        print(f"Error: {exc}")