from typing import Dict, Any

# Global list of fields that are allowed to be updated.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
]

def alter_vehicle_info(details: Dict[str, Any], modifications: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the vehicle information in ``details`` with the values provided
    in ``modifications``. Only keys that are present in the global
    ``ALLOWED_FIELDS`` list may be updated.

    Parameters
    ----------
    details : dict
        The current state of the vehicle attributes.
    modifications : dict
        Dictionary containing field names and their new values.

    Returns
    -------
    dict
        A new dictionary that contains the updated vehicle information.
        The original ``details`` dictionary is not modified.

    Raises
    ------
    ValueError
        If any key in ``modifications`` is not listed in ``ALLOWED_FIELDS``.
    """
    # Create a shallow copy to avoid mutating the original input
    updated = details.copy()

    # Validate modification keys
    for key in modifications:
        if key not in ALLOWED_FIELDS:
            raise ValueError(
                f"Field '{key}' is not allowed to be modified. "
                f"Allowed fields: {ALLOWED_FIELDS}"
            )
        # Apply the modification
        updated[key] = modifications[key]

    return updated