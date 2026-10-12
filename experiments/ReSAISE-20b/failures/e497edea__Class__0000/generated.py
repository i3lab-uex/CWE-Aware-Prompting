# Global list of fields that are allowed to be updated.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "transmission",
    "mileage",
]

def adjust_vehicle_info(auto: dict, modifications: dict) -> dict:
    """
    Update only the allowed attributes of a vehicle dictionary.

    Parameters
    ----------
    auto : dict
        Dictionary representing the vehicle.  The function mutates this dictionary.
    modifications : dict
        Mapping of attribute names to new values.  Only keys present in
        ``ALLOWED_FIELDS`` will be applied.

    Returns
    -------
    dict
        The same dictionary object passed in as ``auto``, now updated.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If ``modifications`` contains keys that are not permitted.
    """
    if not isinstance(auto, dict):
        raise TypeError("`auto` must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("`modifications` must be a dictionary")

    # Validate that all requested modifications are allowed
    disallowed = [k for k in modifications if k not in ALLOWED_FIELDS]
    if disallowed:
        raise ValueError(
            f"Attempted to modify forbidden fields: {', '.join(disallowed)}"
        )

    # Apply the allowed modifications
    for key, value in modifications.items():
        auto[key] = value

    return auto