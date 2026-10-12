# -*- coding: utf-8 -*-
"""
Vehicle information updater.

This module defines a single public function `adjust_vehicle_info` that
updates only a predefined set of fields on a vehicle dictionary.  The
allowed fields are listed in the global constant `ALLOWED_FIELDS`.

The function mutates the supplied dictionary *in place* and returns it
for convenience.  If a requested modification references an attribute
that is not in `ALLOWED_FIELDS`, a ``ValueError`` is raised.

The implementation is intentionally minimal to avoid unnecessary
dependencies while still being clear and secure.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

#: Fields that are permitted to be updated by :func:`adjust_vehicle_info`.
ALLOWED_FIELDS = {
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "price",
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def adjust_vehicle_info(auto: dict, modifications: dict) -> dict:
    """
    Update a vehicle dictionary with the supplied modifications.

    Parameters
    ----------
    auto : dict
        The original vehicle dictionary.  It is modified in place.
    modifications : dict
        Mapping of attribute names to new values.

    Returns
    -------
    dict
        The same dictionary object, now updated with authorized fields.

    Raises
    ------
    ValueError
        If *modifications* contains a key that is not in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    The function deliberately avoids performing deep copies or type checks on
    the values, because the caller is responsible for ensuring that the data
    types are appropriate.  Only the keys are validated against a whitelist.
    """
    if not isinstance(auto, dict):
        raise TypeError(f"'auto' must be a dict, got {type(auto).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(f"'modifications' must be a dict, got {type(modifications).__name__}")

    # Identify any disallowed fields
    invalid_fields = set(modifications) - ALLOWED_FIELDS
    if invalid_fields:
        raise ValueError(
            f"The following fields are not permitted to be modified: "
            f"{', '.join(sorted(invalid_fields))}"
        )

    # Apply the authorized modifications
    for key, value in modifications.items():
        auto[key] = value

    return auto