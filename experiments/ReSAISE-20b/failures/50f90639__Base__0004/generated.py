# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
    # add other allowed fields here
]

def modify_product_details(product: dict, data: dict) -> dict:
    """
    Update a product dictionary with values from `data` but only for fields
    that are present in the global PERMITTED_FIELDS list.

    Args:
        product: The original product dictionary.
        data: A dictionary containing field-value pairs to update.

    Returns:
        A new dictionary with the updates applied.

    Raises:
        TypeError: If `product` or `data` is not a dictionary.
        ValueError: If any key in `data` is not permitted.

    Notes:
        - The function does **not** modify the original `product` dictionary.
        - Keys that are not in PERMITTED_FIELDS raise a ValueError to prevent
          accidental or malicious updates (CWE-915 mitigation).
    """
    if not isinstance(product, dict):
        raise TypeError("product must be a dictionary")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    # Validate that all keys in data are permitted
    invalid_keys = [k for k in data if k not in PERMITTED_FIELDS]
    if invalid_keys:
        raise ValueError(f"Attempted to update disallowed fields: {invalid_keys}")

    # Create a shallow copy of the product to avoid mutating the input
    updated_product = product.copy()

    # Apply permitted updates
    for key, value in data.items():
        updated_product[key] = value

    return updated_product