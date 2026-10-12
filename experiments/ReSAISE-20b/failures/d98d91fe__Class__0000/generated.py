# -*- coding: utf-8 -*-
"""
Vehicle attribute updater.

The module exposes a single public function :func:`modify_car_details` that
updates only the attributes listed in ``ALLOWED_FIELDS``.  Any attempt to
modify a disallowed field raises :class:`ValueError`.  The function returns a
new dictionary containing the updated state; the original ``car`` object is left
unchanged to avoid unintended side effects.

The implementation follows best practices for defensive programming and
avoids the CWE‑913 vulnerability by strictly controlling which attributes may
be altered.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, List

# --------------------------------------------------------------------------- #
# Global configuration – list of fields that may be updated
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS: List[str] = [
    "make",
    "model",
    "year",
    "color",
    "mileage",
    "vin",  # Vehicle Identification Number
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def modify_car_details(car: Dict[str, Any], changes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new car dictionary with the requested updates applied.

    Parameters
    ----------
    car : dict
        The original vehicle dictionary.  Must be a mapping of attribute names
        to values.
    changes : dict
        Mapping from attribute name to the new value that should be applied.

    Returns
    -------
    dict
        A shallow copy of ``car`` with the specified changes applied.

    Raises
    ------
    ValueError
        If ``changes`` contains a key that is not present in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    * The function performs a shallow copy of the input dictionary.  Nested
      mutable objects are not deeply copied; callers should be aware if their
      ``car`` contains such structures.
    * The function does not modify the input ``car`` in place.  This design
      choice protects callers from accidental mutation and aligns with the
      principle of least astonishment.

    Examples
    --------
    >>> car = {"make": "Toyota", "model": "Corolla", "year": 2015}
    >>> changes = {"color": "red", "mileage": 120000}
    >>> modify_car_details(car, changes)
    {'make': 'Toyota', 'model': 'Corolla', 'year': 2015, 'color': 'red', 'mileage': 120000}
    """
    # Validate that all requested changes are allowed
    for field in changes:
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not permitted for update")

    # Create a shallow copy to avoid mutating the caller's dictionary
    updated_car = copy.copy(car)

    # Apply allowed changes
    for field, value in changes.items():
        updated_car[field] = value

    return updated_car