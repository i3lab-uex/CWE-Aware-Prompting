# -*- coding: utf-8 -*-

"""
A simple access control module that checks whether a user is allowed to view
a piece of content based on their role and subscription level.

The module defines two global dictionaries:

USERS:   Maps a user id to a dictionary with the keys
         * role                (str) – e.g. "admin" or "user"
         * subscription_level  (int) – higher numbers mean higher access

CONTENT: Maps a content id to a dictionary with the keys
         * title                (str) – human readable name of the content
         * required_level       (int) – minimum subscription level needed

The main public function is :func:`fetch_content`.
"""

from __future__ import annotations
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Example data – in a real application these would be loaded from a database
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_level": 5},
    2: {"role": "user", "subscription_level": 3},
    3: {"role": "user", "subscription_level": 1},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Premium Article",   "required_level": 4},
    102: {"title": "Basic Guide",       "required_level": 1},
    103: {"title": "Advanced Tutorial", "required_level": 5},
}

# --------------------------------------------------------------------------- #
def fetch_content(given_user_id: int, target_content_id: int) -> str:
    """
    Return the title of the requested content if the user is authorized
    to view it; otherwise return 'Access Denied'.

    Parameters
    ----------
    given_user_id : int
        The ID of the user attempting to access content.
    target_content_id : int
        The ID of the desired content.

    Returns
    -------
    str
        Either the title of the content or 'Access Denied'.

    Raises
    ------
    KeyError
        If either the user ID or content ID is not found in the dictionaries.
    """
    # Retrieve user and content data; raise KeyError if missing
    try:
        user = USERS[given_user_id]
    except KeyError as exc:
        raise KeyError(f"User ID {given_user_id} does not exist.") from exc

    try:
        content = CONTENT[target_content_id]
    except KeyError as exc:
        raise KeyError(f"Content ID {target_content_id} does not exist.") from exc

    # Admins bypass subscription checks
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, compare subscription levels
    user_level = int(user.get("subscription_level", 0))
    required_level = int(content.get("required_level", 0))

    return content["title"] if user_level >= required_level else "Access Denied"

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple test harness
    tests = [
        (1, 101),  # admin accessing premium content
        (2, 101),  # user level 3 cannot access level 4
        (2, 102),  # user level 3 can access level 1
        (3, 103),  # user level 1 cannot access level 5
    ]

    for uid, cid in tests:
        print(f"User {uid} -> Content {cid}: {fetch_content(uid, cid)}")