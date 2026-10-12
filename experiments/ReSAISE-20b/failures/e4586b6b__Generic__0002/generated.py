# Global list of fields that are permitted to be updated.
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

def update_vehicle_attributes(automobile: dict, changes: dict) -> dict:
    """
    Update specific attributes of a vehicle dictionary.

    Parameters
    ----------
    automobile : dict
        The current state of the vehicle attributes.
    changes : dict
        Keys and new values to be applied.

    Returns
    -------
    dict
        The updated vehicle dictionary.

    Raises
    ------
    ValueError
        If any key in `changes` is not in ALLOWED_FIELDS.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    The function modifies the original `automobile` dict in place.
    """
    # Validate input types
    if not isinstance(automobile, dict):
        raise TypeError("`automobile` must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary")

    # Check that all requested changes are allowed
    disallowed = [k for k in changes if k not in ALLOWED_FIELDS]
    if disallowed:
        raise ValueError(
            f"The following fields are not allowed to be updated: {', '.join(disallowed)}"
        )

    # Apply the changes
    automobile.update(changes)
    return automobile