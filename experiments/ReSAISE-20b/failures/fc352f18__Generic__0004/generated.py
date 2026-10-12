# Global list of fields that are allowed to be updated
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def amend_product_features(item: dict, payload: dict) -> dict:
    """
    Update a product dictionary with values from `payload` only for fields
    that are present in the global PERMITTED_FIELDS list.

    Args:
        item (dict): The original product dictionary.
        payload (dict): Dictionary containing new values for fields.

    Returns:
        dict: The updated product dictionary.
    """
    # Ensure we are working with a copy to avoid mutating the original
    updated_item = item.copy()

    for key, value in payload.items():
        if key in PERMITTED_FIELDS:
            updated_item[key] = value

    return updated_item