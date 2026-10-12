# -*- coding: utf-8 -*-

# Sample data for demonstration. In a real application these would come from a database.
USERS = {
    1: {"role": "admin", "subscription": None},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
}

CONTENT = {
    101: {"title": "Basic Article", "data": "Content for basic subscribers.", "required_subscription": "basic"},
    102: {"title": "Premium Video", "data": "Content for premium subscribers.", "required_subscription": "premium"},
    103: {"title": "Admin Report", "data": "Sensitive admin data.", "required_subscription": None},
}


def access_content(current_user_id: int, content_id: int):
    """
    Return the content data if the user is authorized to view it, else return 'Access Denied'.

    Parameters
    ----------
    current_user_id : int
        The user_id of the actor attempting to access content.
    content_id : int
        The identifier of the content being accessed.

    Returns
    -------
    str
        The content data if authorized, otherwise 'Access Denied'.
    """
    # Retrieve user and content records safely
    user = USERS.get(current_user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(content_id)
    if not content:
        return "Access Denied"

    # Admins have unrestricted access
    if user.get("role") == "admin":
        return content["data"]

    # Non-admins must match the required subscription level
    required = content.get("required_subscription")
    if required is None:
        # Content that does not require a subscription (public)
        return content["data"]

    if user.get("subscription") == required:
        return content["data"]

    # If none of the conditions are met, deny access
    return "Access Denied"