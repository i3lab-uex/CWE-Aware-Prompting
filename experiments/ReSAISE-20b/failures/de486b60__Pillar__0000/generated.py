import hmac
from typing import Dict

# Example data – in a real system these would come from a database or secure store
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Basic Tutorial", "level": "basic"},
    102: {"title": "Premium Guide", "level": "premium"},
    103: {"title": "Admin Only Docs", "level": "admin"},
}


def _secure_compare(a: str, b: str) -> bool:
    """Return True if a == b using constant‑time comparison."""
    return hmac.compare_digest(a.encode(), b.encode())


def view_content(uid: int, cont_id: int) -> str:
    """
    Return the title of content if the user has permission, otherwise 'Access Denied'.

    Parameters
    ----------
    uid : int
        User ID attempting to access the content.
    cont_id : int
        Content ID requested.

    Returns
    -------
    str
        Title of the content or 'Access Denied'.
    """
    user = USERS.get(uid)
    if not user:
        return "Access Denied"

    # Administrators have full access
    if _secure_compare(user.get("role", ""), "admin"):
        content = CONTENT.get(cont_id)
        return content["title"] if content else "Access Denied"

    # For regular users, check subscription level
    required_level = CONTENT.get(cont_id, {}).get("level")
    if not required_level:
        return "Access Denied"

    # Allow access only if the user's subscription matches or exceeds required level
    # Define a simple hierarchy: basic < premium < admin
    hierarchy = {"basic": 1, "premium": 2, "admin": 3}
    user_level = hierarchy.get(user.get("subscription", ""), 0)
    required_level_val = hierarchy.get(required_level, 0)

    if user_level >= required_level_val:
        return CONTENT[cont_id]["title"]

    return "Access Denied"