import copy

# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def modify_item_details(item: dict, details: dict) -> dict:
    """
    Update an item dictionary with values from ``details`` only for
    fields listed in the global ``PERMITTED_FIELDS``.

    Parameters
    ----------
    item : dict
        The original product dictionary.  It may contain any keys.
    details : dict
        Dictionary of desired updates.

    Returns
    -------
    dict
        A new dictionary containing the updated product state.
    """
    # Work on a shallow copy to avoid mutating the original input.
    updated_item = copy.deepcopy(item)

    for key, value in details.items():
        if key in PERMITTED_FIELDS:
            updated_item[key] = value
    return updated_item