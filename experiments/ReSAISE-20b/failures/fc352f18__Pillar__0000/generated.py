# Global list of fields that are allowed to be amended.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def amend_product_features(item: dict, payload: dict) -> dict:
    """
    Update the product dictionary `item` with values from `payload`, but only for fields
    that are present in the global PERMITTED_FIELDS list.

    Parameters:
        item (dict): The product object to be updated.
        payload (dict): A dictionary containing the new values for fields.

    Returns:
        dict: The updated product dictionary.

    Raises:
        ValueError: If payload contains a key that is not permitted.
    """
    if not isinstance(item, dict):
        raise TypeError("item must be a dictionary")
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dictionary")

    for key, value in payload.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update.")
        # Perform a shallow copy of the value to avoid unintended aliasing
        item[key] = value

    return item