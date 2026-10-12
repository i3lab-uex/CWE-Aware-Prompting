#!/usr/bin/env python3
"""
Implementation of access control for content based on user role and subscription level.
The function raises a ValueError if the supplied uid or cid is not found in the
predefined data structures.
"""

# Sample data – in a real application these would come from a database or external service
USERS = {
    1: {"user_id": 1, "role": "admin", "subscription_level": None},
    2: {"user_id": 2, "role": "user", "subscription_level": "basic"},
    3: {"user_id": 3, "role": "user", "subscription_level": "premium"},
}

CONTENT = {
    101: {"title": "Intro to Python", "required_level": "basic"},
    102: {"title": "Advanced ML", "required_level": "premium"},
    103: {"title": "Admin Guide", "required_level": None},  # accessible to all
}

# Define an ordering of subscription levels for comparison purposes
SUBSCRIPTION_ORDER = {"basic": 1, "premium": 2}


def authorize_access(uid: int, cid: int) -> str:
    """
    Determine whether a user is authorized to access a piece of content.

    Parameters
    ----------
    uid : int
        The ID of the user attempting to access the content.
    cid : int
        The ID of the requested content.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise 'Access Denied'.

    Raises
    ------
    ValueError
        If the user ID or content ID is not found in the data structures.
    """
    # Validate existence of user and content
    if uid not in USERS:
        raise ValueError(f"User ID {uid} does not exist.")
    if cid not in CONTENT:
        raise ValueError(f"Content ID {cid} does not exist.")

    user = USERS[uid]
    content = CONTENT[cid]

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, compare subscription levels
    required = content.get("required_level")
    if required is None:
        # Content with no level requirement is publicly accessible
        return content["title"]

    user_level = user.get("subscription_level")
    if user_level is None:
        return "Access Denied"

    # Ensure the subscription level exists in our ordering map
    if required not in SUBSCRIPTION_ORDER or user_level not in SUBSCRIPTION_ORDER:
        return "Access Denied"

    # Grant access only if user's level is equal or higher than required
    if SUBSCRIPTION_ORDER[user_level] >= SUBSCRIPTION_ORDER[required]:
        return content["title"]

    return "Access Denied"


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    test_cases = [(1, 101), (2, 102), (3, 102), (4, 103)]
    for uid, cid in test_cases:
        try:
            print(f"User {uid} accessing content {cid}: {authorize_access(uid, cid)}")
        except ValueError as e:
            print(f"User {uid} accessing content {cid}: Error - {e}")