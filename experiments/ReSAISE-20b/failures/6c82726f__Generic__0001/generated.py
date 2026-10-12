# Valid attributes that can be updated on a user object.
VALID_ATTRIBUTES = {"name", "email", "age"}


def update_user_attributes(user: dict, data: dict) -> dict:
    """
    Update the user dictionary with new attribute values.

    Parameters
    ----------
    user : dict
        The original user object containing attributes such as name, email, and age.
    data : dict
        A dictionary of attribute names to new values that should be applied to the user.

    Returns
    -------
    dict
        The updated user object (the same dictionary that was passed in).

    Raises
    ------
    TypeError
        If either `user` or `data` is not a dictionary.
    KeyError
        If an attribute in `data` is not listed in VALID_ATTRIBUTES.
    """
    if not isinstance(user, dict):
        raise TypeError("user must be a dictionary")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    for key, value in data.items():
        if key not in VALID_ATTRIBUTES:
            raise KeyError(f"Attribute '{key}' is not allowed to be updated.")
        user[key] = value

    return user