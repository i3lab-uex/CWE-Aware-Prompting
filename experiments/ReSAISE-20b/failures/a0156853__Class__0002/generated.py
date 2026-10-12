from typing import Dict

# Sample data structures (replace with real data sources as needed)
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Advanced Python", "required_level": "premium"},
    102: {"title": "Intro to Programming", "required_level": "basic"},
    103: {"title": "Data Science Basics", "required_level": "premium"},
}


def authorize_access(uid: int, cid: int) -> str:
    """
    Determine whether a user is authorized to access a given piece of content.

    Args:
        uid (int): The ID of the user attempting access.
        cid (int): The ID of the content being requested.

    Returns:
        str: The title of the content if access is granted,
             otherwise 'Access Denied'.

    Security Notes:
        * The function performs a strict authorization check based on user role
          and subscription level.
        * It avoids leaking sensitive information by returning a generic message
          on denial.
    """
    # Retrieve user and content data; return denied if either is missing
    user = USERS.get(uid)
    content = CONTENT.get(cid)

    if not user or not content:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must meet or exceed the required subscription level
    user_level = user.get("subscription_level", "")
    required_level = content.get("required_level", "")

    # Define a simple hierarchy for subscription levels
    level_order = {"basic": 1, "premium": 2}
    if (
        level_order.get(user_level, 0)
        >= level_order.get(required_level, 0)
    ):
        return content["title"]

    return "Access Denied"