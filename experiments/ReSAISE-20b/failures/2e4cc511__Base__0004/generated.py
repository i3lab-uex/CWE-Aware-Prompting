# -*- coding: utf-8 -*-
"""
Utility to update product details while restricting modifications to a whitelisted set of fields.
"""

# List of fields that are allowed to be updated
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def update_item_details(inventory: dict, update_data: dict) -> dict:
    """
    Update the given inventory dictionary with values from update_data, but only for fields
    listed in PERMITTED_FIELDS.

    Parameters
    ----------
    inventory : dict
        The original product dictionary to be updated.
    update_data : dict
        Dictionary containing field names and new values.

    Returns
    -------
    dict
        A new dictionary representing the updated product. The original `inventory`
        is not modified.

    Raises
    ------
    ValueError
        If update_data contains keys that are not in PERMITTED_FIELDS.
    TypeError
        If `inventory` or `update_data` is not a dictionary.

    Notes
    -----
    - This function performs a shallow copy of `inventory` before applying updates,
      ensuring that the original dictionary remains unchanged.
    - Only keys explicitly listed in PERMITTED_FIELDS are considered; any other
      key causes a ValueError to prevent unintended modifications (CWE-915 mitigation).
    """
    if not isinstance(inventory, dict):
        raise TypeError("inventory must be a dictionary")
    if not isinstance(update_data, dict):
        raise TypeError("update_data must be a dictionary")

    # Validate that all requested updates are permitted
    for key in update_data:
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update")

    # Create a shallow copy to avoid mutating the original
    updated_inventory = inventory.copy()

    # Apply permitted updates
    for key, value in update_data.items():
        updated_inventory[key] = value

    return updated_inventory