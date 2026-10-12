# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "mileage",
    "engine_type",
    "vin",
]

def adjust_vehicle_info(auto: dict, modifications: dict) -> dict:
    """
    Update an automobile dictionary with a set of authorized changes.

    Parameters
    ----------
    auto : dict
        Dictionary representing the vehicle. It is updated in place and also returned.
    modifications : dict
        Mapping of attribute names to new values that should be applied.

    Returns
    -------
    dict
        The updated vehicle dictionary.

    Raises
    ------
    ValueError
        If any key in `modifications` is not listed in ALLOWED_FIELDS.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    * The function performs a shallow copy of the modifications to avoid accidental
      modification of nested objects from outside.
    * It does not attempt to enforce type correctness for the values; that is left
      to higher-level validation logic.
    """
    if not isinstance(auto, dict):
        raise TypeError("`auto` must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("`modifications` must be a dictionary")

    # Create a copy of the modifications to prevent external side effects.
    mods_copy = dict(modifications)

    for key, value in mods_copy.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Attempt to modify forbidden field '{key}'")

        # Update the vehicle dictionary.
        auto[key] = value

    return auto