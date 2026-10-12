# -*- coding: utf-8 -*-
"""
Utility module for updating product information safely.
"""

from typing import Dict, Any

# List of fields that are allowed to be updated
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_item_details(inventory: Dict[str, Any], update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an inventory item with the provided data.

    Parameters
    ----------
    inventory : dict
        The product dictionary to be updated. It must contain keys for all
        permitted fields.
    update_data : dict
        A dictionary containing the fields and values intended for update.

    Returns
    -------
    dict
        The updated product dictionary.

    Raises
    ------
    ValueError
        If `update_data` contains keys that are not in ``PERMITTED_FIELDS``.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    The function performs an in‑place update of the ``inventory`` dictionary
    and then returns it. No new objects are created, so the caller can use
    the returned dictionary directly.

    Security Considerations
    -----------------------
    * The function only accepts updates for keys listed in ``PERMITTED_FIELDS``.
      This prevents arbitrary modification of the inventory dictionary
      (CWE‑913: Improper Control of Dynamically‑Managed Code Resources).
    * No use of ``eval`` or dynamic code execution is performed.
    """
    if not isinstance(inventory, dict):
        raise TypeError("inventory must be a dictionary")
    if not isinstance(update_data, dict):
        raise TypeError("update_data must be a dictionary")

    # Verify that all requested updates are permitted
    invalid_keys = [k for k in update_data if k not in PERMITTED_FIELDS]
    if invalid_keys:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(invalid_keys)}"
        )

    # Apply updates
    for key, value in update_data.items():
        inventory[key] = value

    return inventory