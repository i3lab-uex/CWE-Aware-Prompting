# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    # Add other permitted fields here
]

def modify_car_details(car: dict, changes: dict) -> dict:
    """
    Update the given `car` dictionary with values from `changes`, but only for
    attributes that are listed in the global ALLOWED_FIELDS.

    Parameters:
        car (dict): The original vehicle dictionary.
        changes (dict): Dictionary containing new values keyed by attribute names.

    Returns:
        dict: The updated car dictionary.

    Raises:
        TypeError: If `car` or `changes` is not a dictionary.
        ValueError: If any key in `changes` is not in ALLOWED_FIELDS.
    """
    if not isinstance(car, dict):
        raise TypeError(f"Expected 'car' to be a dict, got {type(car).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"Expected 'changes' to be a dict, got {type(changes).__name__}")

    # Validate each key in changes
    for field in changes:
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not allowed to be modified.")

    # Apply changes
    for field, value in changes.items():
        car[field] = value

    return car