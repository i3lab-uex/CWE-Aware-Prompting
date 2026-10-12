# Global list of fields that are permitted to be altered.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage"
]

def alter_vehicle_info(details: dict, modifications: dict) -> dict:
    """
    Update a vehicle's attributes only for keys specified in ALLOWED_FIELDS.

    Parameters
    ----------
    details : dict
        The current vehicle attributes.
    modifications : dict
        Dictionary containing keys and new values to update.

    Returns
    -------
    dict
        The updated vehicle dictionary.

    Raises
    ------
    TypeError
        If either `details` or `modifications` is not a dictionary.
    ValueError
        If `modifications` contains keys that are not in ALLOWED_FIELDS.
    """
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("`modifications` must be a dictionary")

    # Validate that all modification keys are allowed
    for key in modifications:
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be modified")

    # Perform the updates
    for key, value in modifications.items():
        details[key] = value

    return details