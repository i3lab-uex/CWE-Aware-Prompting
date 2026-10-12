import re

# Example USERS dictionary structure.
# In a real application this would come from a database or secure store.
USERS = {
    1: {"name": "Alice",   "role": "admin",     "privilege": "admin"},
    2: {"name": "Bob",     "role": "moderator","privilege": "moderator"},
    3: {"name": "Charlie", "role": "user",     "privilege": "normal"},
    # ... more users ...
}

# Allowed privilege levels
_ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}

def update_user_privilege(actor_id: int, recipient_id: int, updated_privilege: str) -> bool:
    """
    Allows an admin user to change the privilege level of another user.

    Parameters
    ----------
    actor_id : int
        ID of the user making the request.
    recipient_id : int
        ID of the user whose privilege is to be changed.
    updated_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was updated successfully, False otherwise.
    """
    # Validate input types
    if not isinstance(actor_id, int) or not isinstance(recipient_id, int):
        return False

    # Normalise privilege string
    if not isinstance(updated_privilege, str):
        return False
    updated_privilege = updated_privilege.strip().lower()

    # Check that the requested privilege is valid
    if updated_privilege not in _ALLOWED_PRIVILEGES:
        return False

    # Fetch actor and recipient records
    actor = USERS.get(actor_id)
    recipient = USERS.get(recipient_id)

    # Actor must exist and be an admin
    if not actor or actor.get("role") != "admin":
        return False

    # Recipient must exist
    if not recipient:
        return False

    # Prevent privilege escalation on self (optional: allow but warn)
    if actor_id == recipient_id and updated_privilege != recipient.get("privilege"):
        # Admin changing own privilege: allow but log or handle as needed
        pass

    # Perform the update
    try:
        recipient["privilege"] = updated_privilege
        return True
    except Exception:
        # In a real system we would log the exception
        return False