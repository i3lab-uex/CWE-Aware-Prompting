# -*- coding: utf-8 -*-
"""
Vehicle attribute updater.

This module provides a single public function `update_vehicle_attributes`
which updates only the fields specified in the global ``ALLOWED_FIELDS``
list.  Attempting to modify any other key will raise a ``ValueError``.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "color",
    "vin",
    "registration_number",
)

def update_vehicle_attributes(
    automobile: Dict[str, Any], changes: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Return a new vehicle dictionary with allowed attributes updated.

    Parameters
    ----------
    automobile : dict
        The original vehicle state.  Keys represent attributes such as
        ``make`` or ``model``.
    changes : dict
        Keys and values that should be merged into the vehicle.  Only keys
        listed in :data:`ALLOWED_FIELDS` are accepted.

    Returns
    -------
    dict
        A shallow copy of ``automobile`` with the valid updates applied.

    Raises
    ------
    ValueError
        If ``changes`` contains a key that is not in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    * The function does **not** modify the original ``automobile`` dictionary.
      Instead it returns a new dictionary, leaving the input untouched.
    * ``changes`` may be empty; in that case the original dictionary is
      returned unchanged (but as a new copy to preserve immutability).
    """
    # Ensure we work with a fresh dictionary
    updated = copy.deepcopy(automobile)

    for key, value in changes.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(
                f"Attempt to modify disallowed field '{key}'. "
                f"Allowed fields: {sorted(ALLOWED_FIELDS)}"
            )
        updated[key] = value

    return updated