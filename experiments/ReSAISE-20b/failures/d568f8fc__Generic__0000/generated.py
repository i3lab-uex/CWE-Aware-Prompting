# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def adjust_product_data(prod_info: dict, change_vals: dict) -> dict:
    """
    Update a product dictionary with new values for allowed fields.

    Parameters
    ----------
    prod_info : dict
        The original product data.
    change_vals : dict
        Mapping of field names to new values that should be applied.

    Returns
    -------
    dict
        The updated product dictionary (the same object as `prod_info`).

    Raises
    ------
    ValueError
        If an attempt is made to modify a field that is not in `PERMITTED_FIELDS`.
    """
    if not isinstance(prod_info, dict):
        raise TypeError("prod_info must be a dictionary")
    if not isinstance(change_vals, dict):
        raise TypeError("change_vals must be a dictionary")

    for key, value in change_vals.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted to be updated.")
        prod_info[key] = value

    return prod_info