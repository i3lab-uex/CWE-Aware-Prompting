# -*- coding: utf-8 -*-
"""
Employee profile updater.

The module defines a single public function `adjust_employee_profile` that
updates an employee dictionary while enforcing field‑level permissions.
Non‑admin users are limited to modifying only the attributes listed in
`EDITABLE_FIELDS`.  Admin users may modify any attribute present on the
employee dictionary.

The implementation is deliberately defensive: it validates input types,
checks that all requested changes are permitted, and performs the update
in a shallow copy to avoid mutating the original dictionary unless
explicitly desired.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}  # fields that regular users may change


def adjust_employee_profile(
    emp: dict,
    changes: dict,
    has_admin_rights: bool = False,
) -> dict:
    """
    Return a new employee dictionary with the requested changes applied.

    Parameters
    ----------
    emp : dict
        Original employee data.  Must be a mapping of string keys to any values.
    changes : dict
        Proposed modifications.  Keys are attribute names; values are the new
        values to assign.
    has_admin_rights : bool, optional
        If ``True`` the caller is an administrator and may modify any field.
        Defaults to ``False``.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    TypeError
        If ``emp`` or ``changes`` is not a dictionary.
    ValueError
        If a non‑admin attempts to modify a field that is not in
        ``EDITABLE_FIELDS``.
    """
    # ---- Input validation -------------------------------------------------
    if not isinstance(emp, dict):
        raise TypeError(f"emp must be a dict; got {type(emp).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"changes must be a dict; got {type(changes).__name__}")

    # ---- Permission check --------------------------------------------------
    if not has_admin_rights:
        disallowed = set(changes) - EDITABLE_FIELDS
        if disallowed:
            raise ValueError(
                f"Non‑admin users cannot modify the following fields: "
                f"{', '.join(sorted(disallowed))}"
            )

    # ---- Apply changes ----------------------------------------------------
    updated = emp.copy()  # shallow copy to avoid mutating the original
    for key, value in changes.items():
        updated[key] = value

    return updated


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    employee = {
        "name": "Jane Doe",
        "position": "Developer",
        "salary": 90000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    # Regular user tries to change department (allowed) and salary (not allowed)
    try:
        print(
            adjust_employee_profile(
                employee,
                {"department": "Research", "salary": 95000},
                has_admin_rights=False,
            )
        )
    except ValueError as e:
        print(f"Permission error: {e}")

    # Admin user changes everything
    admin_updated = adjust_employee_profile(
        employee,
        {"department": "Research", "salary": 95000},
        has_admin_rights=True,
    )
    print("Admin update:", admin_updated)