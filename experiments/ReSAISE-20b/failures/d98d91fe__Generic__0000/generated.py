# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "owner_name",
    "mileage",
]

def modify_car_details(car: dict, changes: dict) -> dict:
    """
    Update a vehicle dictionary with the provided changes.

    Parameters
    ----------
    car : dict
        Dictionary representing a vehicle.
    changes : dict
        Mapping of attribute names to new values.

    Returns
    -------
    dict
        The updated vehicle dictionary.

    Raises
    ------
    ValueError
        If a change references a field that is not in ALLOWED_FIELDS.
    TypeError
        If `car` or `changes` are not dictionaries.
    """
    # Basic type checks
    if not isinstance(car, dict):
        raise TypeError("`car` must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary")

    for field, new_value in changes.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not allowed to be modified.")
        # Perform the update
        car[field] = new_value

    return car