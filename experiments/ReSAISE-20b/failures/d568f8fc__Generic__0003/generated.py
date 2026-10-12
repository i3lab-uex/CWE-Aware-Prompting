# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def adjust_product_data(prod_info: dict, change_vals: dict) -> dict:
    """
    Update the product dictionary with new values for permitted fields.

    Parameters
    ----------
    prod_info : dict
        The original product data.
    change_vals : dict
        A dictionary containing the fields to update and their new values.

    Returns
    -------
    dict
        A new dictionary reflecting the applied changes.

    Raises
    ------
    ValueError
        If any key in ``change_vals`` is not present in :data:`PERMITTED_FIELDS`.
    """
    if not isinstance(prod_info, dict):
        raise TypeError("prod_info must be a dictionary")
    if not isinstance(change_vals, dict):
        raise TypeError("change_vals must be a dictionary")

    # Copy the original product data to avoid mutating the caller's object
    updated = prod_info.copy()

    for key, value in change_vals.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update.")
        updated[key] = value

    return updated