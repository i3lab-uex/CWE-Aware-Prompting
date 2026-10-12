# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def edit_product_info(item: dict, details: dict) -> dict:
    """
    Update the product dictionary `item` with values from `details`
    but only for keys listed in PERMITTED_FIELDS.

    Parameters
    ----------
    item : dict
        The original product dictionary. It will be modified in place.
    details : dict
        A dictionary containing potential updates.

    Returns
    -------
    dict
        The updated product dictionary.
    """
    # Validate input types early to avoid accidental mutation of non-dicts
    if not isinstance(item, dict):
        raise TypeError("item must be a dictionary")
    if not isinstance(details, dict):
        raise TypeError("details must be a dictionary")

    # Iterate over the provided details and apply only permitted fields
    for key, value in details.items():
        if key in PERMITTED_FIELDS:
            item[key] = value

    return item