# Allowed fields that can be updated on a vehicle dictionary.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "mileage",
    "engine_type",
    "transmission",
    "vin",
    "owner_name",
]

def adjust_vehicle_info(auto: dict, modifications: dict) -> dict:
    """
    Update the `auto` dictionary with values from `modifications`, but only for keys
    that are listed in the global ALLOWED_FIELDS.

    Parameters
    ----------
    auto : dict
        The original vehicle dictionary.
    modifications : dict
        A mapping of field names to new values.

    Returns
    -------
    dict
        The updated vehicle dictionary.

    Raises
    ------
    TypeError
        If `auto` or `modifications` is not a dictionary.
    ValueError
        If any key in `modifications` is not present in ALLOWED_FIELDS.
    """
    if not isinstance(auto, dict):
        raise TypeError(f"'auto' must be a dict, got {type(auto).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(f"'modifications' must be a dict, got {type(modifications).__name__}")

    # Create a shallow copy to avoid mutating the original dictionary
    updated = auto.copy()

    for field, value in modifications.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not allowed to be updated.")
        updated[field] = value

    return updated