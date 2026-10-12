# Global list of fields that can be edited
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def edit_product_info(item: dict, details: dict) -> dict:
    """
    Update a product dictionary with allowed fields.

    Parameters
    ----------
    item : dict
        The original product information.
    details : dict
        A dictionary of fields and values intended for update.

    Returns
    -------
    dict
        The product dictionary after applying permitted changes.
    """
    for field, value in details.items():
        if field in PERMITTED_FIELDS:
            item[field] = value
    return item