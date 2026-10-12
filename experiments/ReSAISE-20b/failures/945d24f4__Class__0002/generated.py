import copy

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

def update_car_information(car_details: dict, changes: dict) -> dict:
    """
    Update only the allowed fields of a car's details.

    Parameters
    ----------
    car_details : dict
        Dictionary containing the current vehicle properties.
    changes : dict
        Dictionary with keys to be updated and their new values.

    Returns
    -------
    dict
        A new dictionary reflecting the applied updates.
    
    Raises
    ------
    TypeError
        If `car_details` or `changes` is not a dictionary.
    ValueError
        If any key in `changes` is not listed in ALLOWED_FIELDS.
    
    Notes
    -----
    This function performs a shallow copy of the input dictionary to avoid side‑effects.
    It does not perform deep validation of field values; callers should ensure data integrity
    (e.g., correct types for `year`, numeric `mileage`, etc.) before invoking this function.
    """
    if not isinstance(car_details, dict):
        raise TypeError("car_details must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Create a copy so the original dict remains unchanged
    updated = copy.deepcopy(car_details)

    for key, value in changes.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")
        # Optional: Basic type checking can be added here if needed
        updated[key] = value

    return updated