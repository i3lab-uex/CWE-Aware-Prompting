# -*- coding: utf-8 -*-
"""
Author: OpenAI ChatGPT
Description:
    Utility to retrieve content based on user role and subscription level.
"""

# --------------------------------------------------------------------------- #
#   Data structures
# --------------------------------------------------------------------------- #

USERS = {
    # usr_id : { "role": str, "subscription": str }
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user",  "subscription": "basic"},
    3: {"role": "user",  "subscription": "premium"},
    4: {"role": "user",  "subscription": "standard"},
}

CONTENT = {
    # contid : { "title": str, "required_subscription": str }
    101: {"title": "Intro to Python",      "required_subscription": "basic"},
    102: {"title": "Advanced AI",          "required_subscription": "premium"},
    103: {"title": "Data Science Basics",  "required_subscription": "standard"},
}

# Define the hierarchy from lowest to highest
subscription_hierarchy = ["basic", "standard", "premium"]


# --------------------------------------------------------------------------- #
#   Helper functions
# --------------------------------------------------------------------------- #

def _subscription_index(sub: str) -> int:
    """
    Return the index of a subscription level in the hierarchy.
    Raises ValueError if the subscription is unknown.
    """
    try:
        return subscription_hierarchy.index(sub)
    except ValueError as exc:
        raise ValueError(f"Unknown subscription level: {sub}") from exc


# --------------------------------------------------------------------------- #
#   Main function
# --------------------------------------------------------------------------- #

def retrieve_content(usr_id: int, contid: int) -> str:
    """
    Return the title of the requested content if the user has sufficient
    authorization, otherwise return 'Access Denied'.

    Parameters:
        usr_id (int): The ID of the user requesting access.
        contid (int): The ID of the content to retrieve.

    Raises:
        KeyError: If usr_id or contid does not exist in the respective dictionaries.
        ValueError: If a subscription level is unknown.

    Returns:
        str: Content title or 'Access Denied'.
    """
    # Fetch user and content data; KeyError will propagate if missing
    user = USERS[usr_id]
    content = CONTENT[contid]

    # Administrators bypass all checks
    if user["role"] == "admin":
        return content["title"]

    # For regular users, compare subscription levels
    user_sub_index = _subscription_index(user["subscription"])
    required_sub_index = _subscription_index(content["required_subscription"])

    if user_sub_index >= required_sub_index:
        return content["title"]
    else:
        return "Access Denied"


# --------------------------------------------------------------------------- #
#   Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    tests = [
        (1, 101),   # admin
        (2, 102),   # basic user trying premium content
        (3, 103),   # premium user accessing standard content
    ]
    for uid, cid in tests:
        print(f"User {uid} accessing content {cid}: {retrieve_content(uid, cid)}")