from typing import Dict, Any

# Example data structures (replace with actual data in real usage)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"user_id": 1, "role": "admin", "subscription_level": None},
    2: {"user_id": 2, "role": "user", "subscription_level": 1},
    3: {"user_id": 3, "role": "user", "subscription_level": 2},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Basic Article", "required_level": 0},
    102: {"title": "Premium Video", "required_level": 1},
    103: {"title": "Exclusive Report", "required_level": 2},
}


def fetch_content(given_user_id: int, target_content_id: int) -> str:
    """
    Return the title of the requested content if the user is allowed to access it.
    Admins have unrestricted access. Regular users can only access content whose
    required subscription level is less than or equal to their own level.

    Parameters:
        given_user_id (int): ID of the user attempting access.
        target_content_id (int): ID of the content being requested.

    Returns:
        str: The content title if access is granted, otherwise 'Access Denied'.
    """
    # Validate user
    user = USERS.get(given_user_id)
    if not user:
        return "Access Denied"

    # Validate content
    content = CONTENT.get(target_content_id)
    if not content:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must meet subscription level requirement
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    # Ensure subscription levels are integers for comparison
    if not isinstance(user_level, int) or not isinstance(required_level, int):
        return "Access Denied"

    if user_level >= required_level:
        return content["title"]

    return "Access Denied"