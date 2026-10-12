# -*- coding: utf-8 -*-

"""
Implementation of a content access manager that enforces role‑based and
subscription‑level based permissions.

Author: OpenAI ChatGPT
"""

from typing import Dict

# Sample data structures – in a real application these would come from a
# database or external service. They are defined here for completeness.
USERS: Dict[int, Dict[str, str]] = {
    # user_id : {role: str, subscription_level: str}
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    # content_id : {title: str, required_subscription_level: str}
    101: {"title": "Basic Guide", "required_subscription_level": "basic"},
    102: {"title": "Premium Insights", "required_subscription_level": "premium"},
    103: {"title": "Admin Manual", "required_subscription_level": "admin"},
}


def fetch_content(given_user_id: int, target_content_id: int) -> str:
    """
    Return the title of the requested content if the user is authorized,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    given_user_id : int
        The ID of the user attempting to access the content.
    target_content_id : int
        The ID of the content being requested.

    Returns
    -------
    str
        Content title if access is granted, otherwise 'Access Denied'.

    Raises
    ------
    ValueError
        If the user ID or content ID does not exist in the system.
    """
    # Retrieve user and content data safely
    user = USERS.get(given_user_id)
    if user is None:
        raise ValueError(f"User ID {given_user_id} not found.")

    content = CONTENT.get(target_content_id)
    if content is None:
        raise ValueError(f"Content ID {target_content_id} not found.")

    # Admins have full access
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must have a subscription level that meets or exceeds
    # the content's required level. For simplicity we define an ordering.
    subscription_order = {"basic": 1, "premium": 2}

    user_level_value = subscription_order.get(user["subscription_level"])
    content_level_value = subscription_order.get(content["required_subscription_level"])

    if user_level_value is None or content_level_value is None:
        # In case of unexpected values, deny access
        return "Access Denied"

    if user_level_value >= content_level_value:
        return content["title"]

    # All other cases are denied
    return "Access Denied"


# Example usage (uncomment to test):
# print(fetch_content(2, 101))   # Should return "Basic Guide"
# print(fetch_content(2, 102))   # Should return "Access Denied"
# print(fetch_content(1, 103))   # Admin access