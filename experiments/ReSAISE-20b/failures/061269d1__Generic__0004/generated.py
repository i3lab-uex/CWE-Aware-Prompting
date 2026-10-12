# -*- coding: utf-8 -*-
"""
Utility module for editing product information.
"""

from __future__ import annotations

# Define the list of fields that can be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def edit_product_info(item: dict, details: dict) -> dict:
    """
    Update a product dictionary with permitted fields.

    Parameters
    ----------
    item : dict
        The original product information.
    details : dict
        A dictionary containing fields and values intended for update.

    Returns
    -------
    dict
        The updated product dictionary. Only keys listed in
        :data:`PERMITTED_FIELDS` are modified; all other keys remain unchanged.

    Notes
    -----
    * The function performs a shallow copy of ``item`` to avoid mutating the
      caller's data.
    * If a key in ``details`` is not part of :data:`PERMITTED_FIELDS`,
      it is silently ignored to prevent accidental data leakage.
    * Keys present in ``details`` but missing from ``item`` are added
      only if they are permitted.
    """
    # Create a shallow copy to avoid side effects on the original dictionary
    updated = dict(item)

    for key, value in details.items():
        if key not in PERMITTED_FIELDS:
            # Ignore disallowed fields
            continue

        # Apply the update (or add new key if missing)
        updated[key] = value

    return updated