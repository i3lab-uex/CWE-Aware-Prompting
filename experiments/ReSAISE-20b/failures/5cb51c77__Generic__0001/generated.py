from typing import Dict, Any

# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS = ["make", "model", "year", "color", "vin"]

def modify_vehicle_data(
    vehicle_info: Dict[str, Any],
    changes_to_apply: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update vehicle information only for fields listed in ALLOWED_FIELDS.

    Parameters
    ----------
    vehicle_info : dict
        The original dictionary containing the vehicle's details.
    changes_to_apply : dict
        A mapping of field names to new values that should be applied.

    Returns
    -------
    dict
        A new dictionary with the allowed changes applied. The original
        `vehicle_info` remains unmodified.

    Raises
    ------
    ValueError
        If any key in `changes_to_apply` is not present in ALLOWED_FIELDS.
    """
    # Create a shallow copy to avoid mutating the input dictionary
    updated_info = vehicle_info.copy()

    for key, new_value in changes_to_apply.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be modified.")
        updated_info[key] = new_value

    return updated_info