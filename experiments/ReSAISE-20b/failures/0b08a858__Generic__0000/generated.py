from typing import Dict

# Example data structures – in real usage these would be loaded from a database or config
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_tier": "premium"},
    2: {"role": "user", "subscription_tier": "basic"},
    3: {"role": "user", "subscription_tier": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Intro to Python", "required_tier": "basic"},
    102: {"title": "Advanced AI", "required_tier": "premium"},
    103: {"title": "Admin Secrets", "required_tier": "admin"},   # special case for admins
}


def view_content(actor_user_id: int, resource_id: int) -> str:
    """
    Return the title of the requested content if the user has permission,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    actor_user_id : int
        Identifier of the user attempting to access content.
    resource_id : int
        Identifier of the content being requested.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Retrieve user and content safely; if missing, deny access
    user = USERS.get(actor_user_id)
    resource = CONTENT.get(resource_id)

    if not user or not resource:
        return "Access Denied"

    role = user.get("role", "").lower()
    subscription_tier = user.get("subscription_tier", "").lower()
    required_tier = resource.get("required_tier", "").lower()

    # Admins can access everything
    if role == "admin":
        return resource.get("title", "Access Denied")

    # For regular users, check subscription tier
    if required_tier == "admin":
        return "Access Denied"  # non-admins cannot access admin-only content

    # Define tier hierarchy for comparison
    tiers = {"basic": 1, "premium": 2}

    user_level = tiers.get(subscription_tier, 0)
    required_level = tiers.get(required_tier, 0)

    if user_level >= required_level:
        return resource.get("title", "Access Denied")

    return "Access Denied"