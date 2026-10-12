#!/usr/bin/env python3
"""
Utility to retrieve content based on user role and subscription level.
"""

from typing import Dict, List

# --------------------------------------------------------------------------- #
# Sample data – in a real application these would be fetched from a database
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "standard"},
    # Add more users as needed
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Basic Guide", "required_subscription": "basic"},
    102: {"title": "Standard Tutorial", "required_subscription": "standard"},
    103: {"title": "Premium Insights", "required_subscription": "premium"},
    # Add more content as needed
}

# Ordered from lowest to highest subscription level
SUBSCRIPTION_HIERARCHY: List[str] = ["basic", "standard", "premium"]

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def retrieve_content(usr_id: int, contid: int) -> str:
    """
    Return the title of the requested content if the user has sufficient
    privileges. Otherwise, return 'Access Denied'.

    Parameters
    ----------
    usr_id : int
        The ID of the user attempting to access the content.
    contid : int
        The ID of the requested content.

    Returns
    -------
    str
        Title of the content or 'Access Denied'.
    """
    # Validate inputs – ensure they are integers
    if not isinstance(usr_id, int) or not isinstance(contid, int):
        raise TypeError("Both usr_id and contid must be integers")

    # Fetch user record
    user = USERS.get(usr_id)
    if not user:
        return "Access Denied"

    # Fetch content record
    content = CONTENT.get(contid)
    if not content:
        return "Access Denied"

    # Administrators bypass subscription checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users – check subscription hierarchy
    user_level = user.get("subscription")
    required_level = content.get("required_subscription")

    # Ensure both levels are valid
    if user_level not in SUBSCRIPTION_HIERARCHY or required_level not in SUBSCRIPTION_HIERARCHY:
        return "Access Denied"

    # User can access if their level is equal or higher in the hierarchy
    if SUBSCRIPTION_HIERARCHY.index(user_level) >= SUBSCRIPTION_HIERARCHY.index(required_level):
        return content["title"]

    # Otherwise access denied
    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    print(retrieve_content(1, 103))   # Admin: should see "Premium Insights"
    print(retrieve_content(2, 102))   # Basic user: should see "Access Denied"
    print(retrieve_content(3, 102))   # Standard user: should see "Standard Tutorial"