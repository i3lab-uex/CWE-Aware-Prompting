from copy import deepcopy

# Fields that are allowed to be updated.  Any attempt to modify a field
# not in this list will raise an exception.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "owner",
    "registration"
]


def update_vehicle_info(vehicle: dict, updates: dict) -> dict:
    """
    Return a new dictionary representing the vehicle with updated attributes.

    Parameters
    ----------
    vehicle : dict
        The original vehicle data.  Keys are strings; values may be any type.
    updates : dict
        A mapping of attribute names to the new value that should be applied.

    Returns
    -------
    dict
        A copy of ``vehicle`` with the requested updates applied.

    Raises
    ------
    ValueError
        If ``updates`` contains a key that is not in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    * The function never mutates the input ``vehicle``; it returns a new
      dictionary.
    * The update is performed atomically: if any key in ``updates`` is
      disallowed, the function raises an exception and no changes are made.
    """
    # Validate that all keys in updates are allowed
    disallowed = set(updates) - set(ALLOWED_FIELDS)
    if disallowed:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(sorted(disallowed))}"
        )

    # Create a shallow copy of the vehicle to avoid side‑effects
    updated_vehicle = deepcopy(vehicle)

    # Apply each allowed update
    for key, value in updates.items():
        updated_vehicle[key] = value

    return updated_vehicle