#!/usr/bin/env python3
"""
Utility for updating product information with controlled field modification.
"""

from typing import Dict, Any

# Only these keys are allowed to be modified by the caller
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def _validate_update_data(update_data: Dict[str, Any]) -> None:
    """
    Internal helper to ensure that the update data contains only permitted fields
    and that values are of acceptable types.

    Raises:
        ValueError: If an unpermitted field is present or if a value type is
                    inappropriate for the expected attribute.
    """
    for key, value in update_data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")

        # Basic type checks – adjust as needed for your domain
        if key == "price":
            if not isinstance(value, (int, float)):
                raise ValueError("Price must be a number.")
            if value < 0:
                raise ValueError("Price cannot be negative.")

        elif key == "stock":
            if not isinstance(value, int):
                raise ValueError("Stock must be an integer.")
            if value < 0:
                raise ValueError("Stock cannot be negative.")

        elif key == "description":
            if not isinstance(value, str):
                raise ValueError("Description must be a string.")

        elif key == "category":
            if not isinstance(value, str):
                raise ValueError("Category must be a string.")


def update_item_details(inventory: Dict[str, Any], update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an inventory item's attributes with the provided data.

    Parameters
    ----------
    inventory : dict
        The current product dictionary. It may contain any keys, but only
        those in PERMITTED_FIELDS are eligible for modification.
    update_data : dict
        The dictionary of fields and values intended for the update.

    Returns
    -------
    dict
        A new dictionary representing the updated product. The original
        `inventory` dictionary is not mutated.

    Raises
    ------
    ValueError
        If an attempt is made to modify a field that is not in
        PERMITTED_FIELDS, or if any value fails basic type validation.
    """
    # Validate incoming data first
    _validate_update_data(update_data)

    # Create a shallow copy to avoid mutating the original dictionary
    updated_inventory = inventory.copy()

    # Apply permitted updates
    for field in PERMITTED_FIELDS:
        if field in update_data:
            updated_inventory[field] = update_data[field]

    return updated_inventory