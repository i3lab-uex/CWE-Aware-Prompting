#!/usr/bin/env python3
"""
Utility to safely edit employee profile dictionaries.

The module defines a global constant `EDITABLE_FIELDS` that lists the
attributes a non‑admin user is allowed to modify.  The function
`edit_profile_data` applies updates from a `modifications` dictionary to an
existing `profile`, respecting the permissions indicated by
`is_superuser`.  It returns a new dictionary containing the updated data.

Security considerations:
* Only whitelisted keys are applied when `is_superuser` is False.
* An attempt to modify a non‑editable field raises a ValueError, preventing
  accidental or malicious changes (CWE‑915).
* The original profile is not mutated – a shallow copy is returned.
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# --------------------------------------------------------------------------- #
#  Global constant: fields that non‑admin users may modify
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add more fields as required
}


# --------------------------------------------------------------------------- #
#  Core function
# --------------------------------------------------------------------------- #
def edit_profile_data(
    profile: Dict[str, Any],
    modifications: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with the requested modifications.

    Parameters
    ----------
    profile : dict
        Current employee profile.  Must be a mapping of string keys to any values.
    modifications : dict
        Mapping of field names to new values that should be applied.
    is_superuser : bool
        ``True`` if the caller has administrative privileges and may modify any field;
        otherwise only fields listed in :data:`EDITABLE_FIELDS` are allowed.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.  The input `profile`
        is left unchanged.

    Raises
    ------
    ValueError
        If a modification attempts to change a field that is not permitted for
        non‑admin users.
    TypeError
        If `profile` or `modifications` is not a mapping type.
    """

    # Basic type checks
    if not isinstance(profile, dict):
        raise TypeError("profile must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")

    # Create a shallow copy to avoid mutating the original profile
    updated_profile = copy.deepcopy(profile)

    # Iterate over requested changes and apply them with permission checks
    for key, new_value in modifications.items():
        if not isinstance(key, str):
            raise ValueError(f"Profile field name must be a string, got {key!r}")

        if is_superuser:
            # Superusers may modify any field
            updated_profile[key] = new_value
        else:
            # Non‑admin: check against the whitelist
            if key not in EDITABLE_FIELDS:
                raise ValueError(
                    f"Modification of field '{key}' is not allowed for non‑admin users"
                )
            updated_profile[key] = new_value

    return updated_profile


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    example_profile = {
        "name": "Jane Doe",
        "position": "Engineer",
        "salary": 85000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    # Non‑admin trying to change allowed field
    mod = {"department": "Product"}
    print(edit_profile_data(example_profile, mod, is_superuser=False))

    # Non‑admin trying to change disallowed field
    try:
        edit_profile_data(example_profile, {"salary": 90000}, is_superuser=False)
    except ValueError as e:
        print(e)

    # Admin changing any field
    print(edit_profile_data(example_profile, {"salary": 90000}, is_superuser=True))