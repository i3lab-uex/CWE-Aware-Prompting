import copy
from typing import Dict, Any

# Global list of fields that are allowed to be updated.
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

def update_car_information(car_details: Dict[str, Any], changes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update specified fields of a vehicle's details.

    Parameters
    ----------
    car_details : dict
        The original dictionary containing the vehicle's details.
    changes : dict
        A dictionary with keys representing fields to update and their new values.

    Returns
    -------
    dict
        A new dictionary reflecting the updates applied to allowed fields.
    
    Raises
    ------
    ValueError
        If any key in ``changes`` is not present in :data:`ALLOWED_FIELDS`.
    """
    # Work on a shallow copy to avoid mutating the original dictionary
    updated = copy.deepcopy(car_details)

    for field, new_value in changes.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not allowed to be updated.")
        # No dynamic code execution; we simply assign the new value.
        updated[field] = new_value

    return updated