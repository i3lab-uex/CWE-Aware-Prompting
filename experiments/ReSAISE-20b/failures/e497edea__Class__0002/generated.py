# Global list of fields that can be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "owner_name",
    "mileage",
]

def adjust_vehicle_info(auto: dict, modifications: dict) -> dict:
    """
    Update only the attributes of a vehicle dictionary that are explicitly allowed.

    Parameters
    ----------
    auto : dict
        The original vehicle dictionary.
    modifications : dict
        Dictionary containing attribute names as keys and the new values.

    Returns
    -------
    dict
        The updated vehicle dictionary.

    Raises
    ------
    ValueError
        If any key in ``modifications`` is not present in ``ALLOWED_FIELDS``.
    TypeError
        If either argument is not a dictionary.
    """
    # Basic type validation
    if not isinstance(auto, dict):
        raise TypeError("`auto` must be a dictionary.")
    if not isinstance(modifications, dict):
        raise TypeError("`modifications` must be a dictionary.")

    # Ensure only allowed fields are updated
    for key in modifications:
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update.")

    # Perform the updates in place
    auto.update(modifications)

    return auto