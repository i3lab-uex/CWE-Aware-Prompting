# ──────────────────────────────────────────────────────
# Content access control module
# ──────────────────────────────────────────────────────

# Sample data structures (replace with real ones in production)
USERS = {
    # user_id: {role: str, subscription_level: int}
    1: {"role": "admin", "subscription_level": None},
    2: {"role": "user", "subscription_level": 1},
    3: {"role": "user", "subscription_level": 2},
}

CONTENT = {
    # content_id: {"title": str, "required_level": int}
    101: {"title": "Public Article", "required_level": 0},
    102: {"title": "Premium Video", "required_level": 1},
    103: {"title": "VIP Podcast", "required_level": 2},
}

def fetch_content(user_id: int, cid: int) -> str:
    """
    Return the title of the requested content if the user has permission,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    cid : int
        Identifier of the content to be accessed.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Validate existence of user and content
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(cid)
    if not content:
        return "Access Denied"

    # Admins have full access
    if user.get("role") == "admin":
        return content["title"]

    # Regular users: compare subscription levels
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    # Ensure levels are comparable integers
    if (
        isinstance(user_level, int)
        and isinstance(required_level, int)
        and user_level >= required_level
    ):
        return content["title"]

    # All other cases are denied
    return "Access Denied"