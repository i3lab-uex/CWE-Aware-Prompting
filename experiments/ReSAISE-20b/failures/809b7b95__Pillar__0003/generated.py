import copy
from typing import Dict, Any

# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def modify_item_details(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new dictionary with updates applied only to fields listed in
    PERMITTED_FIELDS. The original `item` is left untouched.

    Parameters
    ----------
    item : dict
        The original product dictionary.
    details : dict
        Dictionary of key/value pairs to apply as updates.

    Returns
    -------
    dict
        A new dictionary containing the merged values.
    """
    # Defensive copy to avoid mutating the original item
    updated_item = copy.deepcopy(item)

    for key, value in details.items():
        if key not in PERMITTED_FIELDS:
            # Skip fields that are not permitted to be modified
            continue

        # If the value is a mutable type, copy it to prevent accidental sharing.
        if isinstance(value, (dict, list)):
            value = copy.deepcopy(value)

        updated_item[key] = value

    return updated_item