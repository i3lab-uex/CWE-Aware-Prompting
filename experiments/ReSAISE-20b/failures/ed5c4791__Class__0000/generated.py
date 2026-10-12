import copy

# Global set of fields that regular users are allowed to edit
EDITABLE_FIELDS = {"name", "position", "department"}

def modify_employee_data(worker: dict, alterations: dict, admin_privileges: bool) -> dict:
    """
    Modify an employee's data while enforcing field-level permissions.

    Args:
        worker (dict): The original employee record.
        alterations (dict): Proposed changes keyed by field name.
        admin_privileges (bool): Whether the caller has administrative rights.

    Returns:
        dict: A new dictionary containing the updated employee data.

    Raises:
        ValueError: If a non‑admin attempts to modify a restricted field.
        TypeError: If inputs are not of the expected type.
    """
    # Basic type validation
    if not isinstance(worker, dict):
        raise TypeError("worker must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary")
    if not isinstance(admin_privileges, bool):
        raise TypeError("admin_privileges must be a boolean")

    # Create a shallow copy to avoid mutating the original worker
    updated_worker = copy.deepcopy(worker)

    for field, new_value in alterations.items():
        # Skip if the field doesn't exist on the worker
        if field not in updated_worker:
            continue

        # Enforce permissions for non‑admin users
        if not admin_privileges and field not in EDITABLE_FIELDS:
            raise ValueError(f"Insufficient privileges to modify '{field}'")

        # Apply the change
        updated_worker[field] = new_value

    return updated_worker