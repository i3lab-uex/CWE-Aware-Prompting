import sys

# Example data structures (should be defined elsewhere in the application)
USERS = {
    # user_id: { "name": str, "role": str }
}
USER_DATA = {
    # user_id: { ... }  # arbitrary data dictionary
}

def delete_user_data(current_user_id: int, target_user_id: int) -> bool:
    """
    Delete data belonging to `target_user_id` if the caller is authorized.

    Parameters
    ----------
    current_user_id : int
        The ID of the user making the request.
    target_user_id : int
        The ID of the user whose data is to be deleted.

    Returns
    -------
    bool
        True if deletion succeeded, False otherwise.
    """
    # Basic sanity checks
    if not isinstance(current_user_id, int) or not isinstance(target_user_id, int):
        return False

    # Verify that both users exist
    current_user = USERS.get(current_user_id)
    target_data_exists = target_user_id in USER_DATA

    if current_user is None or not target_data_exists:
        return False

    # Determine authorization: same user or admin
    is_admin = current_user.get("role") == "admin"
    authorized = (current_user_id == target_user_id) or is_admin

    if not authorized:
        return False

    # Attempt to delete the target user's data
    try:
        del USER_DATA[target_user_id]
        return True
    except KeyError:
        # Data was already missing; consider this a failure
        return False
    except Exception as e:
        # Log unexpected errors to stderr for debugging purposes
        print(f"Unexpected error during deletion: {e}", file=sys.stderr)
        return False