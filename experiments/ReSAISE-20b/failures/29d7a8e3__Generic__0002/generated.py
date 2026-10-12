#!/usr/bin/env python3
"""
Utility to edit employee profile data safely.

The module defines a global constant `EDITABLE_FIELDS` which lists the keys
that a non‑admin user is allowed to modify.  The function `edit_profile_data`
creates a new profile dictionary containing the requested changes, enforcing
the edit rules and performing basic validation.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

from typing import Any, Dict, Iterable


# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# Fields that can be modified by non‑admin users.
EDITABLE_FIELDS: Iterable[str] = (
    "name",
    "position",
    "department",
    # Add more fields here as required
)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def edit_profile_data(
    profile: Dict[str, Any],
    modifications: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return an updated employee profile dictionary.

    Parameters
    ----------
    profile : dict
        The current employee profile.  Keys should be strings.
    modifications : dict
        Mapping of fields to new values that the caller wishes to apply.
    is_superuser : bool
        If ``True`` the caller may modify any field; otherwise only fields in
        :data:`EDITABLE_FIELDS` are allowed.

    Returns
    -------
    dict
        A new dictionary containing the updated profile data.  The original
        ``profile`` is not modified.

    Raises
    ------
    TypeError
        If any of the arguments are not of the expected type.
    ValueError
        If a non‑admin attempts to modify a disallowed field.

    Notes
    -----
    The function performs shallow copying; nested objects are not deep‑copied.
    """
    # ---------- Input validation ----------
    if not isinstance(profile, dict):
        raise TypeError(f"Expected profile to be a dict, got {type(profile).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(f"Expected modifications to be a dict, got {type(modifications).__name__}")
    if not isinstance(is_superuser, bool):
        raise TypeError(f"Expected is_superuser to be a bool, got {type(is_superuser).__name__}")

    # ---------- Enforce edit rules ----------
    if not is_superuser:
        disallowed = [key for key in modifications if key not in EDITABLE_FIELDS]
        if disallowed:
            raise ValueError(
                f"Non‑admin users cannot modify the following fields: {', '.join(disallowed)}"
            )

    # ---------- Apply changes ----------
    updated_profile = profile.copy()
    for key, value in modifications.items():
        # Basic safety: ensure keys are strings
        if not isinstance(key, str):
            raise TypeError(f"Profile field names must be strings; got {type(key).__name__}")
        updated_profile[key] = value

    return updated_profile


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to run)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Example profile
    emp_profile = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 90000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    # Non‑admin attempt to change allowed fields
    try:
        new_profile = edit_profile_data(
            emp_profile,
            {"position": "Senior Engineer", "department": "Product"},
            is_superuser=False
        )
        print("Non‑admin update succeeded:", new_profile)
    except Exception as e:
        print("Error:", e)

    # Non‑admin attempt to change disallowed field
    try:
        edit_profile_data(
            emp_profile,
            {"salary": 95000},
            is_superuser=False
        )
    except Exception as e:
        print("Expected error:", e)

    # Admin update
    admin_profile = edit_profile_data(
        emp_profile,
        {"salary": 95000, "social_security_number": "987-65-4321"},
        is_superuser=True
    )
    print("Admin update succeeded:", admin_profile)