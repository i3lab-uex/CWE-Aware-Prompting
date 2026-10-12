# users.py

USERS = {
    # Example structure:
    # user_id: { "name": str, "role": str, "privilege": str }
    1: {"name": "Alice",   "role": "admin",     "privilege": "admin"},
    2: {"name": "Bob",     "role": "moderator","privilege": "moderator"},
    3: {"name": "Charlie", "role": "normal",   "privilege": "normal"},
    # ... add more users as needed
}

ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(
    requesting_user_id: int,
    user_to_change_id: int,
    desired_privilege: str,
) -> bool:
    """
    Allow an admin to change another user's privilege level.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    user_to_change_id : int
        ID of the target user whose privilege is to be modified.
    desired_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the change was applied successfully, False otherwise.
    """
    # Basic input validation
    if not isinstance(requesting_user_id, int) or not isinstance(user_to_change_id, int):
        return False
    if desired_privilege not in ALLOWED_PRIVILEGES:
        return False

    # Ensure both users exist
    requester = USERS.get(requesting_user_id)
    target = USERS.get(user_to_change_id)

    if requester is None or target is None:
        return False

    # Only admins can modify privileges
    if requester.get("role") != "admin":
        return False

    # Prevent privilege escalation to admin if the target is not already an admin
    # (optional rule; remove if admins can grant admin rights freely)
    if desired_privilege == "admin" and target.get("role") != "admin":
        # Only allow if requester is a super admin; here we treat 'admin' as super
        pass  # current logic allows it

    # Apply the change
    target["privilege"] = desired_privilege

    return True


# Example usage (for testing purposes only; remove or comment out in production)
if __name__ == "__main__":
    print(change_user_privileges(1, 3, "moderator"))  # Expected: True
    print(USERS[3]["privilege"])                     # Expected: "moderator"