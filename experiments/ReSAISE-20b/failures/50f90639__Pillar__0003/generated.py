from __future__ import annotations

# Allowed fields that may be updated.  Extend as needed.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def modify_product_details(product: dict, data: dict) -> dict:
    """
    Update a product dictionary with values from *data* only for fields that are
    explicitly permitted.  The function returns a new dictionary; the original
    *product* is left untouched.

    Args:
        product: The original product dictionary.
        data: Dictionary containing the fields to update.

    Returns:
        A new dictionary representing the modified product.

    Raises:
        ValueError: If *product* is not a mapping or if any key in *data*
                    is not permitted.
    """
    if not isinstance(product, dict):
        raise ValueError("product must be a dictionary")

    # Create a shallow copy so we do not mutate the original
    updated_product = product.copy()

    for key, value in data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update")

        # Basic type validation could be added here if needed
        updated_product[key] = value

    return updated_product