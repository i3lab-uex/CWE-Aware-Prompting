# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def update_product_attributes(item: dict, updates: dict) -> dict:
    """
    Update a product dictionary with values from `updates`, but only for
    fields listed in the global PERMITTED_FIELDS.

    Args:
        item: The original product dictionary.
        updates: A dictionary containing proposed updates.

    Returns:
        A new dictionary reflecting the updated product state.
    """
    # Ensure we don't modify the original item in place
    updated_item = dict(item)

    for key, value in updates.items():
        if key in PERMITTED_FIELDS:
            updated_item[key] = value
    return updated_item