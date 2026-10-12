# Allowed fields that can be modified on a vehicle record.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "registration_state",
    "owner_name",
]

def modify_vehicle_data(vehicle_info: dict, changes_to_apply: dict) -> dict:
    """
    Update a vehicle's information with the provided changes.

    Parameters
    ----------
    vehicle_info : dict
        Original dictionary containing vehicle details.
    changes_to_apply : dict
        Dictionary with keys to update and their new values.

    Returns
    -------
    dict
        A new dictionary reflecting the applied changes.

    Raises
    ------
    KeyError
        If a key in ``changes_to_apply`` is not listed in ``ALLOWED_FIELDS``.

    Notes
    -----
    * The function does **not** modify the original ``vehicle_info`` dictionary.
    * Only keys present in ``ALLOWED_FIELDS`` are accepted; all others raise an error.
    """
    # Create a shallow copy to avoid mutating the original dictionary
    updated_info = vehicle_info.copy()

    for key, new_value in changes_to_apply.items():
        if key not in ALLOWED_FIELDS:
            raise KeyError(
                f"Field '{key}' is not allowed to be modified. "
                f"Allowed fields: {ALLOWED_FIELDS}"
            )
        updated_info[key] = new_value

    return updated_info