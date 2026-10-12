# update_item_details.py

"""
Utility to safely update product information in an inventory dictionary.

Only keys listed in PERMITTED_FIELDS are allowed to be updated.
"""

from typing import Dict, Any

# Define the set of fields that may be modified
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_item_details(inventory: Dict[str, Any], update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an inventory item's attributes based on the provided update_data.

    Parameters
    ----------
    inventory : dict
        The original product dictionary. Must contain keys for each permitted field.
    update_data : dict
        Dictionary of fields to update. Only keys in PERMITTED_FIELDS are considered.

    Returns
    -------
    dict
        A new dictionary with the updated values applied to the original inventory.

    Raises
    ------
    ValueError
        If any key in update_data is not permitted.
    TypeError
        If inventory or update_data are not dictionaries.
    """
    if not isinstance(inventory, dict):
        raise TypeError("inventory must be a dictionary")
    if not isinstance(update_data, dict):
        raise TypeError("update_data must be a dictionary")

    # Create a shallow copy to avoid mutating the original inventory
    updated_inventory = dict(inventory)

    for key, value in update_data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")
        # Optional: add type checks for each permitted field
        if key == "price":
            if not isinstance(value, (int, float)):
                raise TypeError("price must be a number")
            if value < 0:
                raise ValueError("price cannot be negative")
        elif key == "stock":
            if not isinstance(value, int):
                raise TypeError("stock must be an integer")
            if value < 0:
                raise ValueError("stock cannot be negative")
        elif key == "category":
            if not isinstance(value, str):
                raise TypeError("category must be a string")
        elif key == "description":
            if not isinstance(value, str):
                raise TypeError("description must be a string")

        updated_inventory[key] = value

    return updated_inventory