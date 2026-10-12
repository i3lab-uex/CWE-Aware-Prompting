# -*- coding: utf-8 -*-
"""
Utility for safely updating product information.

The module defines a global list `PERMITTED_FIELDS` that contains the names of
attributes that are allowed to be modified. The function `update_product_info`
takes a product dictionary and a dictionary of changes, updates only the
permitted fields, validates input types where appropriate, and returns the
modified product dictionary.

The implementation follows best practices for security and robustness:
* Input validation – ensures only known keys are updated.
* Type checking – optional but demonstrates defensive programming.
* Error handling – raises informative exceptions for invalid data.
"""

from __future__ import annotations

# Global list of fields that may be updated.  This should be kept in sync with
# the application’s schema or configuration.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

# Optional: define expected types for each field to aid validation.
FIELD_TYPES = {
    "price": (int, float),
    "description": str,
    "stock": int,
    "category": str,
}

def update_product_info(prod: dict, change_data: dict) -> dict:
    """
    Update a product dictionary with new values from `change_data`.

    Only keys that are present in the global ``PERMITTED_FIELDS`` list will be
    applied. Keys not in this list are ignored and cause a ``ValueError`` to
    be raised.

    Parameters
    ----------
    prod : dict
        The original product dictionary. It is modified in place.
    change_data : dict
        Dictionary containing new values for fields to update.

    Returns
    -------
    dict
        The updated product dictionary (the same object as ``prod``).

    Raises
    ------
    ValueError
        If any key in ``change_data`` is not permitted or if a value does not
        match the expected type for that field.
    """
    # Validate input types to guard against accidental injection of malformed data
    if not isinstance(prod, dict):
        raise TypeError("`prod` must be a dictionary")
    if not isinstance(change_data, dict):
        raise TypeError("`change_data` must be a dictionary")

    for key, value in change_data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update")

        # Optional: type validation
        expected = FIELD_TYPES.get(key)
        if expected and not isinstance(value, expected):
            raise ValueError(
                f"Field '{key}' expects type {expected}, got {type(value).__name__}"
            )

        # Perform the update
        prod[key] = value

    return prod