import re

# Regular expression that matches a non-empty string containing only visible ASCII characters.
# This excludes control characters such as CR (\r) and LF (\n), which are disallowed in HTTP header values.
_SAFE_HEADER_RE = re.compile(r"^[\x21-\x7E]+$")  # ASCII characters from '!' to '~'

def append_user_header(user_header: str) -> str:
    """
    Construct a safe HTTP header line containing the user-provided value.

    The function validates that `user_header` consists only of printable ASCII characters
    (excluding CR and LF) to prevent header injection attacks. If the value fails validation,
    a ValueError is raised.

    Parameters
    ----------
    user_header : str
        The custom header value provided by the user.

    Returns
    -------
    str
        A complete header line of the form "X-Custom-Header: <value>\r\n".

    Raises
    ------
    ValueError
        If `user_header` contains disallowed characters.
    """
    if not isinstance(user_header, str):
        raise TypeError("user_header must be a string")

    # Ensure the header value does not contain CR or LF characters.
    if not _SAFE_HEADER_RE.fullmatch(user_header):
        raise ValueError("user_header contains invalid characters (CR, LF or non-ASCII)")

    # Construct the header line with CRLF terminator.
    return f"X-Custom-Header: {user_header}\r\n"