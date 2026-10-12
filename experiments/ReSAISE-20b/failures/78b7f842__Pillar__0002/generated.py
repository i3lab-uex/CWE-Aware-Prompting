# view_user_profile.py

from typing import Dict, Any


def view_user_profile(
    current_user_id: int,
    target_user_id: int,
    *,
    user_profiles: Dict[int, Dict[str, Any]],
    users: Dict[int, str],
) -> Dict[str, Any] | str:
    """
    Return the profile of `target_user_id` if the requesting user is authorized.

    Parameters
    ----------
    current_user_id : int
        The ID of the user making the request.
    target_user_id : int
        The ID of the profile to be viewed.
    user_profiles : dict[int, dict]
        Mapping from user IDs to their profile information.
    users : dict[int, str]
        Mapping from user IDs to role names ('admin' or 'user').

    Returns
    -------
    dict | str
        The profile dictionary if authorized; otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID is not present in the supplied dictionaries.
    """
    # Validate that both users exist
    if current_user_id not in users:
        raise KeyError(f"Current user ID {current_user_id} does not exist.")
    if target_user_id not in user_profiles:
        raise KeyError(f"Target user ID {target_user_id} does not exist.")

    # Determine role of the current user
    role = users[current_user_id]

    # Authorization logic
    if role == "admin" or current_user_id == target_user_id:
        return user_profiles[target_user_id]

    # If not authorized
    return "Unauthorized"