# -*- coding: utf-8 -*-

"""
Vehicle data modifier.

This module defines a single function `modify_auto_data` which updates
only the fields that are explicitly allowed. The list of permitted
fields is defined by the global constant `ALLOWED_FIELDS`.  Attempts to
modify any other field will raise a ``ValueError``.
"""

from copy import deepcopy
from typing import Dict, Any

# Global list of fields that may be updated.  Add or remove items as
# necessary for your application.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "engine_type",
]

def modify_auto_data(auto_details: Dict[str, Any],
                     field_updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the vehicle details with a set of permitted field changes.

    Parameters
    ----------
    auto_details : dict
        Dictionary containing the current vehicle details.
    field_updates : dict
        Dictionary of fields to update with their new values.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle details.

    Raises
    ------
    ValueError
        If any key in ``field_updates`` is not present in
        :data:`ALLOWED_FIELDS`.

    Notes
    -----
    - The function does **not** modify the input ``auto_details`` in place.
      A deep copy is returned with the updates applied.
    - All keys are treated case‑sensitive; if you need case‑insensitivity,
      normalize the keys before passing them to this function.
    """
    # Validate that all requested updates are allowed
    invalid_fields = [k for k in field_updates if k not in ALLOWED_FIELDS]
    if invalid_fields:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(invalid_fields)}"
        )

    # Create a deep copy to avoid mutating the original dictionary
    updated_details = deepcopy(auto_details)

    # Apply allowed updates
    for key, value in field_updates.items():
        updated_details[key] = value

    return updated_details