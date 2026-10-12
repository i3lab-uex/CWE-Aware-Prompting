from __future__ import annotations

# Global set of attributes that are allowed to be updated.
VALID_ATTRIBUTES = {"name", "email", "age"}

def update_user_attributes(user: dict, data: dict) -> dict:
    """
    Update a user dictionary with values from ``data`` only for attributes
    that are present in :data:`VALID_ATTRIBUTES`.

    Parameters
    ----------
    user :
        Dictionary representing the user object. It is **not** modified in place;
        a new dictionary containing the updated attributes is returned.
    data :
        Dictionary with attribute names as keys and their new values.

    Returns
    -------
    dict
        A new dictionary containing the updated user attributes.  Only keys in
        :data:`VALID_ATTRIBUTES` are considered; all other keys in ``data`` raise a
        :class:`ValueError`.

    Raises
    ------
    ValueError
        If ``data`` contains a key that is not in :data:`VALID_ATTRIBUTES`.
    """
    # Create a shallow copy to avoid mutating the original user dict.
    updated_user = user.copy()

    for key, value in data.items():
        if key not in VALID_ATTRIBUTES:
            raise ValueError(f"Attribute '{key}' is not allowed to be updated.")
        # Basic type validation can be added here if needed.
        updated_user[key] = value

    return updated_user