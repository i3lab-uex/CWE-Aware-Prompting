# -*- coding: utf-8 -*-

"""
Product information updater.

This module defines a single public function `update_item_information` that
updates a product dictionary with new values supplied in another dictionary.
Only fields listed in the global `PERMITTED_FIELDS` are allowed to be updated.

The implementation follows best practices for safety and maintainability:
* A shallow copy of the original product is made to avoid mutating input
  arguments.
* The function validates that each key in `new_data` is permitted; otherwise
  a `ValueError` is raised.
* The function is documented and type annotated for clarity.
"""

from __future__ import annotations

# Global list of fields that are allowed to be updated
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def update_item_information(
    product_info: dict,
    new_data: dict
) -> dict:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    product_info : dict
        The original product dictionary.  Keys are expected to be strings.
    new_data : dict
        A mapping of field names to new values.  Only keys present in
        `PERMITTED_FIELDS` are applied; other keys cause a ``ValueError``.

    Returns
    -------
    dict
        A new dictionary containing the updated product information.

    Raises
    ------
    ValueError
        If any key in ``new_data`` is not present in ``PERMITTED_FIELDS``.

    Notes
    -----
    The function does **not** modify the original ``product_info`` dictionary.
    This ensures that the caller retains control over its own data, preventing
    unintended side effects (CWE‑664: Improper Control of a Resource Through its
    Lifetime).
    """
    if not isinstance(product_info, dict):
        raise TypeError("product_info must be a dictionary")
    if not isinstance(new_data, dict):
        raise TypeError("new_data must be a dictionary")

    # Create a shallow copy to avoid mutating the input
    updated_product = product_info.copy()

    # Validate and apply updates
    for key, value in new_data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(
                f"Field '{key}' is not permitted for update. "
                f"Allowed fields: {PERMITTED_FIELDS}"
            )
        updated_product[key] = value

    return updated_product