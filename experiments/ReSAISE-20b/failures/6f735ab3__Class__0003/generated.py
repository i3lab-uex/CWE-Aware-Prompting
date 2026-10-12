# update_vehicle_info.py

from typing import Dict, Any, List

# Global list of fields that are allowed to be updated
ALLOWED_FIELDS: List[str] = [
    "make",
    "model",
    "year",
    "owner",
    "registration"
]

def update_vehicle_info(vehicle: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update vehicle attributes based on the provided updates dictionary.

    Parameters
    ----------
    vehicle : dict
        Dictionary representing a vehicle object.
    updates : dict
        Dictionary containing attributes to update and their new values.

    Returns
    -------
    dict
        A new dictionary with the updated vehicle attributes.

    Raises
    ------
    ValueError
        If any key in `updates` is not present in ALLOWED_FIELDS.
    """
    # Ensure we do not modify the original vehicle dictionary
    updated_vehicle = vehicle.copy()

    for key, value in updates.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")
        # Simple type checks can be added here if needed
        updated_vehicle[key] = value

    return updated_vehicle