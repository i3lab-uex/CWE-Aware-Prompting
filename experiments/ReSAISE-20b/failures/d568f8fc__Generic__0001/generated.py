# Define the fields that are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def adjust_product_data(prod_info: dict, change_vals: dict) -> dict:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    prod_info : dict
        The original product data.
    change_vals : dict
        Dictionary of fields to update with their new values.

    Returns
    -------
    dict
        The updated product dictionary (the same object is modified in place).

    Raises
    ------
    TypeError
        If either `prod_info` or `change_vals` is not a dictionary.
    KeyError
        If an attempt is made to update a field that is not in PERMITTED_FIELDS.
    """
    if not isinstance(prod_info, dict):
        raise TypeError("prod_info must be a dictionary")
    if not isinstance(change_vals, dict):
        raise TypeError("change_vals must be a dictionary")

    for field, new_value in change_vals.items():
        if field not in PERMITTED_FIELDS:
            raise KeyError(f"Field '{field}' is not permitted for update.")
        prod_info[field] = new_value

    return prod_info