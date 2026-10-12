from typing import Dict

# Example USERS dictionary structure.
# In a real application this would be loaded from a database or secure store.
USERS: Dict[int, Dict[str, str]] = {
    # user_id : { "role": "...", "privilege": "..." }
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}

def change_user_privileges(
    requesting_user_id: int,
    user_to_change_id: int,
    desired_privilege: str
) -> bool:
    """
    Allow an admin user to change the privilege level of another user.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    user_to_change_id : int
        ID of the target user whose privilege is to be changed.
    desired_privilege : str
        Desired privilege level for the target user. Must be one of
        'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the privilege change was applied successfully, False otherwise.
    """
    # Basic validation of input types
    if not isinstance(requesting_user_id, int) or not isinstance(user_to_change_id, int):
        return False
    if not isinstance(desired_privilege, str):
        return False

    # Ensure the desired privilege is a known value
    if desired_privilege not in ALLOWED_PRIVILEGES:
        return False

    # Retrieve user records safely
    requester = USERS.get(requesting_user_id)
    target = USERS.get(user_to_change_id)

    # If either user does not exist, deny the operation
    if requester is None or target is None:
        return False

    # Only users with 'admin' role may change privileges
    if requester.get("role") != "admin":
        return False

    # Prevent privilege escalation by non-admins
    # (already enforced above, but double‑check that the target is not an admin)
    if target.get("role") == "admin" and desired_privilege != "admin":
        # An admin can demote another admin, but this might be a policy decision.
        # Here we allow it but log or audit in real systems.
        pass

    # Apply the change
    try:
        target["privilege"] = desired_privilege
        return True
    except Exception:
        # In a real system we would log the exception.
        return False