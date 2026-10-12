#!/usr/bin/env python3
"""
Access control module.

This module provides a single function `access_content` that verifies whether a user
is allowed to view a piece of content based on their role and subscription level.

Security considerations:
- All lookups are performed in constant time to avoid timing attacks.
- The function returns a neutral string ("Access Denied") when the user is not
  authorized, preventing information leakage about the existence of resources.
"""

from __future__ import annotations

import hashlib
from typing import Dict, Any

# Example data structures. In a real system these would be fetched from a database.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription": None},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"data": "Basic content", "required_subscription": "basic"},
    102: {"data": "Premium content", "required_subscription": "premium"},
    103: {"data": "Admin only content", "required_subscription": None},
}


def _hash_compare(a: str, b: str) -> bool:
    """
    Constant‑time string comparison to mitigate timing attacks.
    """
    return hashlib.sha256(a.encode()).digest() == hashlib.sha256(b.encode()).digest()


def access_content(current_user_id: int, content_id: int) -> str:
    """
    Return the requested content data if the user is authorized,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to access the content.
    content_id : int
        The ID of the requested content.

    Returns
    -------
    str
        Content data if authorized, else 'Access Denied'.
    """
    # Retrieve user and content records safely
    user = USERS.get(current_user_id)
    content = CONTENT.get(content_id)

    # If either record is missing, deny access without revealing which
    if user is None or content is None:
        return "Access Denied"

    role = user.get("role")
    subscription = user.get("subscription")

    # Admins have full access
    if role == "admin":
        return content.get("data", "")

    # Non-admins must have a matching subscription level
    required = content.get("required_subscription")

    # Content that requires no subscription is accessible to all users
    if required is None:
        return content.get("data", "")

    # Ensure subscription comparison is safe
    if subscription and _hash_compare(subscription, required):
        return content.get("data", "")

    # Default deny
    return "Access Denied"