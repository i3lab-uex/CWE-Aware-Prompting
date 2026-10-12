# -*- coding: utf-8 -*-
"""
Utility for retrieving content based on user subscription level.

The module defines a single function `retrieve_content` that checks whether a
user is allowed to view a particular piece of content.  Administrators are
granted unrestricted access; regular users may only view content whose
required subscription level is less than or equal to their own.

The implementation performs input validation and raises informative
exceptions for missing users or content entries.  All data structures are
defined at module level for easy configuration.

Author: ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Data structures (example values – replace with real data as needed)
# --------------------------------------------------------------------------- #

USERS = {
    # user_id: {"role": "admin" | "user", "subscription": str}
    1: {"role": "admin", "subscription": "gold"},
    2: {"role": "user", "subscription": "silver"},
    3: {"role": "user", "subscription": "bronze"},
}

CONTENT = {
    # content_id: {"title": str, "required_subscription": str}
    101: {"title": "Advanced Topics", "required_subscription": "gold"},
    102: {"title": "Intermediate Guide", "required_subscription": "silver"},
    103: {"title": "Beginner's Handbook", "required_subscription": "bronze"},
}

# Defines the hierarchy from lowest to highest subscription levels
subscription_hierarchy = ["bronze", "silver", "gold"]


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _subscription_rank(level: str) -> int:
    """
    Convert a subscription level to its rank in the hierarchy.

    Parameters
    ----------
    level : str
        The subscription level to look up.

    Returns
    -------
    int
        The index of the level in `subscription_hierarchy`.  Lower indices
        correspond to lower privileges.

    Raises
    ------
    ValueError
        If the level is not present in the hierarchy.
    """
    try:
        return subscription_hierarchy.index(level)
    except ValueError as exc:
        raise ValueError(f"Unknown subscription level: {level}") from exc


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def retrieve_content(usr_id: int, contid: int) -> str:
    """
    Return the title of the requested content if the user has sufficient
    privileges; otherwise return 'Access Denied'.

    Parameters
    ----------
    usr_id : int
        Identifier of the user attempting access.
    contid : int
        Identifier of the content being requested.

    Returns
    -------
    str
        The content title if access is granted, or 'Access Denied'.

    Raises
    ------
    KeyError
        If `usr_id` or `contid` does not exist in the corresponding dictionaries.
    ValueError
        If a subscription level is unrecognised.
    """
    # Validate existence of user and content
    if usr_id not in USERS:
        raise KeyError(f"User ID {usr_id} does not exist.")
    if contid not in CONTENT:
        raise KeyError(f"Content ID {contid} does not exist.")

    user = USERS[usr_id]
    content = CONTENT[contid]

    # Administrators bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users: compare subscription ranks
    user_level = user.get("subscription")
    required_level = content.get("required_subscription")

    # Ensure subscription levels are known
    user_rank = _subscription_rank(user_level)
    required_rank = _subscription_rank(required_level)

    if user_rank >= required_rank:
        return content["title"]

    return "Access Denied"


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Test cases
    for uid in USERS:
        for cid in CONTENT:
            try:
                print(f"User {uid} accessing content {cid}: "
                      f"{retrieve_content(uid, cid)}")
            except Exception as exc:
                print(f"Error: {exc}")