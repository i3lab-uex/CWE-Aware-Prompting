# adjust_vehicle_info.py

from typing import Dict, Any

# List of attributes that are allowed to be modified
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "engine_type",
    "transmission",
]

def adjust_vehicle_info(auto: Dict[str, Any], modifications: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update only permitted attributes of a vehicle dictionary.

    Parameters
    ----------
    auto : dict
        The original vehicle data.
    modifications : dict
        Keys and new values for fields that should be updated.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.
    
    Raises
    ------
    ValueError
        If `auto` or `modifications` is not a dictionary.
    KeyError
        If any key in `modifications` is not in ALLOWED_FIELDS.
    """
    if not isinstance(auto, dict):
        raise ValueError("`auto` must be a dictionary")
    if not isinstance(modifications, dict):
        raise ValueError("`modifications` must be a dictionary")

    # Create a shallow copy to avoid mutating the original
    updated_auto = auto.copy()

    for key, value in modifications.items():
        if key not in ALLOWED_FIELDS:
            raise KeyError(f"Field '{key}' is not allowed to be modified.")
        updated_auto[key] = value

    return updated_auto