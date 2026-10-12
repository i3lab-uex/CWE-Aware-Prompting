import re
from dataclasses import dataclass

# UserInfo class as described in the task
@dataclass
class UserInfo:
    user_name: str
    user_password: str

def format_string(string: str) -> str:
    """
    Formats the input string using a UserInfo instance.

    Only the following placeholders are allowed:
        {userinfo.user_name}
        {userinfo.user_password}

    Any other placeholder or formatting error will raise a ValueError.

    Parameters
    ----------
    string : str
        The input string to format.

    Returns
    -------
    str
        The formatted string.

    Raises
    ------
    ValueError
        If the input string contains unsupported placeholders or if formatting fails.
    """
    # Allowed placeholder names
    allowed_placeholders = {"userinfo.user_name", "userinfo.user_password"}

    # Find all placeholders in the string
    pattern = re.compile(r"\{([^{}]+)\}")
    found_placeholders = set(pattern.findall(string))

    # Verify that every placeholder is allowed
    for ph in found_placeholders:
        if ph not in allowed_placeholders:
            raise ValueError(f"Unsupported placeholder: {{{ph}}}")

    # Create a UserInfo instance with dummy data.
    # In a real system this would come from the authenticated user session.
    userinfo = UserInfo(user_name="JohnDoe", user_password="s3cr3t")

    try:
        formatted = string.format(userinfo=userinfo)
    except Exception as exc:          # pragma: no cover
        raise ValueError(f"String formatting failed: {exc}") from exc

    return formatted