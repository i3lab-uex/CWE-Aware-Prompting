import copy

# Only these keys are allowed to be updated
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def modify_product_data(product_details: dict, update_info: dict) -> dict:
    """
    Update a product dictionary with values from `update_info` only for
    fields listed in PERMITTED_FIELDS.

    Parameters
    ----------
    product_details : dict
        The original product data. It may contain any keys, but only the
        permitted ones can be modified.
    update_info : dict
        Dictionary containing keys and values intended for the update.

    Returns
    -------
    dict
        A new dictionary containing the updated product data. The original
        `product_details` is left untouched.

    Raises
    ------
    ValueError
        If any key in `update_info` is not present in PERMITTED_FIELDS.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    * A shallow copy of the product data is made to avoid mutating the input.
    * The function does not perform type validation on field values; callers
      should ensure the data is valid for their use case.
    """
    if not isinstance(product_details, dict):
        raise TypeError("product_details must be a dictionary")
    if not isinstance(update_info, dict):
        raise TypeError("update_info must be a dictionary")

    # Validate update keys
    invalid_keys = set(update_info) - PERMITTED_FIELDS
    if invalid_keys:
        raise ValueError(f"Attempted to update disallowed fields: {sorted(invalid_keys)}")

    # Create a copy so we don't mutate the original
    updated_product = copy.deepcopy(product_details)

    # Apply updates
    for key, value in update_info.items():
        updated_product[key] = value

    return updated_product