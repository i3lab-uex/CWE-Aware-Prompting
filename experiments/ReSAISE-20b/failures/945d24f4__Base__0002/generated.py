# Global list of fields that are permitted to be updated.
ALLOWED_FIELDS = {"make", "model", "year", "color", "vin"}

def update_car_information(car_details: dict, changes: dict) -> dict:
    """
    Update a vehicle's details with the provided changes.

    Parameters
    ----------
    car_details : dict
        The original dictionary containing vehicle properties.
    changes : dict
        Dictionary of fields to update with their new values.

    Returns
    -------
    dict
        A new dictionary reflecting the updated vehicle details.

    Raises
    ------
    ValueError
        If any key in ``changes`` is not listed in ``ALLOWED_FIELDS``.
    TypeError
        If ``car_details`` or ``changes`` is not a dictionary.

    Notes
    -----
    This function performs a shallow copy of ``car_details`` before applying updates,
    ensuring that the original dictionary remains unchanged. Only fields explicitly
    allowed in ``ALLOWED_FIELDS`` may be modified; attempting to update any other field
    will raise a :class:`ValueError`. This protects against CWE‑915: Improperly
    Controlled Modification of Dynamically-Determined Object Attributes.
    """
    if not isinstance(car_details, dict):
        raise TypeError("car_details must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Create a copy to avoid mutating the original dict
    updated = car_details.copy()

    for field, new_value in changes.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not allowed to be updated")
        updated[field] = new_value

    return updated