#!/usr/bin/env python3
"""
Utility for safely editing employee profile data.

The module defines a single public function `edit_profile_data` that updates
fields in an employee profile dictionary.  Only fields listed in the global
constant `EDITABLE_FIELDS` may be modified by non‑admin users.  Superusers are
allowed to modify any field.

The implementation follows the principle of least privilege and guards against
CWE‑915 (Improperly Controlled Modification of Dynamically-Determined Object
Attributes).
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global constants
# --------------------------------------------------------------------------- #

# Fields that may be modified by a non‑admin user.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Salary is intentionally omitted to protect financial data.
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def edit_profile_data(
    profile: dict,
    modifications: dict,
    is_superuser: bool
) -> dict:
    """
    Return a new profile dictionary with the requested modifications applied.

    Parameters
    ----------
    profile : dict
        The original employee profile.  Keys should be strings; values may be
        any JSON‑serialisable type.
    modifications : dict
        Mapping of field names to new values that should be applied.
    is_superuser : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A shallow copy of ``profile`` with the allowed modifications applied.

    Raises
    ------
    ValueError
        If a modification attempts to change a field that the caller is not
        permitted to edit.
    TypeError
        If ``profile`` or ``modifications`` is not a dictionary.
    """
    # Validate input types early
    if not isinstance(profile, dict):
        raise TypeError(f"profile must be a dict, got {type(profile).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(f"modifications must be a dict, got {type(modifications).__name__}")

    # Create a shallow copy to avoid mutating the original
    updated_profile = profile.copy()

    for field, new_value in modifications.items():
        # Non‑admin users can only edit a restricted set of fields
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Modification of field '{field}' is not permitted for non‑admin users."
            )

        # Optionally, enforce that the field actually exists in the profile.
        # If it does not exist we can choose to ignore or add; here we allow adding.
        updated_profile[field] = new_value

    return updated_profile