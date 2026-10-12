# -*- coding: utf-8 -*-
"""
Vehicle information adjustment module.

This module provides a single function `adjust_vehicle_info` that safely updates
specific attributes of a vehicle dictionary. Only fields listed in the global
`ALLOWED_FIELDS` list are permitted to be modified.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable


# List of fields that are allowed to be updated. Extend this list as needed.
ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "mileage",
)


def _validate_modifications(modifications: Dict[str, Any]) -> None:
    """
    Validate that all keys in `modifications` are present in ALLOWED_FIELDS.

    Raises:
        ValueError: If any key is not allowed.
    """
    disallowed = set(modifications) - set(ALLOWED_FIELDS)
    if disallowed:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(sorted(disallowed))}"
        )


def adjust_vehicle_info(auto: Dict[str, Any], modifications: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new vehicle dictionary with allowed fields updated.

    Parameters
    ----------
    auto : dict
        The original vehicle data. This dictionary is **not** modified in place.
    modifications : dict
        Mapping of attribute names to new values. Only keys present in
        `ALLOWED_FIELDS` will be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.

    Raises
    ------
    ValueError
        If `modifications` contains a key that is not in `ALLOWED_FIELDS`.

    Notes
    -----
    * The function performs a shallow copy of the original dictionary to avoid
      side‑effects on caller data.
    * This implementation intentionally avoids modifying the original dictionary
      to prevent unintended resource leaks or state inconsistencies.
    """
    # Validate modifications first to avoid partially applying changes
    _validate_modifications(modifications)

    # Create a shallow copy to preserve the original data
    updated_auto = copy.deepcopy(auto)

    # Apply each allowed modification
    for field, value in modifications.items():
        updated_auto[field] = value

    return updated_auto