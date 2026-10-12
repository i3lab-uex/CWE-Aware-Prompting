# Global dictionary of attributes that are allowed to be updated
VALID_ATTRIBUTES = {"name", "email", "age"}

def update_user_attributes(user: dict, data: dict) -> dict:
    """
    Update a user dictionary with new attribute values.

    Parameters
    ----------
    user : dict
        Original user data.  This dictionary will not be modified.
    data : dict
        Keys and values to update in the user.  Only keys that exist in
        VALID_ATTRIBUTES are accepted.

    Returns
    -------
    dict
        A new dictionary containing the updated user data.

    Raises
    ------
    ValueError
        If ``data`` contains a key that is not in VALID_ATTRIBUTES.
    TypeError
        If either ``user`` or ``data`` is not a dictionary.
    """
    # Validate argument types
    if not isinstance(user, dict):
        raise TypeError("user must be a dictionary")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    # Make a shallow copy to avoid mutating the original user
    updated_user = user.copy()

    # Process each key/value pair in data
    for key, value in data.items():
        if key not in VALID_ATTRIBUTES:
            raise ValueError(f"Attribute '{key}' is not allowed to be updated.")
        # Update the copy
        updated_user[key] = value

    return updated_user