from __future__ import annotations

# Example data structures – replace with real data in production
USERS = {
    1: {"role": "admin", "subscription": None},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
}

CONTENT = {
    101: {"title": "Intro to Python", "required_subscription": "basic"},
    102: {"title": "Advanced AI", "required_subscription": "premium"},
    103: {"title": "Admin Secrets", "required_subscription": None},
}


def access_content(current_user_id: int, content_id: int) -> str | dict:
    """
    Return the requested content if the user is authorized, otherwise return 'Access Denied'.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to access content.
    content_id : int
        The ID of the content being accessed.

    Returns
    -------
    dict | str
        Content data if authorized, otherwise 'Access Denied'.
    """
    # Validate input types early
    if not isinstance(current_user_id, int) or not isinstance(content_id, int):
        return "Access Denied"

    user = USERS.get(current_user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(content_id)
    if not content:
        return "Access Denied"

    # Admins bypass subscription checks
    if user.get("role") == "admin":
        return content

    # Regular users must have a matching subscription
    required = content.get("required_subscription")
    if required is None:
        # Content with no subscription requirement is open to all users
        return content

    if user.get("subscription") == required:
        return content

    return "Access Denied"