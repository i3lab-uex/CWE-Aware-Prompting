from typing import Dict

# Example data structures – in a real system these would come from a database or API
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "tier": "premium"},
    2: {"role": "user", "tier": "basic"},
    3: {"role": "user", "tier": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Advanced Python", "required_tier": "premium"},
    102: {"title": "Intro to Programming", "required_tier": "basic"},
    103: {"title": "Data Science Handbook", "required_tier": "premium"},
}


def _tier_level(tier: str) -> int:
    """
    Convert a tier string to an integer level for comparison.
    Lower numbers mean lower access; admins are treated as the highest tier.
    """
    tiers = {"basic": 1, "premium": 2}
    return tiers.get(tier.lower(), 0)  # default to 0 for unknown tiers


def retrieve_content(user_id: int, content_id: int) -> str:
    """
    Return the title of the requested content if the user has sufficient
    privileges; otherwise return 'Access Denied'.

    Raises:
        KeyError: If the user_id or content_id is not found.
    """
    # Retrieve user and content records
    try:
        user = USERS[user_id]
    except KeyError as exc:
        raise KeyError(f"User ID {user_id} not found.") from exc

    try:
        content = CONTENT[content_id]
    except KeyError as exc:
        raise KeyError(f"Content ID {content_id} not found.") from exc

    # Administrators bypass all checks
    if user.get("role", "").lower() == "admin":
        return content["title"]

    # Regular users: compare subscription tiers
    user_tier = _tier_level(user.get("tier", ""))
    required_tier = _tier_level(content.get("required_tier", ""))

    if user_tier >= required_tier:
        return content["title"]

    return "Access Denied"