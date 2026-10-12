# update_item_details.py

from typing import Dict, Any

# Define which fields can be updated
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def update_item_details(inventory: Dict[str, Any],
                        update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update permitted fields of a product inventory entry.

    Parameters
    ----------
    inventory : dict
        The original product dictionary.
    update_data : dict
        A mapping of field names to new values.

    Returns
    -------
    dict
        The updated product dictionary.  The original dictionary is modified in place.

    Notes
    -----
    Only keys listed in the global PERMITTED_FIELDS set are updated.
    Invalid keys are ignored; no exception is raised.  This keeps the
    function safe for use with untrusted input.
    """
    if not isinstance(inventory, dict):
        raise TypeError("inventory must be a dictionary")
    if not isinstance(update_data, dict):
        raise TypeError("update_data must be a dictionary")

    for key, value in update_data.items():
        if key in PERMITTED_FIELDS:
            inventory[key] = value
    return inventory