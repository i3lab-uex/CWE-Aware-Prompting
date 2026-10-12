# ------------------------------------------------------------
# Content retrieval based on user role and subscription level
# ------------------------------------------------------------

from typing import Dict, List

# ------------------------------------------------------------------
# Example data structures – in a real system these would be loaded
# from a database or configuration file.
# ------------------------------------------------------------------
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "standard"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Intro to Python", "required_subscription": "basic"},
    102: {"title": "Advanced AI", "required_subscription": "standard"},
    103: {"title": "Enterprise Security", "required_subscription": "premium"},
}

# The hierarchy defines the order of subscription levels
subscription_hierarchy: List[str] = ["basic", "standard", "premium"]


def _subscription_rank(level: str) -> int:
    """
    Return the index of a subscription level in the hierarchy.
    Lower index means lower level. Raises ValueError if unknown level.
    """
    try:
        return subscription_hierarchy.index(level)
    except ValueError as exc:
        raise ValueError(f"Unknown subscription level: {level}") from exc


def retrieve_content(usr_id: int, contid: int) -> str:
    """
    Return the title of a content item if the user has permission,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    usr_id : int
        Identifier of the user attempting to access content.
    contid : int
        Identifier of the requested content.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise 'Access Denied'.

    Raises
    ------
    KeyError
        If the user or content ID does not exist.
    ValueError
        If an unknown subscription level is encountered.
    """
    # Retrieve user and content data; let KeyError propagate for missing IDs
    user = USERS[usr_id]
    content = CONTENT[contid]

    # Admins have unrestricted access
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, check subscription level
    user_level = user.get("subscription")
    required_level = content.get("required_subscription")

    # Ensure both levels are valid
    user_rank = _subscription_rank(user_level)
    required_rank = _subscription_rank(required_level)

    # Grant access if user's level is equal or higher than required
    return content["title"] if user_rank >= required_rank else "Access Denied"