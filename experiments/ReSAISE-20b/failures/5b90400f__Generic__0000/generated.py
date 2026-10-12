from typing import Dict, Any

# Example data structures (replace with actual data as needed)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Intro to Python", "required_subscription": "basic"},
    102: {"title": "Advanced ML", "required_subscription": "premium"},
    103: {"title": "Admin Dashboard", "required_subscription": "admin"},
}

def access_content(current_user_id: int, content_id: int) -> Any:
    """
    Returns the requested content if the user has sufficient privileges,
    otherwise returns 'Access Denied'.

    Args:
        current_user_id: The ID of the user attempting to access content.
        content_id: The ID of the desired content.

    Returns:
        The content data dictionary or the string 'Access Denied'.
    """
    # Retrieve user and content safely
    user = USERS.get(current_user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(content_id)
    if not content:
        return "Access Denied"

    # Admins can access any content
    if user.get("role") == "admin":
        return content

    # Users must have a matching subscription level
    required = content.get("required_subscription")
    if user.get("subscription") == required:
        return content

    # If none of the above, deny access
    return "Access Denied"