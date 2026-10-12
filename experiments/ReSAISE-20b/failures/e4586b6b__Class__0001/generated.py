# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "transmission",
]

def update_vehicle_attributes(automobile: dict, changes: dict) -> dict:
    """
    Update specific fields of a vehicle's attributes.

    Parameters
    ----------
    automobile : dict
        The current state of the vehicle's attributes.
    changes : dict
        A dictionary containing fields to be updated and their new values.

    Returns
    -------
    dict
        The vehicle dictionary after applying valid modifications.

    Raises
    ------
    ValueError
        If any key in ``changes`` is not present in :data:`ALLOWED_FIELDS`.
    """
    if not isinstance(automobile, dict):
        raise TypeError("`automobile` must be a dictionary.")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary.")

    for key, value in changes.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")
        automobile[key] = value

    return automobile