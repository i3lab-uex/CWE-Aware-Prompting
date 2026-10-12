# -*- coding: utf-8 -*-
"""
Utility module for product data manipulation.
"""

from __future__ import annotations

# Define the list of fields that are allowed to be edited.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def edit_product_info(item: dict, details: dict) -> dict:
    """
    Update a product dictionary with new values from *details*.

    Only keys present in the global :data:`PERMITTED_FIELDS` list will be
    considered for modification. All other keys are ignored to avoid
    accidental tampering with sensitive or internal fields.

    Parameters
    ----------
    item : dict
        The original product dictionary. It is modified in-place and also
        returned for convenience.
    details : dict
        A mapping of field names to new values. Only keys that exist in
        :data:`PERMITTED_FIELDS` will be applied.

    Returns
    -------
    dict
        The same dictionary object that was passed in, now updated with the
        permitted changes.

    Raises
    ------
    TypeError
        If *item* or *details* is not a mapping.
    """
    if not isinstance(item, dict):
        raise TypeError(f"item must be a dict; got {type(item).__name__}")
    if not isinstance(details, dict):
        raise TypeError(f"details must be a dict; got {type(details).__name__}")

    # Update only permitted fields.
    for key, value in details.items():
        if key in PERMITTED_FIELDS:
            item[key] = value

    return item