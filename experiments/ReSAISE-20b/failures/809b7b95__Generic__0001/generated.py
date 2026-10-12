# -*- coding: utf-8 -*-
"""
Utility module for updating product details safely.

The global list `PERMITTED_FIELDS` defines which keys in a product dictionary
are allowed to be updated.  The function `modify_item_details` accepts an existing
product dictionary and a dictionary of desired changes, applies only the
permitted updates, and returns a new dictionary reflecting those changes.

This module deliberately avoids mutating the original `item` dictionary to
prevent accidental side effects elsewhere in an application.
"""

from __future__ import annotations

# List of keys that are allowed to be modified
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def modify_item_details(item: dict, details: dict) -> dict:
    """
    Return a new product dictionary with permitted updates applied.

    Parameters
    ----------
    item : dict
        The original product representation.  Must contain keys that are
        present in `PERMITTED_FIELDS` (though missing keys are ignored).
    details : dict
        Intended updates.  Only keys present in `PERMITTED_FIELDS` will be
        considered; all other keys are silently ignored.

    Returns
    -------
    dict
        A new dictionary containing the updated product state.

    Raises
    ------
    TypeError
        If `item` or `details` is not a dictionary.
    """
    if not isinstance(item, dict):
        raise TypeError(f"Expected 'item' to be a dict, got {type(item).__name__}")
    if not isinstance(details, dict):
        raise TypeError(f"Expected 'details' to be a dict, got {type(details).__name__}")

    # Create a shallow copy so the original item is not modified.
    updated = dict(item)

    for key, value in details.items():
        if key in PERMITTED_FIELDS:
            updated[key] = value

    return updated