import typing as _t

# Example data structures; in real usage these would be populated elsewhere.
USERS: dict[int, dict[str, _t.Any]] = {
    # user_id: {role: str, tier: str}
    1: {"role": "admin", "tier": "gold"},
    2: {"role": "user", "tier": "silver"},
    3: {"role": "user", "tier": "bronze"},
}

CONTENT: dict[int, dict[str, _t.Any]] = {
    # content_id: {title: str, required_tier: str}
    101: {"title": "Advanced Python", "required_tier": "gold"},
    102: {"title": "Intermediate C++", "required_tier": "silver"},
    103: {"title": "Intro to JavaScript", "required_tier": "bronze"},
}


def get_content(active_user_id: int, item_id: int) -> str:
    """
    Return the title of a content item if the user has permission, otherwise
    return 'Access Denied'.

    Parameters
    ----------
    active_user_id : int
        The ID of the user attempting to access content.
    item_id : int
        The ID of the requested content.

    Returns
    -------
    str
        Content title if access is granted, otherwise 'Access Denied'.

    Raises
    ------
    KeyError
        If the user or content item is not found in the respective dictionaries.
    """
    # Validate input types (basic security check)
    if not isinstance(active_user_id, int) or not isinstance(item_id, int):
        raise TypeError("Both active_user_id and item_id must be integers.")

    # Retrieve user and content data
    try:
        user = USERS[active_user_id]
    except KeyError as exc:
        raise KeyError(f"User ID {active_user_id} not found.") from exc

    try:
        content = CONTENT[item_id]
    except KeyError as exc:
        raise KeyError(f"Content ID {item_id} not found.") from exc

    # Administrators bypass tier checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must meet or exceed the required tier
    user_tier = user.get("tier")
    required_tier = content.get("required_tier")

    # Define tier hierarchy for comparison
    tier_order = {"bronze": 1, "silver": 2, "gold": 3}
    user_rank = tier_order.get(user_tier, 0)
    required_rank = tier_order.get(required_tier, 0)

    if user_rank >= required_rank:
        return content["title"]

    return "Access Denied"