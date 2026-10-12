# -*- coding: utf-8 -*-

from typing import Dict, Any

# List of fields that are permitted to be modified
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "mileage",
    "engine_type",
    "transmission",
    "vin",
]


def adjust_vehicle_info(auto: Dict[str, Any], modifications: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with the provided modifications only for allowed fields.

    Parameters
    ----------
    auto : dict
        The original vehicle dictionary.
    modifications : dict
        Dictionary of key/value pairs to update in `auto`.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.

    Raises
    ------
    ValueError
        If any key in `modifications` is not present in ``ALLOWED_FIELDS``.
    """
    if not isinstance(auto, dict):
        raise TypeError("`auto` must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("`modifications` must be a dictionary")

    # Create a shallow copy to avoid mutating the original
    updated_auto = auto.copy()

    disallowed_keys = [k for k in modifications if k not in ALLOWED_FIELDS]
    if disallowed_keys:
        raise ValueError(f"Attempted to modify disallowed fields: {', '.join(disallowed_keys)}")

    # Apply allowed modifications
    for key, value in modifications.items():
        updated_auto[key] = value

    return updated_auto