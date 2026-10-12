#!/usr/bin/env python3
"""
Utility for updating an employee profile safely.
"""

from typing import Dict, Any

# Fields that a non‑admin user is allowed to modify.
EDITABLE_FIELDS = {"name", "position", "department"}


def _validate_dict(name: str, value: Any) -> None:
    """Internal helper to validate that a value is a dictionary."""
    if not isinstance(value, dict):
        raise TypeError(f"'{name}' must be a dict, got {type(value).__name__}")


def modify_employee_profile(
    worker: Dict[str, Any],
    changes: Dict[str, Any],
    is_privileged: bool,
) -> Dict[str, Any]:
    """
    Update an employee profile according to the supplied changes.

    Parameters
    ----------
    worker : dict
        The current employee profile.
    changes : dict
        Mapping of fields to new values that should be applied.
    is_privileged : bool
        ``True`` if the caller has admin rights; otherwise only fields in
        :data:`EDITABLE_FIELDS` may be updated.

    Returns
    -------
    dict
        The modified employee profile.

    Raises
    ------
    TypeError
        If ``worker`` or ``changes`` are not dictionaries.
    ValueError
        If a non‑privileged caller attempts to modify a disallowed field.
    """
    # Basic type checking
    _validate_dict("worker", worker)
    _validate_dict("changes", changes)

    # Make a shallow copy so the original is not mutated unexpectedly
    updated = worker.copy()

    for key, new_value in changes.items():
        # Skip keys that don't exist on the profile
        if key not in worker:
            continue

        # Enforce editable field restrictions for non‑privileged users
        if not is_privileged and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Field '{key}' cannot be modified by a non‑admin user."
            )

        updated[key] = new_value

    return updated