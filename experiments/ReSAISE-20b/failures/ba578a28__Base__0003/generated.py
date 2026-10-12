# -*- coding: utf-8 -*-
"""
Secure product data modifier.

The module defines a single function `modify_product_data` that updates
product attributes only if they are explicitly permitted.  This protects
against CWE‑915 (Improperly Controlled Modification of Dynamically-
Determined Object Attributes).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# List of attributes that are allowed to be updated.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def _validate_field_name(field: str) -> None:
    """
    Ensure the field name is in PERMITTED_FIELDS.
    Raises a ValueError if it is not permitted.
    """
    if field not in PERMITTED_FIELDS:
        raise ValueError(f"Field '{field}' is not permitted for update.")

def _validate_field_value(field: str, value) -> None:
    """
    Basic type validation for each permitted field.
    This can be extended as needed.
    Raises a TypeError if the value type is incorrect.
    """
    if field == "price":
        if not isinstance(value, (int, float)):
            raise TypeError("Price must be a number.")
    elif field == "stock":
        if not isinstance(value, int):
            raise TypeError("Stock must be an integer.")
    elif field in ("description", "category"):
        if not isinstance(value, str):
            raise TypeError(f"{field.capitalize()} must be a string.")
    # No validation needed for other fields at the moment.

def modify_product_data(product_details: dict, update_info: dict) -> dict:
    """
    Update product attributes safely.

    Parameters
    ----------
    product_details : dict
        The original product data.
    update_info : dict
        A dictionary containing the fields and new values to apply.

    Returns
    -------
    dict
        The updated product dictionary.  If a field is not in
        `PERMITTED_FIELDS`, it will be ignored.

    Raises
    ------
    ValueError
        If an update field is not permitted.
    TypeError
        If a value does not match the expected type for its field.

    Notes
    -----
    The function performs a shallow copy of `product_details` to avoid
    mutating the input dictionary.
    """
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a dictionary.")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a dictionary.")

    updated_product = product_details.copy()

    for field, new_value in update_info.items():
        _validate_field_name(field)
        _validate_field_value(field, new_value)
        updated_product[field] = new_value

    return updated_product