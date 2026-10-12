# Global list of fields that are allowed to be updated
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def update_item_details(inventory: dict, update_data: dict) -> dict:
    """
    Update an inventory item with the provided data while enforcing a whitelist
    of permissible fields.

    Parameters:
        inventory (dict): The original product dictionary. Must contain
                           keys that match the permitted fields.
        update_data (dict): Dictionary of fields and new values to apply.

    Returns:
        dict: A new dictionary representing the updated product. The original
              `inventory` is not modified.

    Raises:
        ValueError: If `update_data` contains a field that is not in
                    PERMITTED_FIELDS.
    """
    # Validate update fields against the whitelist
    for field in update_data:
        if field not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{field}' is not permitted for update.")

    # Create a shallow copy to avoid mutating the original inventory
    updated = inventory.copy()

    # Apply permitted updates
    for field, value in update_data.items():
        updated[field] = value

    return updated