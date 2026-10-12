# -*- coding: utf-8 -*-
"""
Vehicle attribute adjustment module.

The global list `ALLOWED_FIELDS` specifies which keys in a vehicle dictionary
are permitted to be updated.  The function `adjust_vehicle_info` applies the
modifications in a safe, type‑checked manner.
"""

from typing import Dict, Any

# List of keys that may be updated on a vehicle dictionary.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "engine_type",
    "transmission",
    "body_style",
]

def adjust_vehicle_info(auto: Dict[str, Any], modifications: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update permitted fields of a vehicle dictionary.

    Parameters
    ----------
    auto : dict
        The original vehicle data. Must be a mutable mapping.
    modifications : dict
        A mapping of keys to new values.

    Returns
    -------
    dict
        The same dictionary object with authorized updates applied.

    Raises
    ------
    TypeError
        If `auto` or `modifications` are not dictionaries.
    KeyError
        If a modification key is not in ``ALLOWED_FIELDS``.
    ValueError
        If a value type does not match the expected type for that field.

    Notes
    -----
    - The function modifies `auto` in place and returns it.
    - For security, only keys listed in ``ALLOWED_FIELDS`` are accepted.
    """
    if not isinstance(auto, dict):
        raise TypeError("auto must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")

    # Simple type expectations for common fields.
    _field_types = {
        "make": str,
        "model": str,
        "year": int,
        "color": str,
        "vin": str,
        "mileage": (int, float),
        "engine_type": str,
        "transmission": str,
        "body_style": str,
    }

    for key, value in modifications.items():
        if key not in ALLOWED_FIELDS:
            raise KeyError(f"Field '{key}' is not allowed to be modified")

        expected_type = _field_types.get(key)
        if expected_type is not None and not isinstance(value, expected_type):
            raise ValueError(
                f"Invalid type for field '{key}': "
                f"expected {expected_type.__name__}, got {type(value).__name__}"
            )

        # Perform the update
        auto[key] = value

    return auto