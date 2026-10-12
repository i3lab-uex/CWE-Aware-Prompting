# SPDX-License-Identifier: MIT

"""
Utility for updating vehicle information while restricting modifications to a predefined set of fields.
"""

from typing import Dict, List

# Global list of attributes that may be updated.  Add or remove fields as required.
ALLOWED_FIELDS: List[str] = [
    "make",
    "model",
    "year",
    "owner",
    "registration"
]


def update_vehicle_info(vehicle: Dict, updates: Dict) -> Dict:
    """
    Update a vehicle dictionary with new values for allowed fields.

    Parameters
    ----------
    vehicle : dict
        The original vehicle object.  It is modified in place.
    updates : dict
        A mapping of field names to new values.

    Returns
    -------
    dict
        The updated vehicle dictionary (same object as ``vehicle``).

    Raises
    ------
    ValueError
        If an attempt is made to modify a field that is not in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    * Only keys present in ``updates`` that are also listed in :data:`ALLOWED_FIELDS`
      will be applied.
    * Keys not present in ``updates`` are left untouched.
    * This function performs a shallow update; nested structures are not deep‑copied.

    Examples
    --------
    >>> v = {"make": "Toyota", "model": "Corolla", "year": 2010, "owner": "Alice"}
    >>> update_vehicle_info(v, {"model": "Camry", "year": 2015})
    {'make': 'Toyota', 'model': 'Camry', 'year': 2015, 'owner': 'Alice'}

    >>> update_vehicle_info(v, {"unknown": "value"})
    Traceback (most recent call last):
        ...
    ValueError: Attempt to modify disallowed field 'unknown'
    """
    allowed_set = set(ALLOWED_FIELDS)

    for key, value in updates.items():
        if key not in allowed_set:
            raise ValueError(f"Attempt to modify disallowed field '{key}'")

        # Perform the update
        vehicle[key] = value

    return vehicle