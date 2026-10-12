from __future__ import annotations

import copy
from typing import Dict, Any

# Define the fields that are allowed to be modified.
ALLOWED_FIELDS = {"make", "model", "year", "color", "vin"}

def alter_vehicle_info(details: Dict[str, Any], modifications: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a vehicle's attributes with the provided modifications.

    Parameters
    ----------
    details : dict
        Current state of vehicle attributes. Must be a dictionary.
    modifications : dict
        Fields and new values to update in the vehicle. Keys must be present in ``ALLOWED_FIELDS``.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle attributes.

    Raises
    ------
    TypeError
        If either ``details`` or ``modifications`` is not a dictionary.
    ValueError
        If any key in ``modifications`` is not listed in ``ALLOWED_FIELDS``.

    Notes
    -----
    This function returns a new dictionary and does not modify the input ``details`` in place,
    preventing accidental side‑effects. The function also performs a shallow copy of the
    values to avoid inadvertent mutation of mutable objects stored in ``details``.
    """
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary.")
    if not isinstance(modifications, dict):
        raise TypeError("`modifications` must be a dictionary.")

    # Check for disallowed keys
    disallowed = set(modifications) - ALLOWED_FIELDS
    if disallowed:
        raise ValueError(f"Attempted to modify disallowed fields: {', '.join(sorted(disallowed))}")

    # Create a shallow copy to avoid mutating the original dictionary
    updated = copy.copy(details)

    # Apply modifications
    for key, value in modifications.items():
        updated[key] = value

    return updated