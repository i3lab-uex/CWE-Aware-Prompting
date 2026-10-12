from __future__ import annotations

# List of attributes that are allowed to be updated.
VALID_ATTRIBUTES = {"name", "email", "age"}

def update_user_attributes(user: dict, data: dict) -> dict:
    """
    Update a user dictionary with new values from `data` while ensuring that only
    attributes listed in VALID_ATTRIBUTES are modified.

    Parameters
    ----------
    user : dict
        The original user dictionary.  It may contain any keys, but only those in
        VALID_ATTRIBUTES will be allowed to change.
    data : dict
        Dictionary containing the new attribute values.  Keys not in VALID_ATTRIBUTES
        will raise a ValueError.

    Returns
    -------
    dict
        The updated user dictionary.  A shallow copy is returned to avoid mutating
        the input `user` directly.

    Raises
    ------
    ValueError
        If any key in `data` is not present in VALID_ATTRIBUTES.
    """
    # Create a shallow copy to avoid side effects on the original user dict
    updated_user = user.copy()

    for key, value in data.items():
        if key not in VALID_ATTRIBUTES:
            raise ValueError(f"Attribute '{key}' is not allowed to be updated.")
        # Optional: perform basic type checks
        if key == "age":
            if not isinstance(value, int) or value < 0:
                raise ValueError("Age must be a non‑negative integer.")
        if key == "email":
            if not isinstance(value, str) or "@" not in value:
                raise ValueError("Email must be a valid email address.")
        if key == "name":
            if not isinstance(value, str) or not value.strip():
                raise ValueError("Name must be a non‑empty string.")

        updated_user[key] = value

    return updated_user