# Define the list of fields that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def update_item_details(inventory: dict, update_data: dict) -> dict:
    """
    Update the attributes of a product in an inventory dictionary.

    Parameters
    ----------
    inventory : dict
        The original product dictionary to be updated.
    update_data : dict
        A dictionary containing field-value pairs intended for update.

    Returns
    -------
    dict
        The updated product dictionary.

    Raises
    ------
    ValueError
        If any key in `update_data` is not present in PERMITTED_FIELDS.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    The function mutates the original `inventory` dictionary in place.
    """
    if not isinstance(inventory, dict):
        raise TypeError("inventory must be a dictionary")
    if not isinstance(update_data, dict):
        raise TypeError("update_data must be a dictionary")

    # Ensure all update keys are permitted
    invalid_keys = set(update_data) - set(PERMITTED_FIELDS)
    if invalid_keys:
        raise ValueError(f"Attempted to update disallowed fields: {', '.join(invalid_keys)}")

    # Apply permitted updates
    for key, value in update_data.items():
        inventory[key] = value

    return inventory