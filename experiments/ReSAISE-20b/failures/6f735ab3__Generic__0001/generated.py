# Global list of attributes that are allowed to be updated.
ALLOWED_FIELDS = ["make", "model", "year", "owner", "registration"]

def update_vehicle_info(vehicle: dict, updates: dict) -> dict:
    """
    Update a vehicle dictionary with new attribute values.

    Parameters
    ----------
    vehicle : dict
        The original vehicle data.
    updates : dict
        A mapping of attribute names to new values.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.

    Raises
    ------
    TypeError
        If either `vehicle` or `updates` is not a dictionary.
    KeyError
        If an update key is not in :data:`ALLOWED_FIELDS`.
    """
    if not isinstance(vehicle, dict):
        raise TypeError("vehicle must be a dictionary")
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    # Create a shallow copy so the original vehicle is not mutated.
    updated_vehicle = vehicle.copy()

    for key, value in updates.items():
        if key not in ALLOWED_FIELDS:
            raise KeyError(f"Field '{key}' is not allowed to be updated.")
        # Basic type checks could be added here if needed.
        updated_vehicle[key] = value

    return updated_vehicle