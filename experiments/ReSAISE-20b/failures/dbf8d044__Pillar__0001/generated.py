# -*- coding: utf-8 -*-
"""
Utility to update user privilege levels while enforcing proper access control.

This module defines a single function `update_user_privilege` that allows an
administrator to change the privilege level of another user account.  The
implementation follows best practices for security and mitigates common
access‑control vulnerabilities (CWE‑284).

Author: OpenAI ChatGPT
"""

from typing import Dict, Any

# Example user store; in a real system this would come from a database.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "alice",   "role": "admin",     "privilege": "admin"},
    2: {"name": "bob",     "role": "moderator","privilege": "moderator"},
    3: {"name": "charlie", "role": "normal",   "privilege": "normal"},
    # Add more users as needed.
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_privilege(actor_id: int, recipient_id: int, updated_privilege: str) -> bool:
    """
    Update the privilege level of a user account.

    Parameters
    ----------
    actor_id : int
        The ID of the user making the request.
    recipient_id : int
        The ID of the user whose privilege is being changed.
    updated_privilege : str
        Desired privilege level for the target user. Must be one of
        {'normal', 'moderator', 'admin'}.

    Returns
    -------
    bool
        True if the privilege change succeeded, False otherwise.
    """
    # 1. Validate input types (basic sanity check)
    if not isinstance(actor_id, int) or not isinstance(recipient_id, int):
        return False
    if not isinstance(updated_privilege, str):
        return False

    # 2. Ensure the target privilege is allowed
    if updated_privilege not in ALLOWED_PRIVILEGES:
        return False

    # 3. Actor must exist
    actor = USERS.get(actor_id)
    if actor is None:
        return False

    # 4. Actor must be an admin
    if actor.get("role") != "admin":
        return False

    # 5. Prevent an admin from demoting themselves
    if actor_id == recipient_id:
        return False

    # 6. Recipient must exist
    recipient = USERS.get(recipient_id)
    if recipient is None:
        return False

    # 7. Update the privilege
    try:
        recipient["privilege"] = updated_privilege
        # Optionally update the role to match privilege level for consistency.
        recipient["role"] = updated_privilege
    except Exception:
        # Log exception in real system; here we simply return False.
        return False

    return True