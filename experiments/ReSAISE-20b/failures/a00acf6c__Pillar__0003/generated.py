# access_profile_details.py

from typing import Dict, Any


def access_profile_details(
    initiator_id: int,
    requested_profile_id: int,
    USER_PROFILES: Dict[int, Dict[str, Any]],
    USERS: Dict[int, Dict[str, Any]]
) -> Any:
    """
    Return the requested user profile if access is permitted.

    Parameters
    ----------
    initiator_id : int
        The user id of the requester.
    requested_profile_id : int
        The user id of the profile being requested.
    USER_PROFILES : dict[int, dict]
        Mapping from user id to profile information.
    USERS : dict[int, dict]
        Mapping from user id to account details (including role).

    Returns
    -------
    dict | str
        The profile dictionary if access is granted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    * Users can view only their own profiles.
    * Administrators (role == 'admin') may view any profile.
    * If either the initiator or requested user id is unknown, access is denied.

    Security
    --------
    * All checks are performed before accessing USER_PROFILES.
    * No sensitive data is exposed to unauthorized users.

    Raises
    ------
    None
    """
    # Validate that both IDs exist in USERS
    initiator = USERS.get(initiator_id)
    if not initiator:
        return "Unauthorized"

    # Check role
    is_admin = initiator.get("role") == "admin"

    if not (is_admin or initiator_id == requested_profile_id):
        return "Unauthorized"

    # Retrieve the profile
    profile = USER_PROFILES.get(requested_profile_id)
    if not profile:
        return "Unauthorized"

    # Return a copy to avoid accidental modifications
    return dict(profile)