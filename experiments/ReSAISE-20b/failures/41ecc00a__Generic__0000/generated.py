import functools

# Example data structures (replace with actual data in production)
USERS = {
    1: {"role": "admin", "tier": "premium"},
    2: {"role": "user", "tier": "free"},
    3: {"role": "user", "tier": "premium"},
}

CONTENT = {
    101: {"title": "Basic Guide", "required_tier": "free"},
    102: {"title": "Premium Tips", "required_tier": "premium"},
    103: {"title": "Admin Manual", "required_tier": "admin"},
}


def _get_user(user_id: int) -> dict | None:
    """Retrieve user record securely."""
    return USERS.get(user_id)


def _get_content(content_id: int) -> dict | None:
    """Retrieve content record securely."""
    return CONTENT.get(content_id)


def retrieve_content(user_id: int, content_id: int) -> str:
    """
    Return the title of the requested content if the user has permission,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the user attempting to access content.
    content_id : int
        Identifier of the content the user wants to access.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    user = _get_user(user_id)
    content = _get_content(content_id)

    # If either user or content is missing, deny access silently
    if not user or not content:
        return "Access Denied"

    # Admins can access all content
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, check subscription tier
    required = content.get("required_tier")
    if required == user.get("tier"):
        return content["title"]

    # If the content requires admin level, deny regular users
    if required == "admin":
        return "Access Denied"

    # Default denial
    return "Access Denied"


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    print(retrieve_content(1, 102))  # Admin accessing premium content
    print(retrieve_content(2, 101))  # Free user accessing free content
    print(retrieve_content(2, 102))  # Free user denied premium content