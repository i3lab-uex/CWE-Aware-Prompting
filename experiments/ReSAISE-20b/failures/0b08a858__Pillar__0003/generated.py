# -*- coding: utf-8 -*-
"""
Implements a secure access control function for content based on user roles
and subscription tiers.

Author: OpenAI ChatGPT
"""

from typing import Dict, Any

# Example user and content dictionaries. In a real application these would
# be populated from a database or external service.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"user_id": 1, "role": "admin", "subscription_tier": "premium"},
    2: {"user_id": 2, "role": "user", "subscription_tier": "basic"},
    3: {"user_id": 3, "role": "user", "subscription_tier": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"content_id": 101, "title": "Basic Article", "required_tier": "basic"},
    102: {"content_id": 102, "title": "Premium Video", "required_tier": "premium"},
    103: {"content_id": 103, "title": "Admin Report", "required_tier": "admin"},
}

# Define a simple tier hierarchy for comparison
TIER_ORDER = {"basic": 1, "premium": 2, "admin": 3}


def _get_user(user_id: int) -> Dict[str, Any]:
    """
    Safely retrieve a user dictionary. Raises KeyError if the user does not exist.
    """
    try:
        return USERS[user_id]
    except KeyError as exc:
        raise KeyError(f"User with ID {user_id} not found") from exc


def _get_content(content_id: int) -> Dict[str, Any]:
    """
    Safely retrieve a content dictionary. Raises KeyError if the content does not exist.
    """
    try:
        return CONTENT[content_id]
    except KeyError as exc:
        raise KeyError(f"Content with ID {content_id} not found") from exc


def view_content(actor_user_id: int, resource_id: int) -> str:
    """
    Returns the title of a content item if the requesting user has sufficient
    privileges. Otherwise, returns 'Access Denied'.

    Parameters:
        actor_user_id (int): ID of the user requesting access.
        resource_id (int): ID of the content to be accessed.

    Returns:
        str: Content title or 'Access Denied'.

    Raises:
        KeyError: If either the user or content does not exist.
    """
    # Retrieve data safely
    user = _get_user(actor_user_id)
    content = _get_content(resource_id)

    # Admins have unconditional access
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, compare subscription tiers
    user_tier = user.get("subscription_tier")
    required_tier = content.get("required_tier")

    # Map tiers to numeric values; if tier unknown, deny access
    user_rank = TIER_ORDER.get(user_tier)
    required_rank = TIER_ORDER.get(required_tier)

    if user_rank is None or required_rank is None:
        return "Access Denied"

    # User must have a tier equal or higher than required
    if user_rank >= required_rank:
        return content["title"]

    # Otherwise deny access
    return "Access Denied"