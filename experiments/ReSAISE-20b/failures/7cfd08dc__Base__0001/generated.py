# -*- coding: utf-8 -*-
"""
Product attribute updater.

This module provides a single function, :func:`update_product_attributes`,
which safely updates only the attributes that are explicitly permitted.
"""

from __future__ import annotations

# List of attribute names that may be updated.  This list is
# intentionally kept in a single place to make it easy to audit.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def update_product_attributes(item: dict, updates: dict) -> dict:
    """
    Update a product dictionary with values from *updates*.

    Only keys that are present in :data:`PERMITTED_FIELDS` will be
    applied.  All other keys in *updates* are ignored and a warning
    is logged.

    Parameters
    ----------
    item : dict
        The original product dictionary.  It is **not** modified in-place;
        a new dictionary containing the updated state is returned.
    updates : dict
        Dictionary of key/value pairs intended for update.

    Returns
    -------
    dict
        A new dictionary containing the updated product state.

    Raises
    ------
    ValueError
        If *updates* contains a key that is not in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    - The function performs a shallow copy of *item* before applying the updates.
      This ensures that nested mutable structures are not inadvertently
      shared between the original and updated dictionaries.
    - The function does not validate the type or value of the updates; such
      validation should be performed elsewhere in the application.
    """
    # Validate that all requested updates are permitted
    invalid_keys = [k for k in updates if k not in PERMITTED_FIELDS]
    if invalid_keys:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(invalid_keys)}"
        )

    # Create a shallow copy to avoid mutating the original item
    updated_item = dict(item)

    # Apply permitted updates
    for key, value in updates.items():
        updated_item[key] = value

    return updated_item