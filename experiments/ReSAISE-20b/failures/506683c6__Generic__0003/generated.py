# Define the list of fields that are permitted to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    # Add more fields here as needed
]


def modify_car_attributes(car: dict, updates: dict) -> dict:
    """
    Update a car dictionary with new values for allowed fields.

    Parameters
    ----------
    car : dict
        The current state of the vehicle's attributes.
    updates : dict
        Dictionary containing field names and their new values.

    Returns
    -------
    dict
        A new dictionary representing the updated vehicle.

    Raises
    ------
    TypeError
        If either `car` or `updates` is not a dictionary.
    ValueError
        If any key in `updates` is not present in ALLOWED_FIELDS.
    """
    # Basic type checking
    if not isinstance(car, dict):
        raise TypeError(f"'car' must be a dict, got {type(car).__name__}")
    if not isinstance(updates, dict):
        raise TypeError(f"'updates' must be a dict, got {type(updates).__name__}")

    # Validate that all requested updates are allowed
    for key in updates:
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be modified")

    # Create a shallow copy of the original car dict and apply updates
    updated_car = car.copy()
    updated_car.update(updates)

    return updated_car