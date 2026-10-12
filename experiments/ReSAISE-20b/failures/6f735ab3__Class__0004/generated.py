from copy import deepcopy
from typing import Dict, Any

# Global list of fields that are permitted to be updated.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "owner",
    "registration",
]

def update_vehicle_info(vehicle: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new vehicle dictionary with allowed fields updated.

    Parameters
    ----------
    vehicle : dict
        The original vehicle data.
    updates : dict
        Key/value pairs to apply to the vehicle.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.

    Raises
    ------
    ValueError
        If an attempt is made to update a field that is not in ALLOWED_FIELDS.
    """
    # Create a shallow copy so the original vehicle is untouched
    updated_vehicle = deepcopy(vehicle)

    for key, value in updates.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")
        updated_vehicle[key] = value

    return updated_vehicle