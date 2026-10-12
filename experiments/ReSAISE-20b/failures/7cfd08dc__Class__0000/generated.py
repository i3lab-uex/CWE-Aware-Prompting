# -*- coding: utf-8 -*-
"""
Utility module for safely updating product attributes.
"""

from __future__ import annotations

# List of fields that are allowed to be updated.  This list should be maintained
# by the application and never exposed for modification at runtime.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_product_attributes(item: dict, updates: dict) -> dict:
    """
    Return a new product dictionary with permitted fields updated.

    Parameters
    ----------
    item : dict
        The original product representation.  Keys must be strings.
    updates : dict
        A mapping of field names to new values.  Only keys present in
        ``PERMITTED_FIELDS`` will be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated product state.  The original
        ``item`` is not modified.

    Raises
    ------
    TypeError
        If either ``item`` or ``updates`` is not a dictionary.
    ValueError
        If any key in ``updates`` is not a string.

    Notes
    -----
    This function does **not** execute any code present in the values of
    ``updates``; it merely assigns them.  This protects against CWE-913
    (Improper Control of Dynamically‑Managed Code Resources) by ensuring that
    no executable code is inadvertently run.
    """
    if not isinstance(item, dict):
        raise TypeError("item must be a dictionary")
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    # Shallow copy to avoid mutating the original product
    updated_item = item.copy()

    for key, value in updates.items():
        if not isinstance(key, str):
            raise ValueError(f"update key {key!r} is not a string")
        if key in PERMITTED_FIELDS:
            updated_item[key] = value

    return updated_item