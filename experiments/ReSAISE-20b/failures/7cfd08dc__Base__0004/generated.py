# List of attributes that are allowed to be updated.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

def update_product_attributes(item: dict, updates: dict) -> dict:
    """
    Update the product dictionary with values from `updates` only for
    fields that are present in PERMITTED_FIELDS.

    Parameters:
        item (dict): Original product dictionary.
        updates (dict): Dictionary containing potential updates.

    Returns:
        dict: A new dictionary representing the updated product state.
    """
    # Create a shallow copy to avoid mutating the original item
    updated_item = dict(item)

    for key, value in updates.items():
        if key in PERMITTED_FIELDS:
            updated_item[key] = value

    return updated_item