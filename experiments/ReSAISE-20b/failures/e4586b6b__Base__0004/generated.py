# -*- coding: utf-8 -*-

"""
Vehicle attribute updater.

The module defines a single public function `update_vehicle_attributes` that
updates an automobile dictionary with a set of changes while enforcing
a strict whitelist of permissible fields.  This protects against
CWE‑915: Improperly Controlled Modification of Dynamically-Determined
Object Attributes.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration: list of attribute names that are allowed to be updated.
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "transmission",
    # Add any other fields that are safe to modify here.
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def update_vehicle_attributes(
    automobile: dict,
    changes: dict,
) -> dict:
    """
    Update an `automobile` dictionary with values from `changes`.

    Parameters
    ----------
    automobile : dict
        The current state of the vehicle.  It is **not** modified in place;
        a new dictionary is returned.
    changes : dict
        Mapping of attribute names to new values.  Only keys listed in
        ``ALLOWED_FIELDS`` are accepted.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle attributes.

    Raises
    ------
    ValueError
        If any key in `changes` is not present in ``ALLOWED_FIELDS``.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    * The function performs a shallow copy of the original vehicle data.
      Nested mutable structures are therefore shared between the input and
      returned dictionary.  If deep copying is required, use ``copy.deepcopy``
      before calling this function.
    * Keys in `changes` that are not present in ``automobile`` will be
      added to the result, provided they are allowed.
    """
    if not isinstance(automobile, dict):
        raise TypeError(f"Expected automobile to be a dict; got {type(automobile).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"Expected changes to be a dict; got {type(changes).__name__}")

    # Identify any disallowed fields
    invalid_keys = [k for k in changes if k not in ALLOWED_FIELDS]
    if invalid_keys:
        raise ValueError(f"Attempted to modify disallowed fields: {invalid_keys}")

    # Create a shallow copy and apply allowed changes
    updated = automobile.copy()
    for key, value in changes.items():
        # Basic type checks could be added here if needed
        updated[key] = value

    return updated


# --------------------------------------------------------------------------- #
# End of module
# --------------------------------------------------------------------------- #