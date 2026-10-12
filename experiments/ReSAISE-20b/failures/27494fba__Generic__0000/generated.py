# adjust_employee_profile.py

from copy import deepcopy
from typing import Dict, Any


# Fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}


def adjust_employee_profile(
    emp: Dict[str, Any],
    changes: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Update an employee dictionary with the supplied changes.

    Parameters
    ----------
    emp : dict
        Original employee record.
    changes : dict
        Proposed modifications. Keys must correspond to fields in `emp`.
    has_admin_rights : bool
        If True, the caller is an administrator and may modify any field.
        Otherwise only fields in :data:`EDITABLE_FIELDS` are allowed.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    PermissionError
        If a non‑admin attempts to modify a field not in :data:`EDITABLE_FIELDS`.
    KeyError
        If ``changes`` contains a key that does not exist in ``emp``.
    """
    # Work on a copy to avoid mutating the caller's dictionary
    updated_emp = deepcopy(emp)

    for field, new_value in changes.items():
        if field not in emp:
            # Reject unknown fields – could be a typo or an attempt to add
            # unsupported attributes.
            raise KeyError(f"Field '{field}' does not exist in the employee record.")

        # Non‑admin users can only edit permitted fields
        if not has_admin_rights and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"User lacks permission to modify the field '{field}'."
            )

        # Perform the update
        updated_emp[field] = new_value

    return updated_emp