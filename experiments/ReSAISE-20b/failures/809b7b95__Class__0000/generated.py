import copy

# Global list of fields that are allowed to be modified.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def modify_item_details(item: dict, details: dict) -> dict:
    """
    Update an item's attributes with values from `details` only if the keys are
    present in PERMITTED_FIELDS. The original item is not mutated; a new dict
    reflecting the updated state is returned.

    Args:
        item (dict): The original product dictionary.
        details (dict): Dictionary of key/value pairs to apply as updates.

    Returns:
        dict: A new dictionary containing the updated product data.

    Raises:
        TypeError: If `item` or `details` is not a dictionary.
    """
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary")
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary")

    # Create a shallow copy to avoid mutating the original item.
    updated_item = copy.deepcopy(item)

    for key, value in details.items():
        if key in PERMITTED_FIELDS:
            updated_item[key] = value

    return updated_item