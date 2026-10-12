# view_content.py

from typing import Dict, Any


# Example data structures – in a real system these would come from a database
USERS: Dict[int, Dict[str, Any]] = {
    1: {"user_id": 1, "role": "admin", "subscription_tier": "premium"},
    2: {"user_id": 2, "role": "user", "subscription_tier": "basic"},
    3: {"user_id": 3, "role": "user", "subscription_tier": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"content_id": 101, "title": "Premium Article", "required_tier": "premium"},
    102: {"content_id": 102, "title": "Basic Article",   "required_tier": "basic"},
    103: {"content_id": 103, "title": "Free Article",   "required_tier": "free"},
}


def view_content(actor_user_id: int, resource_id: int) -> str:
    """
    Return the title of a content item if the actor_user_id has permission to view it.
    Admins can view all items. Regular users may only view content whose required_tier
    matches their subscription tier.

    Parameters:
        actor_user_id (int): The ID of the user attempting to access content.
        resource_id   (int): The ID of the requested content.

    Returns:
        str: The content title if access is granted, otherwise 'Access Denied'.

    Raises:
        KeyError: If the user or content ID does not exist in their respective dictionaries.
    """
    # Retrieve user and content data – KeyError will propagate if missing
    user = USERS[actor_user_id]
    resource = CONTENT[resource_id]

    # Admins bypass all checks
    if user.get("role") == "admin":
        return resource["title"]

    # Regular users: compare subscription tier with required tier
    if user.get("subscription_tier") == resource.get("required_tier"):
        return resource["title"]

    # If we reach here, access is denied
    return "Access Denied"


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    tests = [
        (1, 101),  # admin accessing premium
        (2, 102),  # basic user accessing basic
        (3, 101),  # premium user accessing premium
        (2, 101),  # basic user trying to access premium
    ]
    for uid, rid in tests:
        print(f"User {uid} accessing {rid}: {view_content(uid, rid)}")