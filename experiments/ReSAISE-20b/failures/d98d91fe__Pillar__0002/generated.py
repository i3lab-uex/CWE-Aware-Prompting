# Global list of attributes that are allowed to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "mileage",
    "vin",          # Vehicle Identification Number
    "engine_type",
    "transmission",
]

def modify_car_details(car: dict, changes: dict) -> dict:
    """
    Return a new dictionary with the specified updates applied to *car*.

    Parameters
    ----------
    car : dict
        The original vehicle dictionary.  It may contain arbitrary keys.
    changes : dict
        Mapping of attribute names to new values that should be applied.

    Returns
    -------
    dict
        A copy of *car* with the permitted changes applied.

    Raises
    ------
    ValueError
        If *changes* contains a key that is not in :data:`ALLOWED_FIELDS`.
    TypeError
        If *car* or *changes* is not a mapping.
    """
    # Basic type checks
    if not isinstance(car, dict):
        raise TypeError(f"Expected 'car' to be a dict, got {type(car).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"Expected 'changes' to be a dict, got {type(changes).__name__}")

    # Validate that all requested changes are allowed
    for key in changes:
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Attempt to modify disallowed field '{key}'")

    # Create a shallow copy to avoid mutating the caller's dictionary
    updated_car = car.copy()

    # Apply the changes
    for key, value in changes.items():
        updated_car[key] = value

    return updated_car