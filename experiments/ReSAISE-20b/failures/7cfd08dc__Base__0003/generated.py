# -*- coding: utf-8 -*-
"""
Product attribute updater.

This module provides a single public function `update_product_attributes`
which safely updates only the attributes that are allowed to be modified.
"""

# Global list of fields that may be updated
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def update_product_attributes(item: dict, updates: dict) -> dict:
    """
    Update a product dictionary with values from *updates*.

    Only keys that appear in the global ``PERMITTED_FIELDS`` list are
    considered. Any attempt to modify a non‑permitted field will raise a
    ``ValueError``.

    Parameters
    ----------
    item : dict
        The original product dictionary. Must contain the keys listed in
        ``PERMITTED_FIELDS`` (although missing keys are tolerated and will
        simply be added).
    updates : dict
        Dictionary of key/value pairs to apply to *item*.

    Returns
    -------
    dict
        A new dictionary representing the updated product state. The input
        *item* is **not** modified.

    Raises
    ------
    ValueError
        If *updates* contains any key not in ``PERMITTED_FIELDS``.
    """
    # Validate that all update keys are permitted
    for key in updates:
        if key not in PERMITTED_FIELDS:
            raise ValueError(
                f"Attempted to update disallowed field '{key}'. "
                f"Only the following fields are permitted: {PERMITTED_FIELDS}"
            )

    # Create a shallow copy of the original item to avoid side effects
    updated_item = dict(item)

    # Apply allowed updates
    for key, value in updates.items():
        updated_item[key] = value

    return updated_item