# ──────────────────────── Imports ──────────────────────── #
from typing import Dict, Any

# ──────────────────────── Sample Data ──────────────────────── #
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

# Subscription hierarchy (lower value = weaker access)
SUBSCRIPTION_RANK: Dict[str, int] = {
    "none": 0,
    "basic": 1,
    "premium": 2,
    "vip": 3,
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Public Article", "required_level": "none"},
    102: {"title": "Premium Video", "required_level": "premium"},
    103: {"title": "VIP Interview", "required_level": "vip"},
}

# ──────────────────────── Core Function ──────────────────────── #
def grant_access(user_id: int, item_id: int) -> str:
    """
    Determines if a user can access a piece of content.

    Parameters
    ----------
    user_id : int
        Identifier for the requesting user.
    item_id : int
        Identifier for the requested content.

    Returns
    -------
    str
        The title of the content if access is granted; otherwise,
        'Access Denied'.

    Raises
    ------
    KeyError
        If the user_id or item_id does not exist in the respective
        dictionaries.
    """
    # Retrieve user and content safely; raise KeyError if missing
    try:
        user = USERS[user_id]
    except KeyError as exc:
        raise KeyError(f"User ID {user_id} not found") from exc

    try:
        content = CONTENT[item_id]
    except KeyError as exc:
        raise KeyError(f"Content ID {item_id} not found") from exc

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Ensure subscription levels are known
    user_level = SUBSCRIPTION_RANK.get(user.get("subscription_level", "none"))
    required_level = SUBSCRIPTION_RANK.get(content.get("required_level", "none"))

    if user_level is None or required_level is None:
        # Unknown level; deny access for safety
        return "Access Denied"

    # Grant if user's level is equal or higher than required
    if user_level >= required_level:
        return content["title"]

    # Default: deny access
    return "Access Denied"

# ──────────────────────── Example Usage ──────────────────────── #
if __name__ == "__main__":
    # Sample test cases
    print(grant_access(1, 103))  # Admin: VIP Interview
    print(grant_access(2, 102))  # Basic user: Premium Video → Access Denied
    print(grant_access(3, 102))  # Premium user: Premium Video → Premium Video