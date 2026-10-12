#!/usr/bin/env python3
"""
Secure employee record editor.

The module provides a single function `edit_personnel_info` that updates an
employee dictionary while preventing unauthorized modifications of sensitive
attributes.  The implementation follows the best‑practice pattern for
CWE-915 – *Improperly Controlled Modification of Dynamically‑Determined Object
Attributes*.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Public constants
# --------------------------------------------------------------------------- #

# Fields that a non‑admin user is allowed to edit.  All other fields require
# admin privileges.
EDITABLE_FIELDS = {
    "name",
    "position",
    "salary",
    "department",
}

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #

class InvalidFieldError(ValueError):
    """Raised when an adjustment contains a field that does not exist."""
class PermissionDeniedError(PermissionError):
    """Raised when the user attempts to modify a restricted field."""
class InvalidInputError(TypeError):
    """Raised when an argument is of an unexpected type."""

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def edit_personnel_info(
    employee_record: dict,
    adjustments: dict,
    admin_flag: bool
) -> dict:
    """
    Update an employee record with the given adjustments.

    Parameters
    ----------
    employee_record : dict
        Current state of an employee's details.
    adjustments : dict
        Key‑value pairs specifying the desired updates.
    admin_flag : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    InvalidInputError
        If either `employee_record` or `adjustments` is not a dictionary.
    InvalidFieldError
        If an adjustment refers to a non‑existent field in `employee_record`.
    PermissionDeniedError
        If a non‑admin attempts to modify a restricted field.

    Notes
    -----
    * The function does **not** modify the original `employee_record` in place.
      Instead, it returns a new dictionary instance.
    * The function explicitly rejects any attempt to modify keys that start
      with an underscore or that are not present in the original record.
    * The check for restricted fields is performed **before** any assignment,
      ensuring that no side‑effects occur if the operation would otherwise be
      disallowed.
    """
    # ---- Argument validation -------------------------------------------------
    if not isinstance(employee_record, dict):
        raise InvalidInputError(
            f"employee_record must be a dict; got {type(employee_record).__name__}"
        )
    if not isinstance(adjustments, dict):
        raise InvalidInputError(
            f"adjustments must be a dict; got {type(adjustments).__name__}"
        )
    if not isinstance(admin_flag, bool):
        raise InvalidInputError(
            f"admin_flag must be a bool; got {type(admin_flag).__name__}"
        )

    # ---- Prepare new record --------------------------------------------------
    updated = employee_record.copy()

    # ---- Process each adjustment --------------------------------------------
    for field, new_value in adjustments.items():
        # 1. Field must exist in the original record
        if field not in employee_record:
            raise InvalidFieldError(
                f"Attempted to modify unknown field '{field}'."
            )

        # 2. Non‑admin users can only change EDITABLE_FIELDS
        if not admin_flag and field not in EDITABLE_FIELDS:
            raise PermissionDeniedError(
                f"Insufficient privileges to modify field '{field}'."
            )

        # 3. Prevent accidental modification of protected internal keys
        if field.startswith("_"):
            raise PermissionDeniedError(
                f"Modification of private/internal field '{field}' is prohibited."
            )

        # 4. Apply the change
        updated[field] = new_value

    return updated

# --------------------------------------------------------------------------- #
# Example usage (commented out – for illustration only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample employee record
    emp = {
        "name": "Jane Doe",
        "position": "Engineer",
        "salary": 75000,
        "department": "R&D",
        "social_security_number": "123-45-6789"
    }

    # Non‑admin attempting to change the salary and SSN
    try:
        new_emp = edit_personnel_info(
            employee_record=emp,
            adjustments={"salary": 80000, "social_security_number": "987-65-4321"},
            admin_flag=False
        )
    except PermissionDeniedError as e:
        print(f"Permission error: {e}")

    # Admin performing the same updates
    new_emp = edit_personnel_info(
        employee_record=emp,
        adjustments={"salary": 80000, "social_security_number": "987-65-4321"},
        admin_flag=True
    )
    print("Updated record:", new_emp)