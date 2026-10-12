#!/usr/bin/env python3
"""
Utility to fetch content based on user role and subscription tier.
"""

from typing import Dict, Any

# --------------------------------------------------------------------
# Example data structures. In a real application these would come from
# a database or an external service.
# --------------------------------------------------------------------
USERS: Dict[int, Dict[str, Any]] = {
    # user_id : {role: str, tier: str or None}
    1: {"role": "admin", "tier": None},
    2: {"role": "user",  "tier": "basic"},
    3: {"role": "user",  "tier": "premium"},
    4: {"role": "user",  "tier": "vip"},
}

# Content required subscription level
CONTENT: Dict[int, Dict[str, Any]] = {
    # content_id : {title: str, required_tier: str or None}
    101: {"title": "Basic Guide",          "required_tier": "basic"},
    102: {"title": "Premium Insights",     "required_tier": "premium"},
    103: {"title": "VIP Exclusive Video",  "required_tier": "vip"},
    104: {"title": "Open Access Article",  "required_tier": None},   # free content
}

# Define a simple ordering for tiers. Higher index = higher privilege.
_TIER_ORDER: Dict[str, int] = {
    "basic": 1,
    "premium": 2,
    "vip": 3
}

def _tier_value(tier: str | None) -> int:
    """
    Convert a tier string to an integer value.  `None` (free content) is
    considered lowest privilege (0).  Unknown tiers are treated as 0.
    """
    if tier is None:
        return 0
    return _TIER_ORDER.get(tier, 0)

def get_content(active_user_id: int, item_id: int) -> str:
    """
    Return the title of the requested content if the user has permission,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    active_user_id : int
        The identifier of the user attempting to access content.
    item_id : int
        The identifier of the content the user is trying to access.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # 1. Validate user exists
    user = USERS.get(active_user_id)
    if not user:
        return "Access Denied"

    # 2. Validate content exists
    content = CONTENT.get(item_id)
    if not content:
        return "Access Denied"

    # 3. Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # 4. Regular users must satisfy tier requirement
    user_tier = user.get("tier")
    required_tier = content.get("required_tier")

    # Free content is always accessible
    if required_tier is None:
        return content["title"]

    # Compare tier levels
    if _tier_value(user_tier) >= _tier_value(required_tier):
        return content["title"]

    # If none of the above, deny access
    return "Access Denied"

# --------------------------------------------------------------------
# Example usage (commented out for production use)
# --------------------------------------------------------------------
# if __name__ == "__main__":
#     print(get_content(2, 101))  # Should return "Basic Guide"
#     print(get_content(2, 102))  # Should return "Access Denied"