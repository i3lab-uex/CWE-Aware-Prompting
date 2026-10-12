# Global list of fields that are allowed to be modified.
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

def modify_vehicle_data(vehicle_info: dict, modifications: dict) -> dict:
    """
    Update the vehicle_info dictionary with values from modifications
    only for attributes listed in ALLOWED_FIELDS.

    Parameters
    ----------
    vehicle_info : dict
        Dictionary containing the current state of a vehicle.
    modifications : dict
        Dictionary mapping attribute names to new values.

    Returns
    -------
    dict
        The updated vehicle_info dictionary.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If modifications contains keys that are not in ALLOWED_FIELDS.

    Notes
    -----
    This function performs strict validation to mitigate CWE-915
    (Improperly Controlled Modification of Dynamically-Determined Object Attributes).
    """
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")

    # Filter modifications to only allowed fields
    for key, value in modifications.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Modification of field '{key}' is not permitted")
        vehicle_info[key] = value

    return vehicle_info