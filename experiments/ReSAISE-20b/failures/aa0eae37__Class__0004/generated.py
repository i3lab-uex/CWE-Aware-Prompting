# modify_auto_data.py

from copy import deepcopy
from typing import Dict, Any

# Global list of fields that are allowed to be updated.
ALLOWED_FIELDS = ["make", "model", "year", "color", "vin", "engine"]

def modify_auto_data(auto_details: Dict[str, Any],
                     field_updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an auto_details dictionary with values from field_updates only for
    keys that are present in the global ALLOWED_FIELDS list.

    Parameters
    ----------
    auto_details : dict
        Dictionary containing the current vehicle details.
    field_updates : dict
        Dictionary of fields to update with their new values.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle details. The original
        `auto_details` is not modified.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If any key in `field_updates` is not in ALLOWED_FIELDS.
    """
    if not isinstance(auto_details, dict):
        raise TypeError("auto_details must be a dictionary")
    if not isinstance(field_updates, dict):
        raise TypeError("field_updates must be a dictionary")

    # Create a shallow copy to avoid mutating the original dict
    updated_details = deepcopy(auto_details)

    for key, value in field_updates.items():
        if not isinstance(key, str):
            raise ValueError(f"Field name must be a string, got {type(key).__name__}")
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")
        # Update the value; no further validation of `value` type is performed
        updated_details[key] = value

    return updated_details