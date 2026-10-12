# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "mileage",
    "vin",
    "engine_type",
    "transmission",
    "fuel_type",
    "price"
]

def adjust_vehicle_info(auto: dict, modifications: dict) -> dict:
    """
    Update an automobile dictionary with new values for allowed fields.

    Parameters
    ----------
    auto : dict
        Dictionary containing vehicle attributes.
    modifications : dict
        Mapping of attribute names to new values.

    Returns
    -------
    dict
        The same dictionary instance updated with the permitted changes.

    Raises
    ------
    ValueError
        If any key in ``modifications`` is not present in :data:`ALLOWED_FIELDS`.
    TypeError
        If ``auto`` or ``modifications`` is not a dictionary.
    """
    if not isinstance(auto, dict):
        raise TypeError(f"'auto' must be a dict, got {type(auto).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(f"'modifications' must be a dict, got {type(modifications).__name__}")

    # Validate that all requested modifications are permitted
    unauthorized = set(modifications) - set(ALLOWED_FIELDS)
    if unauthorized:
        raise ValueError(f"Attempted to modify disallowed fields: {', '.join(sorted(unauthorized))}")

    # Apply the allowed modifications
    for key, value in modifications.items():
        auto[key] = value

    return auto