# Global list of fields that are allowed to be updated
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
    Update a product dictionary with the provided data.

    Only keys that are present in PERMITTED_FIELDS will be updated.
    The function returns a new dictionary containing the modified product
    data, leaving the original `product` unchanged.

    Parameters:
        product (dict): Original product data.
        data (dict): Fields to update with their new values.

    Returns:
        dict: The updated product dictionary.
    """
    if not isinstance(product, dict):
        raise TypeError("product must be a dictionary")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    # Create a copy to avoid mutating the original product
    updated_product = product.copy()

    for key, value in data.items():
        if key in PERMITTED_FIELDS:
            updated_product[key] = value

    return updated_product