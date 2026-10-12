# -*- coding: utf-8 -*-
"""
Access control module.
"""

from typing import Dict, Tuple

# --------------------------------------------------------------------------- #
# Sample data (would normally come from a database or external source)
# --------------------------------------------------------------------------- #

USERS: Dict[int, Tuple[str, int]] = {
    # user_id : (role, subscription_level)
    1: ("admin", 0),          # Admins have level 0 (unrestricted)
    2: ("user", 1),           # Basic subscriber
    3: ("user", 2),           # Premium subscriber
}

CONTENT: Dict[int, Tuple[str, int]] = {
    # content_id : (title, required_subscription_level)
    101: ("Public Article", 0),          # Accessible to all
    102: ("Basic Tutorial", 1),          # Requires basic subscription
    103: ("Premium Guide", 2),           # Requires premium subscription
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def grant_access(user_id: int, item_id: int) -> str:
    """
    Return the title of a content item if the user is allowed to access it.
    Otherwise return 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the user attempting to access content.
    item_id : int
        Identifier of the requested content.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise 'Access Denied'.

    Notes
    -----
    - Admin users (role == 'admin') bypass subscription checks.
    - Subscription levels are compared numerically: higher level includes all lower ones.
    """
    # Validate input types to avoid accidental misuse
    if not isinstance(user_id, int) or not isinstance(item_id, int):
        return "Access Denied"

    # Retrieve user data safely
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    role, user_level = user

    # Retrieve content data safely
    content = CONTENT.get(item_id)
    if not content:
        return "Access Denied"

    title, required_level = content

    # Admins have unrestricted access
    if role.lower() == "admin":
        return title

    # Regular users: check subscription level
    if user_level >= required_level:
        return title

    # Default case: deny access
    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (would normally be in a separate test module)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Should return the title
    print(grant_access(1, 102))   # Admin accessing premium content
    print(grant_access(2, 101))   # Basic user accessing public article

    # Should deny access
    print(grant_access(2, 103))   # Basic user trying to access premium guide
    print(grant_access(999, 101)) # Non‑existent user