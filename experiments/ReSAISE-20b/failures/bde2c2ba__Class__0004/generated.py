# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def update_item_information(product_info: dict, new_data: dict) -> dict:
    """
    Update a product dictionary with values from `new_data` only for keys that
    are present in the global PERMITTED_FIELDS list.

    Args:
        product_info (dict): Original product data.
        new_data (dict): Desired updates.

    Returns:
        dict: A new dictionary containing the updated product data.
    """
    # Create a shallow copy to avoid mutating the original input
    updated_product = product_info.copy()

    for key, value in new_data.items():
        if key in PERMITTED_FIELDS:
            updated_product[key] = value

    return updated_product