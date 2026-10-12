import re
from dataclasses import dataclass

# --------------------------------------------------------------------------- #
# Data model – user information
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class UserInfo:
    """Container for user credentials."""
    user_name: str
    user_password: str


# --------------------------------------------------------------------------- #
# Formatting utility – safe string formatting
# --------------------------------------------------------------------------- #
def format_string(string: str) -> str:
    """
    Format *string* using the `UserInfo` context.

    The function only allows placeholders that refer to public user data
    (`{userinfo.user_name}`).  Attempts to expose sensitive information,
    such as the password, are rejected.

    Parameters
    ----------
    string : str
        The template string containing placeholders.

    Returns
    -------
    str
        The formatted string.

    Raises
    ------
    ValueError
        If the template references a sensitive attribute or if formatting
        fails for any reason.
    """
    # Reject templates that attempt to expose the password
    if re.search(r"\{userinfo\.user_password\}", string):
        raise ValueError("Template may not expose user password")

    # Prepare a UserInfo instance with dummy values
    # In real usage, this would be the actual logged‑in user.
    dummy_user = UserInfo(user_name="dummy", user_password="******")

    try:
        # Perform the formatting
        result = string.format(userinfo=dummy_user)
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"Formatting error: {exc}") from exc

    return result