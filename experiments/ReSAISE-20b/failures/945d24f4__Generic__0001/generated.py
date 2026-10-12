# Global list of fields that are allowed to be updated.
ALLOWED_FIELDS = ['make', 'model', 'year', 'color', 'vin']

def update_car_information(car_details: dict, changes: dict) -> dict:
    """
    Update the specified fields of a car's details dictionary.

    Parameters
    ----------
    car_details : dict
        The original dictionary containing the vehicle's details.
    changes : dict
        A mapping of field names to new values that should be applied.

    Returns
    -------
    dict
        The dictionary after applying the allowed updates. The original
        `car_details` dictionary is modified in place and returned.

    Raises
    ------
    ValueError
        If any key in `changes` is not present in the global
        `ALLOWED_FIELDS` list.
    """
    # Validate that all requested changes are permitted.
    invalid_fields = [k for k in changes if k not in ALLOWED_FIELDS]
    if invalid_fields:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(invalid_fields)}"
        )

    # Apply the changes.
    car_details.update(changes)
    return car_details