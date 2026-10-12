# -*- coding: utf-8 -*-
"""
Authorise content access based on user role and subscription level.

The module defines a single function `authorize_access` which checks whether
a user identified by `uid` is allowed to view the content identified by `cid`.

Authorisation rules:
1. Users with role ``'admin'`` always have access.
2. Regular users may only view content whose required subscription level
   is less than or equal to the user’s own subscription level.
3. If the user or content ID does not exist, or if the user is not allowed,
   the function returns ``'Access Denied'``.

The subscription levels are compared numerically – a higher value represents
a more privileged plan.  The dictionaries `USERS` and `CONTENT` can be
populated elsewhere in the application; a small example is provided for
testing purposes.
"""

from __future__ import annotations

# Example data – in a real application these would come from a database
USERS: dict[int, dict[str, str | int]] = {
    1: {"user_id": 1, "role": "admin", "subscription_level": 3},
    2: {"user_id": 2, "role": "user",  "subscription_level": 1},
    3: {"user_id": 3, "role": "user",  "subscription_level": 2},
}

CONTENT: dict[int, dict[str, str | int]] = {
    101: {"content_id": 101, "title": "Basic Article",        "required_level": 1},
    102: {"content_id": 102, "title": "Premium Video",        "required_level": 2},
    103: {"content_id": 103, "title": "VIP Interview",        "required_level": 3},
}

def authorize_access(uid: int, cid: int) -> str:
    """
    Return the title of the requested content if the user is authorised,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    uid : int
        The user identifier.
    cid : int
        The content identifier.

    Returns
    -------
    str
        Content title if authorised, else 'Access Denied'.
    """
    user = USERS.get(uid)
    content = CONTENT.get(cid)

    # If either the user or the content does not exist – deny access
    if user is None or content is None:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users: compare subscription levels
    user_level = int(user.get("subscription_level", 0))
    required_level = int(content.get("required_level", 0))

    if user_level >= required_level:
        return content["title"]

    return "Access Denied"

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(authorize_access(1, 103))  # Admin: VIP Interview
#     print(authorize_access(2, 102))  # User level 1 vs required 2: Access Denied
#     print(authorize_access(3, 102))  # User level 2 vs required 2: Premium Video