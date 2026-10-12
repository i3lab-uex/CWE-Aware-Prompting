# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS = [
    'make',
    'model',
    'year',
    'color',
    'vin',
    'mileage',
    'price',
]

def modify_car_details(car: dict, changes: dict) -> dict:
    """
    Update the given `car` dictionary with values from `changes`, but only for
    attributes listed in ALLOWED_FIELDS.

    Parameters:
        car (dict): The original vehicle dictionary.
        changes (dict): Mapping of field names to new values.

    Returns:
        dict: The updated vehicle dictionary.

    Raises:
        ValueError: If `changes` contains a key not in ALLOWED_FIELDS.
    """
    if not isinstance(car, dict):
        raise TypeError("car must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Validate that all requested changes are permitted.
    invalid_fields = [field for field in changes if field not in ALLOWED_FIELDS]
    if invalid_fields:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(invalid_fields)}"
        )

    # Apply the changes.
    car.update(changes)
    return car