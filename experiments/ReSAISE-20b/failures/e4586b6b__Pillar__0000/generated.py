import copy

# Global list of fields that are allowed to be updated.
ALLOWED_FIELDS = {"make", "model", "year", "color", "vin"}

def update_vehicle_attributes(automobile: dict, changes: dict) -> dict:
    """
    Update an automobile's attributes with the provided changes.

    Parameters
    ----------
    automobile : dict
        Current state of vehicle attributes.
    changes : dict
        Fields and new values to apply.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle attributes.

    Raises
    ------
    ValueError
        If `changes` contains a key that is not in ALLOWED_FIELDS.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    * The function performs a shallow copy of the original dictionary to avoid side‑effects.
    * Only keys listed in ``ALLOWED_FIELDS`` are permitted; attempting to modify any other key
      raises an exception, preventing accidental alteration of protected fields.
    """
    if not isinstance(automobile, dict):
        raise TypeError("`automobile` must be a dictionary.")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary.")

    # Validate that all requested changes are allowed
    invalid_keys = set(changes) - ALLOWED_FIELDS
    if invalid_keys:
        raise ValueError(f"Attempted to modify disallowed fields: {sorted(invalid_keys)}")

    # Work on a copy to avoid mutating the input dictionary
    updated = copy.deepcopy(automobile)

    # Apply allowed changes
    for key, value in changes.items():
        updated[key] = value

    return updated