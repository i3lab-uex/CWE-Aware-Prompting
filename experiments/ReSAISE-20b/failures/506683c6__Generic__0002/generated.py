# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "price",
]

def modify_car_attributes(car: dict, updates: dict) -> dict:
    """
    Update the attributes of a car dictionary with values from `updates`.

    Parameters
    ----------
    car : dict
        Current state of the vehicle's attributes.
    updates : dict
        Fields and new values to apply.

    Returns
    -------
    dict
        The updated car dictionary.

    Raises
    ------
    ValueError
        If an attempt is made to modify a field that is not in ALLOWED_FIELDS.
    """
    for key, value in updates.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be modified.")
        car[key] = value
    return car