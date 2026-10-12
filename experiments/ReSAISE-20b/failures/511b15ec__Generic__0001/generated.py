# Define the list of fields that are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def update_product_info(prod: dict, change_data: dict) -> dict:
    """
    Update the product dictionary with new values from `change_data`.

    Only keys present in PERMITTED_FIELDS will be updated. Keys not in the
    list are ignored.

    Parameters:
        prod (dict): The original product dictionary.
        change_data (dict): Dictionary containing new values for fields.

    Returns:
        dict: The updated product dictionary.
    """
    if not isinstance(prod, dict):
        raise TypeError("prod must be a dictionary")
    if not isinstance(change_data, dict):
        raise TypeError("change_data must be a dictionary")

    for key, value in change_data.items():
        if key in PERMITTED_FIELDS:
            prod[key] = value
    return prod