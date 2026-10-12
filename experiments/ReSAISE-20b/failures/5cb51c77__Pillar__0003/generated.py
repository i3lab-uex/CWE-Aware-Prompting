# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS = {"make", "model", "year", "color", "vin"}

def modify_vehicle_data(vehicle_info: dict, changes_to_apply: dict) -> dict:
    """
    Update vehicle information with the given changes, but only for fields that are
    explicitly allowed. The original dictionary is not modified; a new dictionary
    containing the updated data is returned.

    Parameters
    ----------
    vehicle_info : dict
        The original vehicle details.
    changes_to_apply : dict
        Mapping of field names to new values that should be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle information.

    Raises
    ------
    ValueError
        If `changes_to_apply` contains a key that is not in ALLOWED_FIELDS.
    """
    # Create a shallow copy to avoid mutating the caller's dictionary
    updated_info = vehicle_info.copy()

    for field, new_value in changes_to_apply.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not allowed to be modified.")
        updated_info[field] = new_value

    return updated_info