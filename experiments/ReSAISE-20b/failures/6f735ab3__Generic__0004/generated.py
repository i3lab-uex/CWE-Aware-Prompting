from typing import Dict, List

# Global list of fields that are allowed to be updated.
ALLOWED_FIELDS: List[str] = [
    "make",
    "model",
    "year",
    "owner",
    "registration",
]

def update_vehicle_info(vehicle: Dict[str, any], updates: Dict[str, any]) -> Dict[str, any]:
    """
    Update a vehicle dictionary with new values for allowed fields.

    Parameters
    ----------
    vehicle : dict
        The original vehicle dictionary. It will be modified in place.
    updates : dict
        Dictionary of field names to new values.

    Returns
    -------
    dict
        The updated vehicle dictionary (same object as ``vehicle``).

    Raises
    ------
    ValueError
        If any key in ``updates`` is not listed in :data:`ALLOWED_FIELDS`.
    """
    # Validate all keys are allowed
    disallowed = [k for k in updates if k not in ALLOWED_FIELDS]
    if disallowed:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(disallowed)}"
        )

    # Apply updates
    vehicle.update(updates)
    return vehicle