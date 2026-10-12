# Define the list of fields that are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def adjust_product_data(prod_info: dict, change_vals: dict) -> dict:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    prod_info : dict
        The original product data.
    change_vals : dict
        Dictionary containing fields to update with their new values.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.

    Raises
    ------
    ValueError
        If ``change_vals`` contains keys that are not in PERMITTED_FIELDS.
    """
    # Validate that all requested changes are permitted
    invalid_keys = set(change_vals) - PERMITTED_FIELDS
    if invalid_keys:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(sorted(invalid_keys))}"
        )

    # Create a shallow copy to avoid mutating the original dictionary
    updated_prod = prod_info.copy()

    # Apply permitted changes
    for key, value in change_vals.items():
        updated_prod[key] = value

    return updated_prod