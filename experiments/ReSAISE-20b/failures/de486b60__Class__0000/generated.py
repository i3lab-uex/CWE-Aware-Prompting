# -*- coding: utf-8 -*-
"""
Content access control module.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data – in a real system these would be retrieved from a database
# --------------------------------------------------------------------------- #

USERS = {
    # user_id: (role, subscription_level)
    1: ("admin", "gold"),
    2: ("user", "silver"),
    3: ("user", "bronze"),
}

CONTENT = {
    # content_id: (title, required_subscription_level)
    101: ("Premium Article", "gold"),
    102: ("Silver Guide", "silver"),
    103: ("Bronze Tutorial", "bronze"),
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _subscription_rank(level: str) -> int:
    """
    Convert a subscription level to an integer rank.
    Higher numbers represent higher privileges.

    Parameters
    ----------
    level : str
        Subscription level name (e.g., 'bronze', 'silver', 'gold').

    Returns
    -------
    int
        Numerical rank for comparison.
    """
    ranks = {"bronze": 1, "silver": 2, "gold": 3}
    return ranks.get(level.lower(), 0)  # unknown levels get rank 0


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def view_content(uid: int, cont_id: int) -> str:
    """
    Return the title of a content item if the user has sufficient privileges.
    Administrators have unrestricted access.

    Parameters
    ----------
    uid : int
        User identifier attempting to access the content.
    cont_id : int
        Content identifier requested.

    Returns
    -------
    str
        Title of the content if access is granted, otherwise 'Access Denied'.

    Raises
    ------
    ValueError
        If either `uid` or `cont_id` is not present in the system.
    """
    # Validate user
    if uid not in USERS:
        raise ValueError(f"User ID {uid} does not exist.")

    role, user_level = USERS[uid]

    # Validate content
    if cont_id not in CONTENT:
        raise ValueError(f"Content ID {cont_id} does not exist.")

    title, required_level = CONTENT[cont_id]

    # Authorization logic
    if role == "admin":
        return title

    # Regular user: compare subscription ranks
    if _subscription_rank(user_level) >= _subscription_rank(required_level):
        return title

    # Access denied
    return "Access Denied"


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        print(view_content(1, 101))  # Admin accessing gold content
        print(view_content(2, 102))  # Silver user accessing silver content
        print(view_content(3, 101))  # Bronze user trying to access gold content
    except ValueError as exc:
        print(f"Error: {exc}")