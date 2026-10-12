from __future__ import annotations

# List of fields that are permitted to be updated.
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

def modify_car_details(car: dict, changes: dict) -> dict:
    """
    Update a vehicle dictionary with new values for allowed fields.

    Parameters
    ----------
    car : dict
        Dictionary representing a vehicle. Must contain keys that match the allowed fields.
    changes : dict
        Mapping of field names to new values. Only keys present in ALLOWED_FIELDS are applied.

    Returns
    -------
    dict
        The updated vehicle dictionary. The input dictionary is modified in place.

    Raises
    ------
    ValueError
        If any key in ``changes`` is not listed in :data:`ALLOWED_FIELDS`.
    TypeError
        If either ``car`` or ``changes`` is not a dictionary.
    """
    if not isinstance(car, dict):
        raise TypeError(f"'car' must be a dict, got {type(car).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"'changes' must be a dict, got {type(changes).__name__}")

    for field, new_value in changes.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not allowed to be modified.")
        car[field] = new_value

    return car