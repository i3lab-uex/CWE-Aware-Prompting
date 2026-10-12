# -*- coding: utf-8 -*-
"""
Utility to safely update user attributes.

The global `VALID_ATTRIBUTES` dictionary defines the set of fields that
are allowed to be modified.  The function `update_user_attributes` takes a
user dictionary and an incoming data dictionary, updates only the valid
attributes, performs basic validation (e.g. age must be a non‑negative int),
and returns the modified user dictionary.

The implementation is defensive: it does not mutate the original data
structures unless they are explicitly passed in, and it raises clear
exceptions when invalid input is encountered.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, Mapping

# Define the attributes that can be updated.
VALID_ATTRIBUTES: set[str] = {"name", "email", "age"}


def _validate_attribute(name: str, value: Any) -> None:
    """
    Validate a single attribute value.

    Parameters
    ----------
    name : str
        The attribute name.
    value : Any
        The new value to assign.

    Raises
    ------
    TypeError
        If the type of ``value`` is inappropriate for the attribute.
    ValueError
        If the value violates a business rule (e.g. negative age).
    """
    if name == "name":
        if not isinstance(value, str):
            raise TypeError(f"Attribute 'name' must be a string, got {type(value).__name__}")
        if not value:
            raise ValueError("Attribute 'name' cannot be empty")

    elif name == "email":
        if not isinstance(value, str):
            raise TypeError(f"Attribute 'email' must be a string, got {type(value).__name__}")
        if "@" not in value:
            raise ValueError("Attribute 'email' must contain '@'")

    elif name == "age":
        if not isinstance(value, int):
            raise TypeError(f"Attribute 'age' must be an integer, got {type(value).__name__}")
        if value < 0:
            raise ValueError("Attribute 'age' cannot be negative")


def update_user_attributes(user: Mapping[str, Any], data: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Update a user dictionary with validated attributes.

    Parameters
    ----------
    user : Mapping[str, Any]
        The original user data.
    data : Mapping[str, Any]
        A mapping of attribute names to new values.

    Returns
    -------
    dict[str, Any]
        A new dictionary containing the updated user data.

    Raises
    ------
    KeyError
        If an attribute in ``data`` is not allowed to be updated.
    TypeError, ValueError
        If an attribute value fails validation.

    Notes
    -----
    The function does **not** modify the original ``user`` or ``data``
    dictionaries; it returns a new dictionary containing the updated
    values.  This behaviour makes the function safe to use in contexts
    where immutability is desired.
    """
    # Work on a shallow copy of the user to avoid side effects
    updated_user: Dict[str, Any] = copy.deepcopy(user)

    for key, new_value in data.items():
        if key not in VALID_ATTRIBUTES:
            raise KeyError(f"Attribute '{key}' is not allowed to be updated")

        # Validate the new value before applying it
        _validate_attribute(key, new_value)

        updated_user[key] = new_value

    return updated_user