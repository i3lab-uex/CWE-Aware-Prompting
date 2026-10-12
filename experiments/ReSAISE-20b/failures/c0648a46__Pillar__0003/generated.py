#!/usr/bin/env python3
"""
Employee profile modifier.

This module defines a single public function `modify_employee_profile` that updates an
employee's profile dictionary.  Non‑admin users may only modify a whitelisted set of
fields defined by the global constant `EDITABLE_FIELDS`.  Attempts to modify any other
field will raise a ``PermissionError``.

The implementation is deliberately defensive: it validates input types, makes a
shallow copy of the profile to avoid accidental mutation of callers' data,
and performs field‑level validation before applying changes.  No external
resources are created or held, so the risk of CWE‑664 (improper control of a
resource) is mitigated by design.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Fields that non‑privileged users are allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add other safe-to-edit fields here.
}

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #

class UnauthorizedFieldError(PermissionError):
    """Raised when a non‑admin user attempts to modify a protected field."""
    pass

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def modify_employee_profile(
    worker: dict,
    changes: dict,
    is_privileged: bool
) -> dict:
    """
    Return a new employee profile dictionary with the requested changes applied.

    Parameters
    ----------
    worker : dict
        Current employee profile.  Must be a mapping of string keys to any values.
    changes : dict
        Mapping of field names to new values that should be applied.
    is_privileged : bool
        ``True`` if the caller has administrative rights; otherwise only
        fields listed in :data:`EDITABLE_FIELDS` may be modified.

    Returns
    -------
    dict
        A shallow copy of ``worker`` with the applied changes.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    UnauthorizedFieldError
        If a non‑admin attempts to modify a field outside :data:`EDITABLE_FIELDS`.
    KeyError
        If ``changes`` contains a key that is not present in ``worker``.

    Notes
    -----
    The function performs a shallow copy of the profile; nested mutable objects are
    not deep‑copied.  This is intentional to preserve reference semantics for such
    nested objects while still preventing accidental mutation of the original
    dictionary passed by the caller.
    """

    # --------------------------------------------------------------------- #
    # Argument validation
    # --------------------------------------------------------------------- #
    if not isinstance(worker, dict):
        raise TypeError(f"'worker' must be a dict; got {type(worker).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"'changes' must be a dict; got {type(changes).__name__}")
    if not isinstance(is_privileged, bool):
        raise TypeError(f"'is_privileged' must be a bool; got {type(is_privileged).__name__}")

    # --------------------------------------------------------------------- #
    # Prepare the updated profile
    # --------------------------------------------------------------------- #
    updated_profile = worker.copy()  # shallow copy to avoid mutating caller's dict

    for field, new_value in changes.items():
        # Ensure the field exists in the original profile
        if field not in worker:
            raise KeyError(f"Field '{field}' does not exist in the employee profile")

        # Enforce edit permissions
        if not is_privileged and field not in EDITABLE_FIELDS:
            raise UnauthorizedFieldError(
                f"Non‑privileged users cannot modify the field '{field}'"
            )

        # Apply the change
        updated_profile[field] = new_value

    return updated_profile

# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample employee profile
    emp = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 90000,
        "department": "R&D",
        "social_security_number": "123-45-6789"
    }

    # Non‑admin attempting to change salary (should raise error)
    try:
        modify_employee_profile(
            worker=emp,
            changes={"salary": 95000},
            is_privileged=False
        )
    except UnauthorizedFieldError as e:
        print(f"Unauthorized change: {e}")

    # Admin updating salary
    updated = modify_employee_profile(
        worker=emp,
        changes={"salary": 95000, "department": "Product"},
        is_privileged=True
    )
    print("Updated profile:", updated)