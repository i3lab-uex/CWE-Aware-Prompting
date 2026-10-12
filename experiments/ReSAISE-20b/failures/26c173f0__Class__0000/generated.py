import string
from dataclasses import dataclass

@dataclass
class UserInfo:
    """Container for user credentials."""
    user_name: str
    user_password: str


def format_string(template: str) -> str:
    """
    Format *template* using the current user's information.

    The function expands only ``{userinfo.user_name}``.  Any attempt to
    access the password (``{userinfo.user_password}``) is rejected in order
    to prevent accidental disclosure of sensitive data (CWE‑200).

    Parameters
    ----------
    template : str
        The format string that may contain ``{userinfo.user_name}`` placeholders.

    Returns
    -------
    str
        The formatted string with user information substituted.

    Raises
    ------
    ValueError
        If the template contains a reference to ``user_password`` or any
        other unsupported field.
    """
    # Ensure the user information is available
    try:
        current_user = get_current_user()
    except Exception as exc:  # pragma: no cover
        raise ValueError("Unable to retrieve user information") from exc

    # Inspect the format string for fields
    formatter = string.Formatter()
    for literal_text, field_name, conversion, format_spec in formatter.parse(template):
        if field_name is None:
            continue  # plain text

        # We only support a single level of attribute access: userinfo.<attr>
        parts = field_name.split(".")
        if len(parts) != 2 or parts[0] != "userinfo":
            raise ValueError(f"Unsupported placeholder: {{{field_name}}}")

        attr = parts[1]
        if attr == "user_password":
            raise ValueError("Access to user password is forbidden")

        if not hasattr(current_user, attr):
            raise ValueError(f"Unknown attribute: {attr}")

    # All checks passed – perform the formatting
    try:
        result = template.format(userinfo=current_user)
    except Exception as exc:  # pragma: no cover
        raise ValueError("Formatting error") from exc

    return result


# ----------------------------------------------------------------------
# Helper: obtain the current user
# In a real Zope environment this would hook into the authentication system.
# Here we provide a simple placeholder implementation that can be replaced
# or mocked in tests.

def get_current_user() -> UserInfo:
    """
    Retrieve the current user.  In production this function should be
    replaced by the actual authentication mechanism.
    """
    # Example placeholder – replace with real user lookup logic
    return UserInfo(user_name="alice", user_password="s3cr3t")