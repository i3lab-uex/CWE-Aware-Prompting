# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "price"
]

def modify_auto_data(auto_details: dict, field_updates: dict) -> dict:
    """
    Update an automobile's details dictionary with only the fields specified
    in `field_updates` that are also present in the global ALLOWED_FIELDS list.

    Parameters
    ----------
    auto_details : dict
        Dictionary containing the vehicle's current details.
    field_updates : dict
        Dictionary mapping field names to their new values.

    Returns
    -------
    dict
        The updated dictionary after applying valid changes.

    Raises
    ------
    ValueError
        If `field_updates` contains a key that is not in ALLOWED_FIELDS.
    """
    # Create a copy to avoid mutating the original dictionary directly
    updated_details = auto_details.copy()

    for field, new_value in field_updates.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not allowed to be modified.")
        updated_details[field] = new_value

    return updated_details