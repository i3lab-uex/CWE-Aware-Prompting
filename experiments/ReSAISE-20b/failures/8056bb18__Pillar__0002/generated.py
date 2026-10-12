# Global list of fields that are permitted to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "price",
    "owner_id",
]

def modify_vehicle_data(vehicle_info: dict, modifications: dict) -> dict:
    """
    Update a vehicle dictionary with only the allowed fields.

    Parameters
    ----------
    vehicle_info : dict
        Dictionary representing the vehicle. It will be updated in place.
    modifications : dict
        Mapping of field names to new values.

    Returns
    -------
    dict
        The updated vehicle dictionary.

    Raises
    ------
    TypeError
        If either argument is not a dict.
    ValueError
        If `modifications` contains keys that are not in ALLOWED_FIELDS.
    """
    # Basic type checks
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")

    # Ensure only allowed fields are modified
    disallowed = set(modifications) - set(ALLOWED_FIELDS)
    if disallowed:
        raise ValueError(f"Attempted to modify disallowed fields: {sorted(disallowed)}")

    # Perform the updates
    for key, value in modifications.items():
        vehicle_info[key] = value

    return vehicle_info