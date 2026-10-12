# view_content.py

USERS = {
    # Example structure: user_id -> {role: str, tier: int}
    1: {"role": "admin", "tier": 3},
    2: {"role": "user", "tier": 1},
    3: {"role": "user", "tier": 2},
}

CONTENT = {
    # Example structure: content_id -> {title: str, required_tier: int}
    101: {"title": "Basic Tutorial", "required_tier": 1},
    102: {"title": "Advanced Guide", "required_tier": 2},
    103: {"title": "Premium Workshop", "required_tier": 3},
}


def view_content(actor_user_id: int, resource_id: int) -> str:
    """
    Return the title of the requested content if the user has access.
    Administrators have unrestricted access. Regular users may only view
    content that matches or is below their subscription tier.

    Parameters
    ----------
    actor_user_id : int
        Identifier of the user attempting to access content.
    resource_id : int
        Identifier of the content being requested.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise
        'Access Denied'.

    Notes
    -----
    - The function is defensive: if either the user or content id does not exist,
      it returns 'Access Denied' instead of raising an exception.
    - User roles are case-insensitive. Any role other than 'admin' is treated
      as a regular user.
    """
    # Retrieve user and content safely
    user = USERS.get(actor_user_id)
    content = CONTENT.get(resource_id)

    if not user or not content:
        return "Access Denied"

    # Normalise role for case-insensitive comparison
    role = user.get("role", "").lower()
    if role == "admin":
        return content["title"]

    # Regular user: check subscription tier
    user_tier = user.get("tier")
    required_tier = content.get("required_tier")

    # If either tier is missing, deny access
    if user_tier is None or required_tier is None:
        return "Access Denied"

    if user_tier >= required_tier:
        return content["title"]

    return "Access Denied"


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    print(view_content(1, 103))  # Admin accessing premium content
    print(view_content(2, 102))  # Regular user with tier 1 accessing tier 2 content