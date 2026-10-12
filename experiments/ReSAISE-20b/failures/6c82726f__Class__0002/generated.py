# Global set of attributes that are allowed to be updated.
VALID_ATTRIBUTES = {"name", "email", "age"}

def update_user_attributes(user: dict, data: dict) -> dict:
    """
    Update a user dictionary with new attribute values from `data`.
    
    Parameters
    ----------
    user : dict
        Dictionary representing a user. Expected to contain keys such as
        'name', 'email', and 'age'.
    data : dict
        Dictionary containing attribute names as keys and the new values.
    
    Returns
    -------
    dict
        A new dictionary containing the updated user data. The original
        `user` dictionary is left untouched.
    
    Raises
    ------
    ValueError
        If `data` contains keys that are not in VALID_ATTRIBUTES.
    
    Notes
    -----
    * The function does **not** execute or evaluate any code present in the
      values of `data`.  It simply copies the values into a new dictionary.
    * This implementation protects against CWE-913 by restricting updates
      to only the attributes listed in VALID_ATTRIBUTES and by avoiding
      any dynamic execution of code.
    """
    
    # Ensure that all keys in data are allowed
    invalid_keys = set(data) - VALID_ATTRIBUTES
    if invalid_keys:
        raise ValueError(f"Attempted to update disallowed attributes: {invalid_keys}")
    
    # Create a shallow copy of the user dict to avoid mutating the original
    updated_user = user.copy()
    
    # Apply the updates
    for key in VALID_ATTRIBUTES:
        if key in data:
            updated_user[key] = data[key]
    
    return updated_user