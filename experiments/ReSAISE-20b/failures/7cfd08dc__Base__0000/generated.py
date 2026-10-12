# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def update_product_attributes(item: dict, updates: dict) -> dict:
    """
    Update a product dictionary with values from `updates` only for fields that are
    present in the global PERMITTED_FIELDS set.

    Parameters:
        item (dict): The original product dictionary. It will be updated in place.
        updates (dict): Dictionary containing key-value pairs to update.

    Returns:
        dict: The updated product dictionary (same object as `item`).

    Raises:
        TypeError: If either argument is not a dictionary.
    """
    if not isinstance(item, dict):
        raise TypeError("item must be a dictionary")
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    for key, value in updates.items():
        if key in PERMITTED_FIELDS:
            item[key] = value

    return item