# view_content.py

"""
Provides a function to retrieve content titles based on user permissions.

The USERS dictionary maps a user ID to a dictionary containing the user's role
and subscription level. The CONTENT dictionary maps a content ID to a
dictionary with the required subscription level and title.

The function view_content(uid, cont_id) returns the content title if the user
has sufficient permissions; otherwise it returns 'Access Denied'.
"""

# Example data – replace with real data or import from your database.
USERS = {
    1: {"role": "admin", "subscription_level": None},
    2: {"role": "user", "subscription_level": 1},
    3: {"role": "user", "subscription_level": 2},
}

CONTENT = {
    101: {"required_level": 1, "title": "Beginner Guide"},
    102: {"required_level": 2, "title": "Advanced Tutorial"},
    103: {"required_level": 3, "title": "Expert Secrets"},
}

def view_content(uid: int, cont_id: int) -> str:
    """
    Return the title of the requested content if the user has permission.
    
    Parameters
    ----------
    uid : int
        The ID of the user requesting access.
    cont_id : int
        The ID of the content to be accessed.

    Returns
    -------
    str
        Content title if access is granted, otherwise 'Access Denied'.

    Raises
    ------
    ValueError
        If the user ID or content ID does not exist.
    """
    # Validate existence of user and content
    if uid not in USERS:
        raise ValueError(f"User ID {uid} does not exist.")
    if cont_id not in CONTENT:
        raise ValueError(f"Content ID {cont_id} does not exist.")

    user = USERS[uid]
    content = CONTENT[cont_id]

    # Administrators bypass subscription checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users: subscription level must be >= required level
    user_level = user.get("subscription_level")
    if user_level is None:
        # Should not happen for non-admins, but guard anyway
        return "Access Denied"

    required_level = content.get("required_level")
    if user_level >= required_level:
        return content["title"]

    return "Access Denied"