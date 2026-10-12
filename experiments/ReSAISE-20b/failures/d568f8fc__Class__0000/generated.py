# Define the list of fields that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def adjust_product_data(prod_info: dict, change_vals: dict) -> dict:
    """
    Update only the fields specified in PERMITTED_FIELDS.

    Parameters
    ----------
    prod_info : dict
        The original product dictionary.  Keys are the product attributes.
    change_vals : dict
        A mapping of field names to new values that should be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.

    Raises
    ------
    ValueError
        If any key in ``change_vals`` is not in PERMITTED_FIELDS.
    TypeError
        If ``prod_info`` or ``change_vals`` is not a dictionary.

    Notes
    -----
    The function performs a shallow copy of ``prod_info`` to avoid mutating the
    caller's dictionary.  It only updates keys that are explicitly allowed,
    preventing accidental or malicious modification of sensitive fields.
    """
    if not isinstance(prod_info, dict):
        raise TypeError("prod_info must be a dictionary")
    if not isinstance(change_vals, dict):
        raise TypeError("change_vals must be a dictionary")

    # Validate that all requested changes are permitted
    invalid_keys = [k for k in change_vals if k not in PERMITTED_FIELDS]
    if invalid_keys:
        raise ValueError(
            f"The following fields are not permitted to be updated: {invalid_keys}"
        )

    # Create a copy to avoid side effects
    updated_product = prod_info.copy()

    # Apply the allowed changes
    for key, value in change_vals.items():
        updated_product[key] = value

    return updated_product