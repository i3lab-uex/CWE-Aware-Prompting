# Define the list of fields that are allowed to be edited.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def edit_product_info(item: dict, details: dict) -> dict:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    item : dict
        The original product dictionary. Must contain keys that are in
        PERMITTED_FIELDS.
    details : dict
        Dictionary containing the fields and values to be updated.

    Returns
    -------
    dict
        A new dictionary with the updates applied. The original `item`
        is not modified.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    KeyError
        If `details` contains a key that is not in PERMITTED_FIELDS.

    Notes
    -----
    Only keys listed in `PERMITTED_FIELDS` may be updated. Any other
    keys in `details` will raise a KeyError to prevent accidental
    modification of protected fields.
    """
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary")
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary")

    # Create a copy so the original dict remains unchanged
    updated = item.copy()

    for key, value in details.items():
        if key not in PERMITTED_FIELDS:
            raise KeyError(f"Field '{key}' is not permitted for update")
        updated[key] = value

    return updated