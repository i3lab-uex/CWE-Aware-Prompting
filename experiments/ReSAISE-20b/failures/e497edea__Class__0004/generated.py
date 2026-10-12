# Global list of fields that are permitted to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "transmission",
    # Add any other fields that should be modifiable here.
]

def adjust_vehicle_info(auto: dict, modifications: dict) -> dict:
    """
    Update only the allowed attributes of a vehicle dictionary.

    Parameters
    ----------
    auto : dict
        The original vehicle dictionary.
    modifications : dict
        A mapping of attribute names to new values that should be applied.

    Returns
    -------
    dict
        The vehicle dictionary after applying the authorized modifications.

    Raises
    ------
    ValueError
        If any key in `modifications` is not present in :data:`ALLOWED_FIELDS`.
    TypeError
        If either argument is not a dictionary.
    """
    if not isinstance(auto, dict):
        raise TypeError(f"'auto' must be a dict, got {type(auto).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(f"'modifications' must be a dict, got {type(modifications).__name__}")

    for key, value in modifications.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Modification of field '{key}' is not allowed.")
        auto[key] = value

    return auto