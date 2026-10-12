# -*- coding: utf-8 -*-

"""
Content access module.

This module defines a simple permission system that determines whether
a user is allowed to view a particular piece of content based on their
role and subscription level.

The data structures below are placeholders; in a real application they
would be populated from a database or external service.
"""

# --------------------------------------------------------------------------- #
# Sample data – in practice these would come from a database or external API
# --------------------------------------------------------------------------- #

USERS = {
    1: {"role": "admin",   "subscription_level": "premium"},
    2: {"role": "user",    "subscription_level": "basic"},
    3: {"role": "user",    "subscription_level": "premium"},
    4: {"role": "guest",   "subscription_level": None},
}

CONTENT = {
    101: {"title": "Advanced Python",      "required_level": "premium"},
    102: {"title": "Intro to Programming", "required_level": "basic"},
    103: {"title": "Guest Guide",          "required_level": None},
}

# --------------------------------------------------------------------------- #
# Utility functions
# --------------------------------------------------------------------------- #

def _normalize_role(role: str) -> str:
    """
    Normalize role strings to lowercase for consistent comparison.
    """
    return role.strip().lower()

def _has_permission(user: dict, content: dict) -> bool:
    """
    Determine if a user has permission to view the content.
    Admins always have access. Regular users must have at least the
    required subscription level.
    """
    if _normalize_role(user.get("role", "")) == "admin":
        return True

    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    # If content has no level requirement, anyone can view it
    if required_level is None:
        return True

    # Basic policy: user level must match or exceed required level.
    # For simplicity, we consider "premium" > "basic".
    hierarchy = {"basic": 1, "premium": 2}
    user_rank = hierarchy.get(user_level, 0)
    required_rank = hierarchy.get(required_level, 0)

    return user_rank >= required_rank

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def view_content(uid: int, cont_id: int) -> str:
    """
    Return the title of the requested content if the user has access.
    Otherwise, return 'Access Denied'.

    Parameters
    ----------
    uid : int
        The user ID attempting to access the content.
    cont_id : int
        The content ID being requested.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Validate input types
    if not isinstance(uid, int) or not isinstance(cont_id, int):
        raise TypeError("uid and cont_id must be integers")

    # Retrieve user and content records
    user = USERS.get(uid)
    content = CONTENT.get(cont_id)

    # Missing user or content – treat as denied
    if not user or not content:
        return "Access Denied"

    # Check permissions
    if _has_permission(user, content):
        return content["title"]
    else:
        return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    print(view_content(1, 101))  # Admin → Advanced Python
    print(view_content(2, 101))  # Basic user → Access Denied
    print(view_content(3, 102))  # Premium user → Intro to Programming
    print(view_content(4, 103))  # Guest → Guest Guide