# SPDX-License-Identifier: MIT

"""
Vehicle attribute updater.

The module defines a single public function :func:`alter_vehicle_info`
which updates only whitelisted fields of a vehicle dictionary.  The
whitelist is defined by the global :data:`ALLOWED_FIELDS` list.

The function performs defensive checks to avoid CWE‑915: it refuses
to modify any attribute not explicitly listed in the whitelist and
does not expose internal state to external mutation.
"""

from __future__ import annotations

import logging
from typing import Dict, Any, Iterable

# Configure a basic logger.  In production this would likely be
# replaced by an application‑wide logging configuration.
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# Public constants
# ----------------------------------------------------------------------
ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "color",
    "vin",
    "owner",
)

# ----------------------------------------------------------------------
# Public API
# ----------------------------------------------------------------------
def alter_vehicle_info(details: Dict[str, Any], modifications: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new dictionary containing the vehicle information from
    *details* updated with any valid modifications specified in
    *modifications*.

    Parameters
    ----------
    details : dict
        Current state of the vehicle.  The function will **not** modify
        this dictionary in place.
    modifications : dict
        Keys and values that should be applied to *details*.

    Returns
    -------
    dict
        A new dictionary that contains the updated vehicle state.

    Raises
    ------
    ValueError
        If *modifications* contains no keys that are allowed.

    Notes
    -----
    - The function is defensive: it only updates keys that are listed in
      :data:`ALLOWED_FIELDS`.  All other keys are ignored.
    - The returned dictionary is a shallow copy of *details* with the
      allowed modifications applied.
    - If *modifications* contains none of the whitelisted keys, a
      :class:`ValueError` is raised to signal that no meaningful update
      could be performed.
    """
    if not isinstance(details, dict):
        raise TypeError(f"details must be a dict, got {type(details).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(f"modifications must be a dict, got {type(modifications).__name__}")

    # Convert ALLOWED_FIELDS to a set for O(1) membership checks.
    allowed = set(ALLOWED_FIELDS)

    # Identify which modifications are actually permitted.
    valid_mods = {k: v for k, v in modifications.items() if k in allowed}

    if not valid_mods:
        _logger.warning(
            "No modifications were applied because none of the provided keys "
            f"are allowed: {list(modifications.keys())}"
        )
        raise ValueError(
            "modifications contain no allowed fields; nothing to update."
        )

    # Create a shallow copy of the original details.
    updated = dict(details)

    # Apply each permitted modification.
    for key, value in valid_mods.items():
        _logger.debug("Updating field '%s' to '%s'", key, value)
        updated[key] = value

    _logger.info(
        "Vehicle info updated: %s", ", ".join(f"{k}={v!r}" for k, v in valid_mods.items())
    )

    return updated