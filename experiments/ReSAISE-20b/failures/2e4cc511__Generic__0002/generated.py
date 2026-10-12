# -*- coding: utf-8 -*-

"""
Product inventory update module.

Provides a single public function `update_item_details` that updates
only permitted fields of an inventory record.
"""

from __future__ import annotations

# Global list of fields that may be modified
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_item_details(inventory: dict, update_data: dict) -> dict:
    """
    Update permitted fields of a product record.

    Parameters
    ----------
    inventory : dict
        The original product dictionary.  It is modified in place and also returned.
    update_data : dict
        Dictionary containing field/value pairs to apply.

    Returns
    -------
    dict
        The updated inventory record.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    KeyError
        If `update_data` contains a key that is not in :data:`PERMITTED_FIELDS`.
    """
    if not isinstance(inventory, dict):
        raise TypeError("inventory must be a dictionary")
    if not isinstance(update_data, dict):
        raise TypeError("update_data must be a dictionary")

    for key, value in update_data.items():
        if key not in PERMITTED_FIELDS:
            raise KeyError(f"Field '{key}' is not permitted for update")
        inventory[key] = value

    return inventory