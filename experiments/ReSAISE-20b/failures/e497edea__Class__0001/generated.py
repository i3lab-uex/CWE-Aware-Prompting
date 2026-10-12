# Global list of fields that are allowed to be updated.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    # add other permitted fields here
]

def adjust_vehicle_info(auto: dict, modifications: dict) -> dict:
    """
    Update the vehicle dictionary `auto` with values from `modifications`
    only for fields that are listed in the global ALLOWED_FIELDS.

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
    KeyError
        If `modifications` contains a key that is not in ALLOWED_FIELDS.
    TypeError
        If `auto` or `modifications` is not a dictionary.

    Notes
    -----
    This function performs no type validation on the values; it simply assigns
    them.  The caller is responsible for ensuring that the new values are of
    appropriate type and within acceptable ranges.
    """
    if not isinstance(auto, dict):
        raise TypeError("`auto` must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("`modifications` must be a dictionary")

    # Create a copy to avoid mutating the original if caller expects immutability.
    updated_auto = auto.copy()

    for key, value in modifications.items():
        if key not in ALLOWED_FIELDS:
            raise KeyError(f"Field '{key}' is not allowed to be updated")
        updated_auto[key] = value

    return updated_auto