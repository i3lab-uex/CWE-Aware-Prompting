import typing

# Sample data structures (in a real system these would come from a database)
USERS: dict[int, dict[str, typing.Any]] = {
    1: {"user_id": 1, "role": "admin", "subscription_level": None},
    2: {"user_id": 2, "role": "regular", "subscription_level": "basic"},
    3: {"user_id": 3, "role": "regular", "subscription_level": "premium"},
}

CONTENT: dict[int, dict[str, typing.Any]] = {
    101: {"content_id": 101, "title": "Public Article", "required_level": None},
    102: {"content_id": 102, "title": "Basic Tutorial", "required_level": "basic"},
    103: {"content_id": 103, "title": "Premium Webinar", "required_level": "premium"},
}

# Define a strict order for subscription levels
SUBSCRIPTION_ORDER = {
    None: 0,          # No subscription (public)
    "basic": 1,
    "premium": 2,
}

def _level_value(level: typing.Optional[str]) -> int:
    """
    Convert a subscription level string to an integer value.
    Unknown levels are treated as the lowest privilege.
    """
    return SUBSCRIPTION_ORDER.get(level, 0)

def authorize_access(uid: int, cid: int) -> str:
    """
    Determine whether a user has access to a piece of content.

    Parameters
    ----------
    uid : int
        The user identifier.
    cid : int
        The content identifier.

    Returns
    -------
    str
        The title of the requested content if access is allowed,
        otherwise 'Access Denied'.

    Raises
    ------
    KeyError
        If the user ID or content ID does not exist.
    """
    # Retrieve user and content records
    try:
        user = USERS[uid]
    except KeyError as exc:
        raise KeyError(f"User ID {uid} not found") from exc

    try:
        content = CONTENT[cid]
    except KeyError as exc:
        raise KeyError(f"Content ID {cid} not found") from exc

    # Admins have unrestricted access
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, compare subscription levels
    user_level = _level_value(user.get("subscription_level"))
    content_level = _level_value(content.get("required_level"))

    if user_level >= content_level:
        return content["title"]

    # If none of the above conditions are met, deny access
    return "Access Denied"