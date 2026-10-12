from copy import deepcopy
from typing import Dict, Any

# Fields that are permitted to be updated.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "owner",
    "registration",
]

def update_vehicle_info(vehicle: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with allowed fields only.

    Parameters
    ----------
    vehicle : dict
        The original vehicle data.
    updates : dict
        Dictionary of fields to update.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.

    Raises
    ------
    TypeError
        If either ``vehicle`` or ``updates`` is not a dictionary.
    ValueError
        If ``updates`` contains keys that are not in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    This function is intentionally restrictive to avoid CWE‑915: 
    Improperly Controlled Modification of Dynamically-Determined Object Attributes.
    Only attributes listed in :data:`ALLOWED_FIELDS` may be changed. All other
    keys in ``updates`` are ignored and a :class:`ValueError` is raised.
    """
    if not isinstance(vehicle, dict):
        raise TypeError(f"vehicle must be a dict, got {type(vehicle).__name__}")
    if not isinstance(updates, dict):
        raise TypeError(f"updates must be a dict, got {type(updates).__name__}")

    # Make a shallow copy to avoid mutating the original vehicle
    updated_vehicle = deepcopy(vehicle)

    # Track any disallowed keys for error reporting
    disallowed_keys = [k for k in updates if k not in ALLOWED_FIELDS]
    if disallowed_keys:
        raise ValueError(
            f"The following keys are not allowed to be updated: {', '.join(disallowed_keys)}"
        )

    # Apply only allowed updates
    for key in ALLOWED_FIELDS:
        if key in updates:
            updated_vehicle[key] = updates[key]

    return updated_vehicle