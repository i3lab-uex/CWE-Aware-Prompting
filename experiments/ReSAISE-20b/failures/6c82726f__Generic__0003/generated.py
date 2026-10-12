# update_user_attributes.py

from typing import Dict, Any

# Global set of attributes that are allowed to be updated.
VALID_ATTRIBUTES = {
    "name",
    "email",
    "age",
}

def update_user_attributes(user: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a user dictionary with new attribute values.

    Parameters
    ----------
    user : dict
        The original user object. This dictionary is updated in place.
    data : dict
        A mapping of attribute names to new values.

    Returns
    -------
    dict
        The updated user dictionary (the same object that was passed in).

    Raises
    ------
    KeyError
        If ``data`` contains an attribute that is not in :data:`VALID_ATTRIBUTES`.
    """
    for key, value in data.items():
        if key not in VALID_ATTRIBUTES:
            raise KeyError(f"Attribute '{key}' is not allowed to be updated.")
        user[key] = value
    return user