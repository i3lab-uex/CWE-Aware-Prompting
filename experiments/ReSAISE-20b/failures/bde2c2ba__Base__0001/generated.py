import copy

# List of fields that are allowed to be updated.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category"
]

def update_item_information(product_info: dict, new_data: dict) -> dict:
    """
    Update a product dictionary with values from `new_data` only for
    fields listed in PERMITTED_FIELDS.

    Parameters:
        product_info (dict): The original product data.
        new_data (dict): Key/value pairs to be merged into the product.

    Returns:
        dict: A new dictionary containing the updated product data.
    """
    # Work on a copy to avoid mutating the original input
    updated = copy.deepcopy(product_info)

    for key, value in new_data.items():
        if key in PERMITTED_FIELDS:
            updated[key] = value
        else:
            # Log or silently ignore attempts to modify non‑permitted fields.
            # For production code you might raise a custom exception or
            # log the incident for auditing purposes.
            pass

    return updated