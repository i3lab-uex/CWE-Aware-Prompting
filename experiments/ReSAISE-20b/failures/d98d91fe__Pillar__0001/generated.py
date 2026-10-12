# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "mileage",
    "price",
]

def modify_car_details(car: dict, changes: dict) -> dict:
    """
    Update a car dictionary with allowed fields.

    Parameters
    ----------
    car : dict
        The original vehicle dictionary.
    changes : dict
        Dictionary of attributes to update.

    Returns
    -------
    dict
        The updated car dictionary.

    Raises
    ------
    KeyError
        If a key in `changes` does not exist in the original car dictionary.
    ValueError
        If a key in `changes` is not part of ALLOWED_FIELDS.
    TypeError
        If either argument is not a dictionary.
    """
    if not isinstance(car, dict):
        raise TypeError("`car` must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary")

    # Verify all keys exist in the original car and are allowed to change
    for key, value in changes.items():
        if key not in car:
            raise KeyError(f"Field '{key}' does not exist in the vehicle record")
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for modification")

    # Perform the update
    car.update(changes)

    return car