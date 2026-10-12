# Define the user and content data structures.
USERS = {
    1: {"role": "admin", "subscription_tier": None},
    2: {"role": "user", "subscription_tier": "basic"},
    3: {"role": "user", "subscription_tier": "premium"},
    # Add more users as needed.
}

CONTENT = {
    101: {"title": "Basic Tutorial", "required_tier": "basic"},
    102: {"title": "Premium Guide", "required_tier": "premium"},
    103: {"title": "Admin Manual", "required_tier": None},
    # Add more content as needed.
}

def retrieve_content(user_id: int, content_id: int) -> str:
    """
    Return the title of the requested content if the user has permission.
    
    Parameters
    ----------
    user_id : int
        The identifier of the user attempting to access content.
    content_id : int
        The identifier of the content the user is trying to access.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise 'Access Denied'.
    """
    # Retrieve user and content records safely.
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(content_id)
    if not content:
        return "Access Denied"

    # Administrators bypass all checks.
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, compare subscription tiers.
    user_tier = user.get("subscription_tier")
    required_tier = content.get("required_tier")

    # If the content has no tier requirement, allow access.
    if required_tier is None:
        return content["title"]

    # Grant access only when tiers match.
    if user_tier == required_tier:
        return content["title"]

    # All other cases result in denial.
    return "Access Denied"