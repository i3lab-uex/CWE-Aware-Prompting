import copy

# Fields that are allowed to be modified.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
    "name",
    "sku",
]

def modify_product_details(product: dict, data: dict) -> dict:
    """
    Update a product dictionary with new values provided in `data`.

    Only keys listed in PERMITTED_FIELDS are considered for update.
    The function does not modify the original `product` dictionary but
    returns a new dictionary containing the updated values.

    Parameters:
        product (dict): The original product data.
        data (dict): A dictionary containing keys and new values.

    Returns:
        dict: The updated product dictionary.

    Raises:
        TypeError: If `product` or `data` is not a dict.
    """
    if not isinstance(product, dict):
        raise TypeError("product must be a dictionary")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    # Create a shallow copy to avoid side effects.
    updated_product = copy.deepcopy(product)

    for key, value in data.items():
        if key not in PERMITTED_FIELDS:
            # Skip any fields that are not allowed to be updated.
            continue

        if key in product:
            # Simple type validation: price must be numeric, stock integer.
            if key == "price":
                if not isinstance(value, (int, float)):
                    raise ValueError("price must be a number")
            elif key == "stock":
                if not isinstance(value, int):
                    raise ValueError("stock must be an integer")

        # Apply the update.
        updated_product[key] = value

    return updated_product