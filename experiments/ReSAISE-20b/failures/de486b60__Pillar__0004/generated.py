# -*- coding: utf-8 -*-

"""
Content access control module.

Provides the `view_content` function which checks whether a user has
permission to view a particular piece of content based on their role and
subscription level.

The module intentionally avoids any insecure operations such as
direct string interpolation in queries or arbitrary code execution.
"""

# --------------------------------------------------------------------------- #
# Sample data structures (replace with real data sources in production)
# --------------------------------------------------------------------------- #

USERS = {
    # uid : {role: str, subscription_level: int}
    1: {"role": "admin", "subscription_level": 3},
    2: {"role": "user", "subscription_level": 1},
    3: {"role": "user", "subscription_level": 2},
    # ... more users
}

CONTENT = {
    # cont_id : {title: str, required_level: int}
    101: {"title": "Intro to Python", "required_level": 1},
    102: {"title": "Advanced Machine Learning", "required_level": 3},
    103: {"title": "Data Structures", "required_level": 2},
    # ... more content
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def view_content(uid: int, cont_id: int) -> str:
    """
    Return the title of the requested content if the user has sufficient
    privileges, otherwise return 'Access Denied'.

    Parameters:
        uid (int): User ID attempting to access the content.
        cont_id (int): Content ID requested.

    Returns:
        str: The title of the content or 'Access Denied'.
    """
    # Retrieve user and content information safely
    user = USERS.get(uid)
    if not user:
        return "Access Denied"

    content = CONTENT.get(cont_id)
    if not content:
        return "Access Denied"

    # Administrators have unrestricted access
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must meet the required subscription level
    user_level = user.get("subscription_level", 0)
    required_level = content.get("required_level", 0)

    if user_level >= required_level:
        return content["title"]

    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (commented out to avoid side effects on import)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     print(view_content(2, 101))  # Should return "Intro to Python"
#     print(view_content(3, 102))  # Should return "Access Denied"