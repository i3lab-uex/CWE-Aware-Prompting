# -*- coding: utf-8 -*-

"""
Vehicle attribute updater.

This module defines a single function, :func:`update_vehicle_attributes`,
which safely updates fields of a vehicle dictionary while enforcing a
whitelist of modifiable keys.  The whitelist is defined by the global
``ALLOWED_FIELDS`` list.

The function raises :class:`ValueError` if any key in ``changes`` is not
present in ``ALLOWED_FIELDS``.

Security note: By strictly controlling which keys can be updated,
the implementation mitigates CWE‑915 (Improperly Controlled Modification
of Dynamically-Determined Object Attributes).
"""

from typing import Dict, Any

# Whitelist of fields that are permitted to be updated.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "odometer",
    "fuel_type",
]

def update_vehicle_attributes(automobile: Dict[str, Any],
                               changes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update allowed attributes of a vehicle dictionary.

    Parameters
    ----------
    automobile : dict
        Current state of the vehicle's attributes. Must be a mutable mapping.
    changes : dict
        Proposed updates where keys are attribute names and values are the new
        values to assign.

    Returns
    -------
    dict
        The same dictionary instance as ``automobile`` but with updated
        values for any keys that are in :data:`ALLOWED_FIELDS`.

    Raises
    ------
    ValueError
        If ``changes`` contains any key that is not in :data:`ALLOWED_FIELDS`.

    Examples
    --------
    >>> vehicle = {'make': 'Toyota', 'model': 'Camry', 'year': 2020}
    >>> update_vehicle_attributes(vehicle, {'color': 'red', 'year': 2021})
    {'make': 'Toyota', 'model': 'Camry', 'year': 2021, 'color': 'red'}
    >>> update_vehicle_attributes(vehicle, {'unknown': 123})
    Traceback (most recent call last):
        ...
    ValueError: Attempted to modify disallowed field(s): unknown
    """
    # Identify any disallowed fields in the proposed changes.
    disallowed = [key for key in changes if key not in ALLOWED_FIELDS]
    if disallowed:
        raise ValueError(
            f"Attempted to modify disallowed field(s): {', '.join(disallowed)}"
        )

    # Apply the allowed changes.
    for key, value in changes.items():
        automobile[key] = value

    return automobile