import copy
from typing import Dict, Any

# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "price",
    "engine_type",
    "transmission",
]

def modify_auto_data(auto_details: Dict[str, Any], field_updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new dictionary with the specified fields updated.

    Parameters
    ----------
    auto_details : dict
        The original vehicle details.
    field_updates : dict
        A dictionary of fields to update with their new values.

    Returns
    -------
    dict
        A copy of `auto_details` with the allowed updates applied.

    Raises
    ------
    KeyError
        If any key in `field_updates` is not present in `ALLOWED_FIELDS`.
    TypeError
        If the input arguments are not dictionaries.
    """
    if not isinstance(auto_details, dict):
        raise TypeError("auto_details must be a dictionary")
    if not isinstance(field_updates, dict):
        raise TypeError("field_updates must be a dictionary")

    # Create a shallow copy so we don't mutate the original
    updated_details = copy.deepcopy(auto_details)

    for key, value in field_updates.items():
        if key not in ALLOWED_FIELDS:
            raise KeyError(f"Field '{key}' is not allowed to be updated.")
        # Basic type validation could be added here if needed
        updated_details[key] = value

    return updated_details