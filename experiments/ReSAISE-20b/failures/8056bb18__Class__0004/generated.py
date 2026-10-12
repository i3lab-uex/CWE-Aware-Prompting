# -*- coding: utf-8 -*-
"""
Vehicle data modification utility.

This module provides a single public function `modify_vehicle_data` that
updates only whitelisted attributes of a vehicle dictionary.  The list of
allowed fields is defined by the global constant `ALLOWED_FIELDS`.  Any attempt
to modify a field not present in this list will raise a `ValueError`.

The implementation deliberately avoids any form of dynamic code execution
(e.g. eval, exec) to mitigate CWE‑913 vulnerabilities.
"""

from __future__ import annotations

from typing import Dict, Any


# Global list of attributes that are permitted to be updated.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "fuel_type",
    "transmission",
]

def modify_vehicle_data(
    vehicle_info: Dict[str, Any],
    modifications: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update the provided `vehicle_info` dictionary with values from
    `modifications`, but only for keys that are present in the global
    ``ALLOWED_FIELDS`` list.

    Parameters
    ----------
    vehicle_info : dict
        Dictionary containing the current state of a vehicle.  Must be a mutable
        mapping.
    modifications : dict
        Dictionary containing the desired changes.  Keys that are not in
        ``ALLOWED_FIELDS`` will cause a :class:`ValueError`.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle information.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If ``modifications`` contains keys that are not in ``ALLOWED_FIELDS``.

    Notes
    -----
    - The function does **not** modify the input ``vehicle_info`` in place.
      It returns a new dictionary, leaving the original untouched.
    - This design choice prevents accidental side‑effects and makes unit
      testing straightforward.

    Examples
    --------
    >>> vehicle = {'make': 'Toyota', 'model': 'Corolla', 'year': 2010}
    >>> modify_vehicle_data(vehicle, {'color': 'red', 'vin': '123'})
    {'make': 'Toyota', 'model': 'Corolla', 'year': 2010, 'color': 'red', 'vin': '123'}
    """
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")

    # Identify disallowed keys
    disallowed = set(modifications) - set(ALLOWED_FIELDS)
    if disallowed:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(sorted(disallowed))}"
        )

    # Create a shallow copy to avoid mutating the original
    updated = vehicle_info.copy()
    updated.update(modifications)
    return updated

# End of module