# -*- coding: utf-8 -*-
"""
Utility for updating product inventory safely.

The module exposes a single public function `update_item_details` which
ensures that only fields listed in the global `PERMITTED_FIELDS` list
can be modified. Attempting to modify any other field raises a
``ValueError``.

CWE-913 (Improper Control of Dynamically-Managed Code Resources) is
avoided by explicitly filtering keys and never executing or importing
code based on user input.
"""

from __future__ import annotations

from typing import Dict, Any

# Fields that are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def update_item_details(
    inventory: Dict[str, Any], update_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Return a new product dictionary with permitted fields updated.

    Parameters
    ----------
    inventory : dict
        The original product data.
    update_data : dict
        A dictionary containing the fields and values to be updated.

    Returns
    -------
    dict
        A new dictionary with the updates applied. The original `inventory`
        is left untouched.

    Raises
    ------
    ValueError
        If any key in `update_data` is not listed in `PERMITTED_FIELDS`.
    """
    # Create a shallow copy to avoid mutating the caller's data.
    updated_inventory = inventory.copy()

    for key, value in update_data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(
                f"Field '{key}' is not permitted for update. "
                f"Allowed fields: {sorted(PERMITTED_FIELDS)}"
            )
        updated_inventory[key] = value

    return updated_inventory