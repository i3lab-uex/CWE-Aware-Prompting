#!/usr/bin/env python3
"""
Employee profile editing utility.

This module defines a single function `edit_profile_data` that updates an
employee's profile dictionary based on supplied modifications while enforcing
access control. Non‑admin users may only change fields listed in the global
`EDITABLE_FIELDS` set; superusers can modify any field.

The function returns a new dictionary representing the updated profile,
leaving the original unchanged. It performs minimal validation to avoid
accidental corruption of critical data such as social security numbers.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    "email",
    "phone_number",
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_valid_key(key: str) -> bool:
    """
    Check whether a key is a valid dictionary key for an employee profile.
    This simple implementation assumes that all keys are strings; more
    sophisticated checks (e.g., against a schema) could be added here.
    """
    return isinstance(key, str)

def _sanitize_value(value: Any) -> Any:
    """
    Basic sanitisation to prevent inadvertent injection of dangerous objects.
    For demonstration purposes we only allow primitive types.  In a real
    application this should be expanded to handle more complex validation.
    """
    if isinstance(value, (str, int, float, bool)):
        return value
    raise ValueError(f"Unsupported value type: {type(value).__name__}")

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def edit_profile_data(
    profile: Dict[str, Any],
    modifications: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return an updated copy of *profile* after applying *modifications*.

    Parameters
    ----------
    profile : dict
        Current employee profile.  The function does not modify this object.
    modifications : dict
        Mapping of fields to new values.  Only keys present in the profile
        will be considered; unknown keys are ignored.
    is_superuser : bool
        If True, all fields may be updated.  If False, only keys listed in
        ``EDITABLE_FIELDS`` are applied.

    Returns
    -------
    dict
        A new dictionary containing the updated profile data.

    Raises
    ------
    PermissionError
        If a non‑superuser attempts to modify a disallowed field.
    ValueError
        If a modification key is invalid or the value type is unsupported.

    Notes
    -----
    The function performs shallow copying of the profile.  Nested mutable
    structures are not deep‑copied; callers should be aware of this behaviour.
    """
    if not isinstance(profile, dict):
        raise TypeError("profile must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")

    # Create a shallow copy to avoid mutating the input
    updated_profile = copy.deepcopy(profile)

    for key, new_value in modifications.items():
        if not _is_valid_key(key):
            raise ValueError(f"Invalid key type: {key!r}")

        if key not in profile:
            # Ignore unknown fields; alternatively, raise an error
            continue

        if not is_superuser and key not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin users cannot modify the '{key}' field."
            )

        # Basic value sanitisation
        sanitized_value = _sanitize_value(new_value)

        updated_profile[key] = sanitized_value

    return updated_profile

# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    sample_profile = {
        "name": "Jane Doe",
        "position": "Developer",
        "salary": 85000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
        "email": "jane.doe@example.com",
    }

    mods = {
        "position": "Senior Developer",
        "salary": 95000,          # should raise PermissionError for non‑admin
        "email": "jane.new@example.com",
    }

    try:
        new_profile = edit_profile_data(sample_profile, mods, is_superuser=False)
        print("Updated profile:", new_profile)
    except Exception as exc:
        print(f"Error: {exc}")