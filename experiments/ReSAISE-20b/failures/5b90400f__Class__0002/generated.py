# Access control implementation for content retrieval

USERS = {
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
}

CONTENT = {
    101: {"data": "Basic Content A", "required_subscription": "basic"},
    102: {"data": "Premium Content B", "required_subscription": "premium"},
    103: {"data": "Basic Content C", "required_subscription": "basic"},
}


def access_content(current_user_id: int, content_id: int) -> str:
    """
    Return the content data if the user is authorized, otherwise return 'Access Denied'.

    Args:
        current_user_id (int): ID of the user attempting to access content.
        content_id (int): ID of the content being accessed.

    Returns:
        str: The content data or 'Access Denied'.
    """
    # Fetch user and content safely
    user = USERS.get(current_user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(content_id)
    if not content:
        return "Access Denied"

    # Admins have unrestricted access
    if user.get("role") == "admin":
        return content["data"]

    # Regular users: check subscription match
    required_sub = content.get("required_subscription")
    if user.get("subscription") == required_sub:
        return content["data"]

    # No match -> deny access
    return "Access Denied"