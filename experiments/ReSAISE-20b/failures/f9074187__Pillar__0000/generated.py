# Define user and content data structures
USERS = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
    # Add more users as needed
}

CONTENT = {
    101: {"title": "Basic Tutorial", "required_level": "basic"},
    102: {"title": "Premium Guide", "required_level": "premium"},
    # Add more content items as needed
}

# Define the hierarchy of subscription levels for comparison
SUBSCRIPTION_HIERARCHY = {
    "basic": 1,
    "premium": 2,
}

def grant_access(user_id: int, item_id: int) -> str:
    """
    Returns the content title if the user is permitted to access it;
    otherwise returns 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the user attempting access.
    item_id : int
        Identifier of the content item.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Validate inputs to prevent type errors and potential injection
    if not isinstance(user_id, int) or not isinstance(item_id, int):
        return "Access Denied"

    # Fetch user and content records
    user = USERS.get(user_id)
    content = CONTENT.get(item_id)

    # If either the user or content does not exist, deny access
    if user is None or content is None:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, compare subscription levels
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    # If any level is missing or invalid, deny access
    if (
        user_level not in SUBSCRIPTION_HIERARCHY or
        required_level not in SUBSCRIPTION_HIERARCHY
    ):
        return "Access Denied"

    # Grant access if user's level is equal or higher than required
    if SUBSCRIPTION_HIERARCHY[user_level] >= SUBSCRIPTION_HIERARCHY[required_level]:
        return content["title"]

    # Otherwise, deny access
    return "Access Denied"