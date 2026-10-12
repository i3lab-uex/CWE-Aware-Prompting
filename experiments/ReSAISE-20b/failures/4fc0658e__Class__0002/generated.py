# -*- coding: utf-8 -*-
"""
Utility to fetch content titles based on user role and subscription level.

The implementation follows the following rules:
1. Admin users (`role == "admin"`) have unrestricted access to all content.
2. Regular users must possess a subscription level that meets or exceeds the
   requirement of the requested content.
3. If the user or the content does not exist, a KeyError is raised.
4. Any other case results in an "Access Denied" response.

The module contains example data for demonstration purposes.  In a real
deployment the `USERS` and `CONTENT` dictionaries would be populated from
a database or external service.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Example data – replace with real persistence in production
# --------------------------------------------------------------------------- #

USERS = {
    # user_id: {role, subscription_level}
    1: {"role": "admin", "subscription_level": None},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

# subscription levels are ordered; lower string means less privilege
SUBSCRIPTION_ORDER = {
    "basic": 1,
    "premium": 2,
    "gold": 3,
}

CONTENT = {
    # content_id: {title, required_subscription}
    101: {"title": "Intro to Python", "required_subscription": "basic"},
    102: {"title": "Advanced Machine Learning", "required_subscription": "premium"},
    103: {"title": "Enterprise Strategy", "required_subscription": "gold"},
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def _get_subscription_value(level: str | None) -> int:
    """
    Convert a subscription level to an integer rank.
    Admins have the highest possible rank (`float('inf')`).
    """
    if level is None:
        return float("inf")  # Admin
    return SUBSCRIPTION_ORDER.get(level, 0)  # Default to 0 if unknown

def fetch_content(given_user_id: int, target_content_id: int) -> str:
    """
    Return the title of the requested content if the user is authorized.
    
    Parameters
    ----------
    given_user_id : int
        Identifier of the user attempting access.
    target_content_id : int
        Identifier of the desired content.

    Returns
    -------
    str
        The title of the content if access is granted,
        otherwise "Access Denied".

    Raises
    ------
    KeyError
        If the user or content ID is not found in the respective dictionaries.
    """
    # Validate existence of user and content
    try:
        user = USERS[given_user_id]
    except KeyError as exc:
        raise KeyError(f"User ID {given_user_id} not found.") from exc

    try:
        content = CONTENT[target_content_id]
    except KeyError as exc:
        raise KeyError(f"Content ID {target_content_id} not found.") from exc

    # Admins bypass subscription checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must meet or exceed the required subscription level
    user_level = _get_subscription_value(user.get("subscription_level"))
    required_level = _get_subscription_value(content.get("required_subscription"))

    if user_level >= required_level:
        return content["title"]

    # All other cases: access denied
    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # These print statements are for demonstration; remove or guard with
    # if __debug__ in production code.
    print(fetch_content(1, 101))  # Admin: access granted
    print(fetch_content(2, 102))  # Basic user to premium content: denied
    print(fetch_content(3, 103))  # Premium user to gold content: denied
    print(fetch_content(3, 101))  # Premium user to basic content: granted