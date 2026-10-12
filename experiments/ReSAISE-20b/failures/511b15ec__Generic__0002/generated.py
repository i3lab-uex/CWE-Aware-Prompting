# Define the fields that are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def update_product_info(prod: dict, change_data: dict) -> dict:
    """
    Update the product dictionary with new values provided in `change_data`.
    
    Only fields listed in PERMITTED_FIELDS are allowed to be modified.
    
    Parameters
    ----------
    prod : dict
        The original product dictionary. It may contain arbitrary keys.
    change_data : dict
        Dictionary of fields to update. Keys must be in PERMITTED_FIELDS.
    
    Returns
    -------
    dict
        The updated product dictionary. (The same object as `prod`.)
    
    Raises
    ------
    ValueError
        If any key in `change_data` is not permitted to be updated.
    """
    # Defensive copy? We modify in place and return the same dict.
    for key, value in change_data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")
        prod[key] = value
    return prod