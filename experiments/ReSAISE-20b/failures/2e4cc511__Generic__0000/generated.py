from __future__ import annotations

# Only these fields are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def update_item_details(inventory: dict, update_data: dict) -> dict:
    """
    Update a product's attributes in *inventory* with the values from
    *update_data*. Only keys listed in ``PERMITTED_FIELDS`` are applied.
    Any other key will raise a :class:`ValueError`.

    Parameters
    ----------
    inventory:
        The product dictionary to be updated.
    update_data:
        Dictionary of attributes that should be changed.

    Returns
    -------
    dict
        The updated product dictionary.
    """
    # Validate that all requested updates are permitted
    invalid_fields = set(update_data) - PERMITTED_FIELDS
    if invalid_fields:
        raise ValueError(
            f"Attempted to update disallowed fields: {sorted(invalid_fields)}"
        )

    # Apply permitted updates
    for key, value in update_data.items():
        inventory[key] = value

    return inventory