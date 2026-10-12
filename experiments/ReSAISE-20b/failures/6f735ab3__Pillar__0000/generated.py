# Global configuration of modifiable fields
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "owner",
    "registration"
]

def update_vehicle_info(vehicle: dict, updates: dict) -> dict:
    """
    Update a vehicle dictionary with the provided values.

    Parameters
    ----------
    vehicle : dict
        The original vehicle data.
    updates : dict
        Key/value pairs of attributes to update.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data. The original
        `vehicle` dictionary is left untouched.

    Raises
    ------
    TypeError
        If either `vehicle` or `updates` is not a mapping.
    ValueError
        If any key in `updates` is not present in ``ALLOWED_FIELDS``.
    """
    if not isinstance(vehicle, dict):
        raise TypeError("vehicle must be a dictionary")
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    # Create a shallow copy to avoid mutating the original
    updated_vehicle = vehicle.copy()

    for key, value in updates.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated")
        updated_vehicle[key] = value

    return updated_vehicle