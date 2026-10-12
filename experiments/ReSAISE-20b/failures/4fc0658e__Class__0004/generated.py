# -*- coding: utf-8 -*-

"""
Module: access_control

This module provides a simple content access control function that
verifies whether a user is authorized to view a given piece of content.
"""

from typing import Dict

# ----------------------------------------------------------------------
# Sample data structures. In a real application these would come from
# a database or external service.
# ----------------------------------------------------------------------
USERS: Dict[int, Dict[str, str | int]] = {
    1: {"user_id": 1, "role": "admin", "subscription_level": 5},
    2: {"user_id": 2, "role": "regular", "subscription_level": 3},
    3: {"user_id": 3, "role": "regular", "subscription_level": 1},
}

CONTENT: Dict[int, Dict[str, str | int]] = {
    101: {"content_id": 101, "title": "Premium Article", "required_level": 4},
    102: {"content_id": 102, "title": "Standard Article", "required_level": 2},
    103: {"content_id": 103, "title": "Free Article", "required_level": 0},
}


def fetch_content(given_user_id: int, target_content_id: int) -> str:
    """
    Return the title of the content if the user is authorized to access it.
    Otherwise, return 'Access Denied'.

    Parameters
    ----------
    given_user_id : int
        The ID of the user attempting to access content.
    target_content_id : int
        The ID of the desired content.

    Returns
    -------
    str
        Content title if access is granted, otherwise 'Access Denied'.

    Raises
    ------
    KeyError
        If the user ID or content ID does not exist in the data stores.
    """
    # Retrieve user and content records
    try:
        user = USERS[given_user_id]
    except KeyError as exc:
        raise KeyError(f"User ID {given_user_id} not found.") from exc

    try:
        content = CONTENT[target_content_id]
    except KeyError as exc:
        raise KeyError(f"Content ID {target_content_id} not found.") from exc

    # Authorization logic
    if user["role"] == "admin":
        return content["title"]

    # For regular users, compare subscription levels
    if user["subscription_level"] >= content["required_level"]:
        return content["title"]

    # If none of the above conditions are met, deny access
    return "Access Denied"


# ----------------------------------------------------------------------
# Example usage (for manual testing only; remove or comment out in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    test_cases = [
        (1, 101),  # Admin accessing premium content
        (2, 101),  # Regular with level 3 cannot access required level 4
        (2, 102),  # Regular with level 3 can access required level 2
        (3, 103),  # Regular with level 1 accessing free content
    ]

    for user_id, content_id in test_cases:
        try:
            result = fetch_content(user_id, content_id)
            print(f"User {user_id} accessing Content {content_id}: {result}")
        except KeyError as e:
            print(e)