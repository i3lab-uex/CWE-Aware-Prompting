from __future__ import annotations

# List of attribute names that are permitted to be altered.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "transmission",
]

def alter_vehicle_info(details: dict, modifications: dict) -> dict:
    """
    Update the vehicle information dictionary with only permitted fields.

    Parameters
    ----------
    details : dict
        Current state of the vehicle attributes.
    modifications : dict
        Proposed changes. Only keys present in ALLOWED_FIELDS are applied.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.

    Raises
    ------
    ValueError
        If any key in ``modifications`` is not in ``ALLOWED_FIELDS``.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    This function performs no deep copy of nested objects; it assumes that all
    values are immutable or that callers manage mutability separately.
    """
    if not isinstance(details, dict):
        raise TypeError("details must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")

    # Validate modification keys
    invalid_keys = [k for k in modifications if k not in ALLOWED_FIELDS]
    if invalid_keys:
        raise ValueError(f"Attempted to modify disallowed fields: {invalid_keys}")

    # Create a new dictionary with updated values
    updated = details.copy()
    updated.update(modifications)
    return updated