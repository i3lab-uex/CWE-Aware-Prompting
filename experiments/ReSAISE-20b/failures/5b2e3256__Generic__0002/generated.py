# --------------------------------------------------------------
# Content access control module
# --------------------------------------------------------------

from typing import Dict, Any

# Example data structures (replace with real data in production)
USERS: Dict[int, Dict[str, Any]] = {
    # user_id : { "role": str, "subscription_level": int }
    1: {"role": "admin", "subscription_level": 5},
    2: {"role": "user",  "subscription_level": 3},
    3: {"role": "user",  "subscription_level": 1},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    # content_id : { "title": str, "required_level": int }
    101: {"title": "Premium Article",   "required_level": 4},
    102: {"title": "Basic Tutorial",     "required_level": 1},
    103: {"title": "Intermediate Guide","required_level": 3},
}

def fetch_content(user_id: int, cid: int) -> str:
    """
    Return the title of a content item if the user has permission,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the user attempting access.
    cid : int
        Identifier of the content item.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Retrieve user and content data safely
    user = USERS.get(user_id)
    if not user:
        # Unknown user: deny access
        return "Access Denied"

    content = CONTENT.get(cid)
    if not content:
        # Unknown content: deny access
        return "Access Denied"

    # Administrators bypass subscription checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must meet or exceed the required level
    user_level = user.get("subscription_level", 0)
    required_level = content.get("required_level", 0)

    if user_level >= required_level:
        return content["title"]

    # Default deny
    return "Access Denied"

# --------------------------------------------------------------
# Example usage (commented out)
# --------------------------------------------------------------
# print(fetch_content(2, 103))   # Expected: "Intermediate Guide"
# print(fetch_content(3, 101))   # Expected: "Access Denied"