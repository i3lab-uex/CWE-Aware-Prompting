# Define user and content data structures
USERS = {
    1: {"role": "admin", "subscription_level": None},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT = {
    101: {"title": "Free Article", "required_level": None},
    102: {"title": "Basic Tutorial", "required_level": "basic"},
    103: {"title": "Premium Guide", "required_level": "premium"},
}

def fetch_content(given_user_id: int, target_content_id: int) -> str:
    """
    Return the title of the requested content if the user has sufficient privileges.
    Otherwise return 'Access Denied'.
    
    Parameters:
        given_user_id (int): ID of the user requesting access.
        target_content_id (int): ID of the content to be accessed.
    
    Returns:
        str: Content title or 'Access Denied'.
    """
    # Validate that the user exists
    user = USERS.get(given_user_id)
    if not user:
        return "Access Denied"

    # Validate that the content exists
    content = CONTENT.get(target_content_id)
    if not content:
        return "Access Denied"

    # Admins have unrestricted access
    if user["role"] == "admin":
        return content["title"]

    # Regular users must meet the required subscription level
    required_level = content.get("required_level")
    if required_level is None:
        # Content with no subscription requirement is publicly accessible
        return content["title"]

    user_level = user.get("subscription_level")
    if user_level == required_level:
        return content["title"]

    # If none of the conditions are met, deny access
    return "Access Denied"