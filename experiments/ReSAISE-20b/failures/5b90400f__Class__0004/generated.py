from typing import Dict, Any

# Example data structures (replace with actual data in production)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_level": None},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"required_subscription": "basic", "data": "Basic content"},
    102: {"required_subscription": "premium", "data": "Premium content"},
    103: {"required_subscription": "basic", "data": "Another basic content"},
}


def access_content(current_user_id: int, content_id: int) -> Any:
    """
    Return the requested content data if the user is authorized.
    Admins can access any content. Regular users may only view
    content that matches their subscription level.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to access content.
    content_id : int
        The ID of the content being accessed.

    Returns
    -------
    Any
        The content data if authorized, otherwise the string 'Access Denied'.
    """
    # Validate that user exists
    user = USERS.get(current_user_id)
    if not user:
        return "Access Denied"

    # Validate that content exists
    content = CONTENT.get(content_id)
    if not content:
        return "Access Denied"

    # Admins bypass subscription checks
    if user.get("role") == "admin":
        return content["data"]

    # Regular users must have matching subscription level
    user_sub = user.get("subscription_level")
    required_sub = content.get("required_subscription")

    if user_sub == required_sub:
        return content["data"]

    # If subscription does not match or is missing, deny access
    return "Access Denied"